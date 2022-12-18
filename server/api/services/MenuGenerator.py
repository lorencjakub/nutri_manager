from api.models.models import CsNutriRecipes, EnNutriRecipes, DeNutriRecipes
import random
from datetime import datetime
from distinct_types import List, Type, GeneratedMenu, GeneratedMenuData, Union


class Menu:
    def __init__(self, proteins: float = 0, carbs: float = 0, fats: float = 0,
                 energy: float = 2000, tags: list = None, with_snack: bool = True) -> None:
        """Menu object class.

        It is able to create random menu according to defined optional parameters.
        :param energy: Maximum sum of energy for a day in kcal. Default value is 2000 kcal.
        :param proteins: Ratio of total energy from proteins to total energy from day in %. Default value is 40%.
        :param carbs: Ratio of total energy from carbs to total energy from day in %. Default value is 40%.
        :param fats: Ratio of total energy from fats to total energy from day in %. Default value is 20%.
        :param tags: tags of specific food categories. Default value is None.
        :param with_snack: Boolean parameter. According this menu will be generated with or without the snack.
        Default value is True.
        """
        self.__is_data_valid = self.__validate_parameters(proteins, carbs, fats, energy)

        if not self.__is_data_valid:
            return

        self.__referential_unit_energy = 4
        self.__referential_fat_energy = 9
        self.__referential_fiber_amount = 30

        self.__max_energy = float(energy)
        self.__proteins_ratio = float(proteins) if proteins != 0 else 40
        self.__carbs_ratio = float(carbs) if carbs != 0 else 40
        self.__fats_ratio = float(fats) if fats != 0 else 20
        self.__tags = tags if tags else []

        self.__with_snack: bool = with_snack
        self.__max_generate_count = 300
        self.__start_time = datetime.now().timestamp()

        self.__balance_nutrients_ratios()

    @classmethod
    def __validate_parameters(cls, proteins: float = 0, carbs: float = 0,
                              fats: float = 0, energy: float = 2000) -> bool:
        for p in [proteins, carbs, fats, energy]:
            if (isinstance(p, float) or str(p).isdigit()) and float(p) >= 0:
                continue

            else:
                return False

        return True

    def is_valid(self) -> bool:
        return self.__is_data_valid

    def __start_timer(self) -> None:
        self.__start_time = datetime.now().timestamp()

    def __balance_nutrients_ratios(self) -> None:
        sum_of_ratios = self.__carbs_ratio + self.__proteins_ratio + self.__fats_ratio

        if sum_of_ratios <= 100:
            diff = 100 - sum_of_ratios
            self.__carbs_ratio += diff / 3
            self.__proteins_ratio += diff / 3
            self.__fats_ratio += diff / 3

        else:
            self.__carbs_ratio = round((self.__carbs_ratio / sum_of_ratios) * 100, 0)
            self.__proteins_ratio = round((self.__proteins_ratio / sum_of_ratios) * 100, 0)
            self.__fats_ratio = round((self.__fats_ratio / sum_of_ratios) * 100, 0)

    def create_menu(self) -> Union[GeneratedMenuData, None]:
        """
        This method takes generated menu from generate_menu() method and summarizes energies from foods.
        If the total energy of day is under 80% of the maximum energy or over the maximum energy, the current menu
        is dropped and the new one is going to be generated. The same case occurs if nutrients ratios are over
        specified maximum ratios (with the tolerance +2.5 for every ratio).

        :return "foods": {
                "breakfast": {
                    "id": int = ID of food in DB,
                    "name": str = name of food,
                    "url": str = url of recipe on zdraverecepty.cz,
                    "portions: int = count of portions of food
                },
                "lunch": {
                    "id": int = ID of food in DB,
                    "name": str = name of food,
                    "url": str = url of recipe on zdraverecepty.cz,
                    "portions: int = count of portions of food
                },
                "snack": {
                    "id": int = ID of food in DB,
                    "name": str = name of food,
                    "url": str = url of recipe on zdraverecepty.cz,
                    "portions: int = count of portions of food
                } if self.__with_snack else None,
                "dinner": {
                    "id": int = ID of food in DB,
                    "name": str = name of food,
                    "url": str = url of recipe on zdraverecepty.cz,
                    "portions: int = count of portions of food
                }
            },
            "nutrients": {
                "energy": float = total energy for a day in kcal,
                "carbs": float = % ratio of carbs,
                "proteins": float = % ratio of proteins,
                "fats": float = % ratio of fats,
                "fiber": float = amount of fiber in g
            }
        :rtype GeneratedMenuData
        """

        parameters_fulfilled: bool = False
        generate_count = 0
        self.__start_timer()

        menu: List[Type[CsNutriRecipes]] = []
        daily_energy: float = 0
        daily_carbs_energy: float = 0
        daily_proteins_energy: float = 0
        daily_fats_energy: float = 0
        daily_fiber_amount: float = 0

        while not parameters_fulfilled and generate_count < self.__max_generate_count:
            menu = self.generate_menu()
            generate_count += 1

            daily_energy = sum([float(food.energy) for food in menu])
            daily_carbs_energy = sum([float(food.carbs) for food in menu]) * 4
            daily_proteins_energy = sum([float(food.proteins) for food in menu]) * 4
            daily_fats_energy = sum([float(food.fats) for food in menu]) * 9
            daily_fiber_amount = sum([float(food.fiber) for food in menu])

            if 0.8 * self.__max_energy <= daily_energy <= self.__max_energy \
                    and (daily_carbs_energy / daily_energy) * 100 <= self.__carbs_ratio + 2.5 \
                    and (daily_proteins_energy / daily_energy) * 100 <= self.__proteins_ratio + 2.5\
                    and (daily_fats_energy / daily_energy) * 100 <= self.__fats_ratio + 2.5:
                parameters_fulfilled = True

        if not parameters_fulfilled:
            return None

        response = {
            "iterations": generate_count,
            "foods": {
                "breakfast": {
                    "id": menu[0].id,
                    "recipe_id": menu[0].recipe_id,
                    "cs_name": menu[0].name,
                    "cs_url": menu[0].url,
                    "portions": menu[0].portions
                },
                "lunch": {
                    "id": menu[1].id,
                    "recipe_id": menu[1].recipe_id,
                    "cs_name": menu[1].name,
                    "cs_url": menu[1].url,
                    "portions": menu[1].portions
                },
                "snack": {
                    "id": menu[2].id,
                    "recipe_id": menu[2].recipe_id,
                    "cs_name": menu[2].name,
                    "cs_url": menu[2].url,
                    "portions": menu[2].portions
                } if self.__with_snack else None,
                "dinner": {
                    "id": menu[3 if self.__with_snack else 4].id,
                    "recipe_id": menu[3 if self.__with_snack else 4].recipe_id,
                    "cs_name": menu[3 if self.__with_snack else 4].name,
                    "cs_url": menu[3 if self.__with_snack else 4].url,
                    "portions": menu[3 if self.__with_snack else 4].portions
                }
            },
            "nutrients": {
                "energy": {
                    "amount": f'{int(daily_energy)} kcal',
                    "ratio": round((daily_energy / self.__max_energy) * 100, 0)
                },
                "carbs": {
                    "amount": f'{int(round((daily_carbs_energy / self.__referential_unit_energy), 0))} g',
                    "ratio": round((daily_carbs_energy / daily_energy) * 100, 0)
                },
                "proteins": {
                    "amount": f'{int(round((daily_proteins_energy / self.__referential_unit_energy), 0))} g',
                    "ratio": round((daily_proteins_energy / daily_energy) * 100, 0)
                },
                "fats": {
                    "amount": f'{int(round((daily_fats_energy / self.__referential_fat_energy), 0))} g',
                    "ratio": round((daily_fats_energy / daily_energy) * 100, 0)
                },
                "fiber": {
                    "amount": f'{int(daily_fiber_amount)} g',
                    "ratio": round((daily_fiber_amount / self.__referential_fiber_amount) * 100, 0)
                }
            }
        }

        for food_name, food_data in response["foods"].items():
            en_food = EnNutriRecipes.query.filter_by(recipe_id=food_data["recipe_id"]).first()
            de_food = DeNutriRecipes.query.filter_by(recipe_id=food_data["recipe_id"]).first()

            if en_food:
                response["foods"][food_name]["en_name"] = en_food.name
                response["foods"][food_name]["en_url"] = en_food.url

            if de_food:
                response["foods"][food_name]["de_name"] = de_food.name
                response["foods"][food_name]["de_url"] = de_food.url

        return response

    @staticmethod
    def generate_menu() -> GeneratedMenu:
        """
        This method does take random breakfast, lunch, snack and dinner from DB.
        __tags are used to recognize food categories (breakfasts, snacks and lunches with dinners).

        :return list of NutriRecipes
        :rtype List[NutriRecipes]
        """

        breakfasts = CsNutriRecipes.query.filter(CsNutriRecipes.tags.contains("15")).all()
        lunches_and_dinners = CsNutriRecipes.query.filter(CsNutriRecipes.tags.contains("16")).all()
        snacks = CsNutriRecipes.query.filter(CsNutriRecipes.tags.contains("34")).all()

        return [
            breakfasts[random.randint(0, len(breakfasts)) - 1 if len(breakfasts) > 1 else 0],
            lunches_and_dinners[random.randint(0, len(lunches_and_dinners) - 1) if len(lunches_and_dinners) > 2 else 0],
            snacks[random.randint(0, len(snacks) - 1) if len(snacks) > 1 else 0],
            lunches_and_dinners[random.randint(0, len(lunches_and_dinners) - 1) if len(lunches_and_dinners) > 2 else 1]
            ]