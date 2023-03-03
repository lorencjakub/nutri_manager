from api.models.models import CsNutriRecipes, EnNutriRecipes, DeNutriRecipes
import random
from datetime import datetime
from distinct_types import List, Type, GeneratedMenu, GeneratedMenuData, Union, Tuple, Dict
from sqlalchemy import or_, and_
import os


class Menu:
    def __init__(self, proteins: float = 40, carbs: float = 40, fats: float = 20,
                 energy: int = 2000, tags: Dict[str, List[str]] = None, with_snack: bool = True,
                 minimum_energy_check: bool = True, iterations: int = 300, random_menu: bool = False) -> None:
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

        self.__is_data_valid = self.__validate_parameters(energy, iterations, [proteins, carbs, fats])

        if not self.__is_data_valid:
            return

        self.__driver = os.environ.get("DB_DRIVERNAME", default="sqlite")

        self.__referential_unit_energy = 4
        self.__referential_fat_energy = 9
        self.__referential_fiber_amount = 30

        self.__max_energy = int(energy)
        self.__min_energy_check = minimum_energy_check
        self.__proteins_ratio = float(proteins)
        self.__carbs_ratio = float(carbs)
        self.__fats_ratio = float(fats)
        self.__tags = tags if tags else {}

        self.__with_snack: bool = with_snack
        self.__random_menu: bool = random_menu
        self.__max_generate_count = int(iterations)

        self.__start_time = datetime.now().timestamp()
        self.__balance_nutrients_ratios()

    @staticmethod
    def __validate_parameters(energy: int, iterations: int, args) -> bool:
        for p in [energy, iterations, *args]:
            if (isinstance(p, float) or str(p).isdigit()) and float(p) >= 0:
                continue

            else:
                return False

        if not (1200 <= int(energy) <= 3500) or not (1 <= int(iterations) <= 500):
            return False

        return True

    def is_valid(self) -> bool:
        return self.__is_data_valid

    def check_balanced_nutrients(self) -> Dict[str, float]:
        return {
            "carbs": self.__carbs_ratio,
            "proteins": self.__proteins_ratio,
            "fats": self.__fats_ratio
        }

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

    def create_menu(self, specific_meal: Union[str, None] = None,
                    meal_ids: Union[List[str], None] = None) -> Union[GeneratedMenuData, None]:
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

        satisfied: bool = False
        generate_count = 0
        self.__start_timer()

        menu: List[Type[CsNutriRecipes]] = []

        while not satisfied and generate_count < self.__max_generate_count:
            menu = self.generate_menu(specific_meal, meal_ids)

            if not menu:
                return None

            generate_count += 1

            satisfied = self.__is_menu_satisfying(menu)

        if not satisfied:
            return None

        daily_energy, daily_carbs_energy, daily_proteins_energy, daily_fats_energy, daily_fiber_amount = satisfied

        return self.__create_response(
            generate_count,
            menu,
            daily_energy,
            daily_carbs_energy,
            daily_proteins_energy,
            daily_fats_energy,
            daily_fiber_amount,
            specific_meal
        )

    def __create_response(
        self,
        generate_count,
        menu: List[Type[CsNutriRecipes]],
        daily_energy: float,
        daily_carbs_energy: float,
        daily_proteins_energy: float,
        daily_fats_energy: float,
        daily_fiber_amount: float,
        specific_meal: Union[str, None]
    ):
        response = {
            "iterations": generate_count,
            "foods": {},
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

        if not specific_meal:
            response["foods"] = {
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
                "dinner": {
                    "id": menu[2 if not self.__with_snack else 3].id,
                    "recipe_id": menu[2 if not self.__with_snack else 3].recipe_id,
                    "cs_name": menu[2 if not self.__with_snack else 3].name,
                    "cs_url": menu[2 if not self.__with_snack else 3].url,
                    "portions": menu[2 if not self.__with_snack else 3].portions
                }
            }

            if self.__with_snack:
                response["foods"]["snack"] = {
                    "id": menu[2].id,
                    "recipe_id": menu[2].recipe_id,
                    "cs_name": menu[2].name,
                    "cs_url": menu[2].url,
                    "portions": menu[2].portions
                }

        else:
            response["foods"] = {
                specific_meal: {
                    "id": menu[0].id,
                    "recipe_id": menu[0].recipe_id,
                    "cs_name": menu[0].name,
                    "cs_url": menu[0].url,
                    "portions": menu[0].portions
                }
            }

        for food_name, food_data in response["foods"].items():
            if food_name == "snack" and not food_data:
                continue

            en_food = EnNutriRecipes.query.filter_by(recipe_id=food_data["recipe_id"]).first()
            de_food = DeNutriRecipes.query.filter_by(recipe_id=food_data["recipe_id"]).first()

            if en_food:
                response["foods"][food_name]["en_name"] = en_food.name
                response["foods"][food_name]["en_url"] = en_food.url

            if de_food:
                response["foods"][food_name]["de_name"] = de_food.name
                response["foods"][food_name]["de_url"] = de_food.url

        return response

    def generate_menu(self, specific_meal: Union[str, None] = None, meal_ids: Union[List[str], None] = None,
                      tags: Union[List[int], None] = None) -> GeneratedMenu:
        """
        This method does take random breakfast, lunch, snack and dinner from DB.
        __tags are used to recognize food categories (breakfasts, snacks and lunches with dinners).

        :return list of NutriRecipes
        :rtype List[NutriRecipes]
        """

        meal_codes = {
            "breakfast": "15",
            "snack": "34",
            "lunch": "16",
            "dinner": "16"
        }

        if not specific_meal and not tags:
            breakfasts = self.__query_tagged_data([meal_codes["breakfast"]], "breakfast")
            lunches = self.__query_tagged_data([meal_codes["lunch"]], "lunch")
            snacks = self.__query_tagged_data([meal_codes["snack"]], "snack")
            dinners = self.__query_tagged_data([meal_codes["dinner"]], "dinner")

            if not breakfasts or not lunches or not snacks or not dinners:
                return False

            menu = [
                breakfasts[random.randint(0, len(breakfasts)) - 1 if len(breakfasts) > 1 else 0],
                lunches[random.randint(0, len(lunches) - 1) if len(lunches) > 1 else 0],
                snacks[random.randint(0, len(snacks) - 1) if len(snacks) > 1 else 0],
                dinners[random.randint(0, len(dinners) - 1) if len(dinners) > 1 else 0]
            ]

            if not self.__with_snack:
                del menu[2]

            return menu

        else:
            meal_set = self.__query_tagged_data([meal_codes[specific_meal]], specific_meal)

            if not meal_set:
                return False

            meals = [
                meal_set[random.randint(0, len(meal_set)) - 1 if len(meal_set) > 1 else 0],
            ]

            if meal_ids:
                for i in meal_ids:
                    meals.append(CsNutriRecipes.query.filter_by(id=i).first())

            return meals

    def __query_tagged_data(self, tags: List[str], meal_name: str) -> List[CsNutriRecipes]:
        queries = []

        if not self.__random_menu and f"{meal_name}_tags" in list(self.__tags.keys()):
            tags.extend(self.__tags[f"{meal_name}_tags"])

            for t in tags:
                substring = [
                    CsNutriRecipes.tags.contains(f'[{t}]'),
                    CsNutriRecipes.tags.contains(f'[{t},'),
                    CsNutriRecipes.tags.contains(f', {t}]'),
                    CsNutriRecipes.tags.contains(f', {t},')
                ]
                queries.append(or_(*substring))

        data = CsNutriRecipes.query.filter(and_(*queries)).all()

        return data

    def __is_menu_satisfying(self, menu) -> Union[bool, Tuple[float, float, float, float, float]]:
        daily_energy = float(sum([float(food.energy) for food in menu]))
        daily_carbs_energy = float(sum([float(food.carbs) for food in menu]) * 4)
        daily_proteins_energy = float(sum([float(food.proteins) for food in menu]) * 4)
        daily_fats_energy = float(sum([float(food.fats) for food in menu]) * 9)
        daily_fiber_amount = float(sum([float(food.fiber) for food in menu]))

        if self.__random_menu:
            return daily_energy, daily_carbs_energy, daily_proteins_energy, daily_fats_energy, daily_fiber_amount

        if self.__min_energy_check and daily_energy < 0.8 * self.__max_energy:
            return False

        if daily_energy <= self.__max_energy \
                and (daily_carbs_energy / daily_energy) * 100 <= self.__carbs_ratio + 2.5 \
                and (daily_proteins_energy / daily_energy) * 100 <= self.__proteins_ratio + 2.5 \
                and (daily_fats_energy / daily_energy) * 100 <= self.__fats_ratio + 2.5:
            return daily_energy, daily_carbs_energy, daily_proteins_energy, daily_fats_energy, daily_fiber_amount
