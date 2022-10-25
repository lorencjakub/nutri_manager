import React, { FC } from 'react'
import { Button } from "@mui/material"
import { useQuery } from '@tanstack/react-query'
import ApiClient from '../../base/utils/Axios/ApiClient'


const DailyMenuPage: FC<{}> = () => {
    const {
        refetch: handleGenerateMenuClick
    } = useQuery(["menu"], async () => await ApiClient.getDailyMenu(), {
        retry: 1,
        enabled: false
    })

    const {
        refetch: handleRecipeClick
    } = useQuery(["recipe"], async () => await ApiClient.getRecipe(1), {
        retry: 1,
        enabled: false
    })

    return (
        <div>
            <h1>Hello, this is DAILY MENU!</h1>
            <Button
                onClick={() => handleGenerateMenuClick()}
            >
                Generate Menu
            </Button>
            <Button
                onClick={() => handleRecipeClick()}
            >
                Get Recipe
            </Button>
        </div>
    )
}

export default DailyMenuPage