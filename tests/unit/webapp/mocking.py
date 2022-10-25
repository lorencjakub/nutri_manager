from distinct_types import Union, GeneratedMenuData, RecipeData


def mock_get_menu(result: Union[bool, None] = None) -> Union[GeneratedMenuData, str]:
    test_menu = [
        {
            "foods": {
                "breakfast": {
                    "id": 1,
                    "name": "Test Breakfast",
                    "portions": 1,
                    "url": "Test Breakfast URL"
                },
                "dinner": {
                    "id": 2,
                    "name": "Test Dinner",
                    "portions": 2,
                    "url": "Test Dinner URL"
                },
                "lunch": {
                    "id": 3,
                    "name": "Test Lunch",
                    "portions": 3,
                    "url": "Test Lunch URL"
                },
                "snack": {
                    "id": 4,
                    "name": "Test Snack",
                    "portions": 4,
                    "url": "Test Snack URL"
                }
            },
            "iterations": 1,
            "nutrients": {
                "carbs": 34,
                "energy": 2000,
                "fats": 33,
                "fiber": 20,
                "proteins": 33
            }
        }
    ]

    def switch(res: Union[bool, None] = None) -> Union[GeneratedMenuData, str]:
        if res is True:
            return test_menu
        elif res is False:
            return False
        elif res is None:
            return "No generated menu does not suit defined nutrient parameters. " \
                   "Please, try it again or change your parameters."

    return switch(result)


def mock_get_recipe() -> RecipeData:
    return {
        "id": 1,
        "ingredients": "Test Ingredients",
        "name": "Test Recipe",
        "nutrients": {
            "carbs": 34,
            "energy": 2000,
            "fats": 33,
            "fiber": 20,
            "proteins": 33
        },
        "portions": 2,
        "url": "Test Recipe URL"
    }