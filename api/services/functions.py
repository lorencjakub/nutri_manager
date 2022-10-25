from .MenuGenerator import Menu
from distinct_types import Union, Tuple, GeneratedMenuData, RecipeData
from api.models import NutriRecipes


def generate_menu(**kwargs) -> Union[bool, Tuple[GeneratedMenuData, int]]:
    menu = Menu(**kwargs)
    return menu.create_menu() if menu.is_valid() else False


def get_recipe(recipe_id: int) -> Union[RecipeData, bool]:
    recipe = NutriRecipes.get_by_id(recipe_id)

    if not recipe:
        return False

    recipe_data = {
        "id": recipe.id,
        "name": recipe.name,
        "url": recipe.url,
        "portions": recipe.portions,
        "nutrients": {
            "energy": recipe.energy,
            "carbs": round(float(recipe.carbs), 0),
            "proteins": round(float(recipe.proteins), 0),
            "fats": round(float(recipe.fats), 0),
            "fiber": round(float(recipe.fiber), 0)
        },
        "ingredients": recipe.ingredients
    }

    return recipe_data
