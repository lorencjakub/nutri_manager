from api.models.models import NutriRecipes
import random
from datetime import datetime
from distinct_types import List, Type, GeneratedMenu, GeneratedMenuData, Tuple


class Menu:
    def __init__(self, proteins: float = 0, carbs: float = 0, fats: float = 0,
                 energy: float = 2000, tags: list = None) -> None:
        """Menu object class.

        It is able to create random menu according to defined optional parameters.
        :param energy: Maximum sum of energy for a day in kcal. Default value is 2000 kcal.
        :param proteins: Ratio of total energy from proteins to total energy from day in %. Default value is 40%.
        :param carbs: Ratio of total energy from carbs to total energy from day in %. Default value is 40%.
        :param fats: Ratio of total energy from fats to total energy from day in %. Default value is 20%.
        :param tags: Tags of specific food categories. Default value is None.
        :param with_snack: Boolean parameter. According this menu will be generated with or without the snack.
        Default value is True.
        """
        self.is_data_valid = self.__validate_parameters(proteins, carbs, fats, energy)

        if not self.is_data_valid:
            return

        self.max_energy = float(energy)
        self.proteins_ratio = float(proteins) if proteins != 0 else 40
        self.carbs_ratio = float(carbs) if carbs != 0 else 40
        self.fats_ratio = float(fats) if fats != 0 else 20
        self.tags = tags if tags else []

        self.with_snack: bool = True
        self.max_generate_count = 300
        self.start_time = datetime.now().timestamp()

        self.__balance_nutrients_ratios()

    @classmethod
    def __validate_parameters(cls, proteins: float = 0, carbs: float = 0, fats: float = 0, energy: float = 2000) -> bool:
        for p in [proteins, carbs, fats, energy]:
            if (isinstance(p, float) or str(p).isdigit()) and p >= 0:
                continue

            else:
                return False

        return True

    def is_valid(self):
        return self.is_data_valid

    def __start_timer(self):
        self.start_time = datetime.now().timestamp()

    def __balance_nutrients_ratios(self):
        sum_of_ratios = self.carbs_ratio + self.proteins_ratio + self.fats_ratio

        if sum_of_ratios <= 100:
            diff = 100 - sum_of_ratios
            self.carbs_ratio += diff / 3
            self.proteins_ratio += diff / 3
            self.fats_ratio += diff / 3

        else:
            self.carbs_ratio = round((self.carbs_ratio / sum_of_ratios) * 100, 0)
            self.proteins_ratio = round((self.proteins_ratio / sum_of_ratios) * 100, 0)
            self.fats_ratio = round((self.fats_ratio / sum_of_ratios) * 100, 0)

    def create_menu(self) -> Tuple[GeneratedMenuData, int]:
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
                } if self.with_snack else None,
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

        menu: List[Type[NutriRecipes]] = []
        day_energy: float = 0
        day_carbs_energy: float = 0
        day_proteins_energy: float = 0
        day_fats_energy: float = 0
        day_fiber_energy: float = 0

        while not parameters_fulfilled and generate_count < self.max_generate_count:
            menu = self.generate_menu()
            generate_count += 1

            day_energy = sum([float(food.energy) for food in menu])
            day_carbs_energy = sum([float(food.carbs) for food in menu]) * 4
            day_proteins_energy = sum([float(food.proteins) for food in menu]) * 4
            day_fats_energy = sum([float(food.fats) for food in menu]) * 9
            day_fiber_energy = sum([float(food.fiber) for food in menu])

            if 0.8 * self.max_energy <= day_energy <= self.max_energy \
                    and (day_carbs_energy / day_energy) * 100 <= self.carbs_ratio + 2.5 \
                    and (day_proteins_energy / day_energy) * 100 <= self.proteins_ratio + 2.5\
                    and (day_fats_energy / day_energy) * 100 <= self.fats_ratio + 2.5:
                parameters_fulfilled = True

        if not parameters_fulfilled:
            return "No generated menu does not suit defined nutrient parameters.\n" \
                   "Please, try it again or change your parameters.", 204

        return {
            "iterations": generate_count,
            "foods": {
                "breakfast": {
                    "id": menu[0].id,
                    "name": menu[0].name,
                    "url": menu[0].url,
                    "portions": menu[0].portions
                },
                "lunch": {
                    "id": menu[1].id,
                    "name": menu[1].name,
                    "url": menu[1].url,
                    "portions": menu[1].portions
                },
                "snack": {
                    "id": menu[2].id,
                    "name": menu[2].name,
                    "url": menu[2].url,
                    "portions": menu[2].portions
                } if self.with_snack else None,
                "dinner": {
                    "id": menu[3 if self.with_snack else 4].id,
                    "name": menu[3 if self.with_snack else 4].name,
                    "url": menu[3 if self.with_snack else 4].url,
                    "portions": menu[3 if self.with_snack else 4].portions
                }
            },
            "nutrients": {
                "energy": day_energy,
                "carbs": round((day_carbs_energy / day_energy) * 100, 0),
                "proteins": round((day_proteins_energy / day_energy) * 100, 0),
                "fats": round((day_fats_energy / day_energy) * 100, 0),
                "fiber": day_fiber_energy
            }
        }, 200

    @staticmethod
    def generate_menu() -> GeneratedMenu:
        """
        This method does take random breakfast, lunch, snack and dinner from DB.
        Tags are used to recognize food categories (breakfasts, snacks and lunches with dinners).

        :return list of NutriRecipes
        :rtype List[NutriRecipes]
        """

        breakfasts = NutriRecipes.query.filter(NutriRecipes.tags.contains("15")).all()
        lunches_and_dinners = NutriRecipes.query.filter(NutriRecipes.tags.contains("16")).all()
        snacks = NutriRecipes.query.filter(NutriRecipes.tags.contains("34")).all()

        return [
            breakfasts[random.randint(0, len(breakfasts)) - 1],
            lunches_and_dinners[random.randint(0, len(lunches_and_dinners) - 1)],
            snacks[random.randint(0, len(snacks) - 1)],
            lunches_and_dinners[random.randint(0, len(lunches_and_dinners) - 1)]
            ]
