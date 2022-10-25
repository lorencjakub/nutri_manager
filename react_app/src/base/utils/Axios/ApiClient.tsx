import axios, { AxiosInstance } from "axios"
import { IFood, IDailyMenu } from "./types"


const apiClient = (): AxiosInstance => axios.create({
    baseURL: process.env.API_BASE_URL,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json"
    },
    transformResponse: (data) => {
        if (data) JSON.parse(data)
    }
})

const getDailyMenu = async () => {
    const response = await apiClient().get<IDailyMenu>("/menu")
    return response
}

const getRecipe = async (id: number) => {
    if (!id || isNaN(id)) throw "Error"

    const response = await apiClient().get<IFood>(`/menu/${parseInt(String(id))}`)
    return response
}

const ApiClient = {
    getDailyMenu,
    getRecipe
}

export default ApiClient