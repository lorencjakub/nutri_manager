interface INutrientData {
    amount: number,
    ratio: number
}

export interface INutrients {
    carbs: INutrientData,
    energy: INutrientData,
    fats: INutrientData,
    fiber: INutrientData,
    proteins: INutrientData
}

export interface IFood {
    id: number,
    name: string,
    portions: number,
    url: string,
    ingredients?: string,
    nutrients?: INutrients
}

export interface IDailyMenu {
    foods: {
        breakfast: IFood,
        lunch: IFood,
        snack?: IFood,
        dinner: IFood
    },
    iterations: number,
    nutrients: INutrients
}