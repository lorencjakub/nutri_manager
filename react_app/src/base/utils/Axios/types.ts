interface INutrients {
    carbs: number,
    energy: number,
    fats: number,
    fiber: number,
    proteins: number
}

export interface IFood {
    id: number,
    name: string,
    portions: number,
    url: number,
    ingredients?: string,
    nutrients?: INutrients,
    procedure?: string
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