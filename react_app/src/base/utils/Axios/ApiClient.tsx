import axios, { AxiosInstance } from "axios"
import { IFood, IDailyMenu } from "./types"


const apiClient = (): AxiosInstance => axios.create({
    baseURL: process.env.API_BASE_URL,
    timeout: 60000,
    headers: {
        "Content-Type": "application/json"
    },
    transformResponse: [(data) => {
        if (data) return JSON.parse(data)
    }]
})

const getDailyMenu = async (): Promise<IDailyMenu> => {
    const response = await apiClient().get<IDailyMenu>("/menu")
    return response.data
}

const getRecipe = async (id: number): Promise<IFood> => {
    if (!id || isNaN(id)) throw "Error"

    const response = await apiClient().get<IFood>(`/menu/${parseInt(String(id))}`)
    return response.data
}

const ApiClient = {
    getDailyMenu,
    getRecipe
}

export default ApiClient