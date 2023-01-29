import axios, { AxiosInstance } from "axios"
import { IFormData } from "../types"
import { IFood, IDailyMenu } from "./types"


const apiClient = (): AxiosInstance => axios.create({
    baseURL: process.env.API_BASE_URL,
    timeout: 60000,
    headers: {
        "Content-Type": "application/json",
        "CorsTrigger": "cors"
    },
    transformResponse: [(data) => {
        if (data) return JSON.parse(data)
    }]
})


const getDailyMenu = async (data: IFormData): Promise<IDailyMenu> => {
    const response = await apiClient().post<IDailyMenu>("/menu", data)
    return response.data
}

const getRandomDailyMenu = async (): Promise<IDailyMenu> => {
    const response = await apiClient().get<IDailyMenu>("/random_menu")
    return response.data
}

const reloadMeal = async (foods: IDailyMenu["foods"], mealToReload: string, isRandom?: boolean): Promise<IDailyMenu> => {
    const response = await apiClient().post<IDailyMenu>("/reload_meal", { foods: foods, meal_to_reload: mealToReload })
    return response.data
}

const reloadRandomMeal = async (foods: IDailyMenu["foods"], mealToReload: string): Promise<IDailyMenu> => {
    var mealIds: number[] = []
    Object.entries(foods).map(([mealName, mealData]) => {
        if (mealName != mealToReload) mealIds.push(mealData.id)
    })

    const response = await apiClient().post<IDailyMenu>("/random_reload_meal", { meal_ids: mealIds, meal_to_reload: mealToReload })
    return response.data
}

const getRecipe = async (id: number): Promise<IFood> => {
    if (!id || isNaN(id)) throw "Error"

    const response = await apiClient().get<IFood>(`/menu/${parseInt(String(id))}`)
    return response.data
}

const ApiClient = {
    getDailyMenu,
    getRandomDailyMenu,
    reloadMeal,
    reloadRandomMeal,
    getRecipe
}

export default ApiClient