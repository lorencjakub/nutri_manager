from .MenuGenerator import Menu
from distinct_types import Union, Tuple, GeneratedMenuData, RecipeData, List
from api.models import CsNutriRecipes


def generate_menu(**kwargs) -> Union[bool, Tuple[GeneratedMenuData, int]]:
    menu = Menu(**kwargs)
    return menu.create_menu() if menu.is_valid() else False


def generate_random_menu() -> Union[bool, Tuple[GeneratedMenuData, int]]:
    menu = Menu().create_menu(True)
    return menu


def generate_random_meal(meal_name: str, meal_ids: List[str]) -> Union[bool, RecipeData]:
    menu = Menu().create_menu(True, meal_name, meal_ids)
    return menu


def get_recipe(recipe_id: int) -> Union[RecipeData, bool]:
    recipe = CsNutriRecipes.get_by_id(recipe_id)

    if not recipe:
        return False

    recipe_data = {
        "id": recipe.id,
        "name": recipe.name,
        "url": recipe.url,
        "portions": recipe.portions,
        "nutrients": {
            "energy": round(float(recipe.energy), 0),
            "carbs": round(float(recipe.carbs), 0),
            "proteins": round(float(recipe.proteins), 0),
            "fats": round(float(recipe.fats), 0),
            "fiber": round(float(recipe.fiber), 0)
        }
    }

    return recipe_data
