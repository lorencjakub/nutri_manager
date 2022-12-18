from distinct_types import Union, GeneratedMenuData, RecipeData


def mock_get_menu(result: Union[bool, None] = None) -> Union[GeneratedMenuData, str]:
    test_menu = [
        {
            "foods": {
                "breakfast": {
                    "id": 1,
                    "portions": 1,
                    "cs_name": "Test breakfast cs",
                    "cs_url": "Test breakfast URL cs",
                    "en_name": "Test breakfast en",
                    "en_url": "Test breakfast URL en",
                    "de_name": "Test breakfast de",
                    "de_url": "Test breakfast URL de",
                    "recipe_id": 1
                },
                "lunch": {
                    "id": 2,
                    "portions": 2,
                    "cs_name": "Test lunch cs",
                    "cs_url": "Test lunch URL cs",
                    "en_name": "Test lunch en",
                    "en_url": "Test lunch URL en",
                    "de_name": "Test lunch de",
                    "de_url": "Test lunch URL de",
                    "recipe_id": 2
                },
                "dinner": {
                    "id": 3,
                    "portions": 3,
                    "cs_name": "Test dinner cs",
                    "cs_url": "Test dinner URL cs",
                    "en_name": "Test dinner en",
                    "en_url": "Test dinner URL en",
                    "de_name": "Test dinner de",
                    "de_url": "Test dinner URL de",
                    "recipe_id": 3
                },
                "snack": {
                    "id": 4,
                    "portions": 4,
                    "cs_name": "Test snack cs",
                    "cs_url": "Test snack URL cs",
                    "recipe_id": 4
                }
            },
            "iterations": 1,
            "nutrients": {
                "carbs": {
                    "amount": "160 g",
                    "ratio": 32.0
                },
                "energy": {
                    "amount": "2000 kcal",
                    "ratio": 100.0
                },
                "fats": {
                    "amount": "40 g",
                    "ratio": 18.0
                },
                "fiber": {
                    "amount": "40 g",
                    "ratio": 133.0
                },
                "proteins": {
                    "amount": "135 g",
                    "ratio": 27.0
                },
            }
        }
    ]

    def switch(res: Union[bool, None] = None) -> Union[GeneratedMenuData, str]:
        if res is True:
            return test_menu
        elif res is False:
            return False
        elif res is None:
            return None

    return switch(result)


def mock_get_recipe() -> RecipeData:
    return {
        "id": 1,
        "name": "Test breakfast cs",
        "nutrients": {
            "carbs": 40.0,
            "energy": 400.0,
            "fats": 15.0,
            "fiber": 10.0,
            "proteins": 40.0
        },
        "portions": 1,
        "url": "Test breakfast URL cs"
    }
