import React from "react"
import { render, screen, act, fireEvent, waitFor } from "../testSetup"
import RecipeCard from "../../app/components/RecipeCard"
import { messagesGetter } from "../../base/Providers/Locales/Provider"
import LocaleComponent from "../LocaleTestComponent"
import {
    mockedDailyMenuSuccessOnlyCs,
    mockedDailyMenuSuccessMultiLang
} from "../MockedApiValues"
import { IFood } from "../../base/utils/Axios/types"


beforeEach(() => {
    jest.clearAllMocks()
    document.body.innerHTML = ""
    localStorage.clear()
    sessionStorage.clear()
})

async function renderTest(mealName: string, data: IFood, locale: string = "cs") {
    localStorage.setItem("locale", locale)

    await act(async () => {
        render(
            <LocaleComponent locale={locale}>
                <RecipeCard
                    mealName={mealName}
                    food={data}
                />
            </LocaleComponent>
        )
    })

    const messages = messagesGetter(locale)

    expect(localStorage.getItem("locale")).toEqual(locale)
    expect(screen.getByText(messages[`containers.layout.content.recipe_card.${mealName}` as keyof typeof messages])).toBeInTheDocument()
    expect(screen.getByText(data[`${locale}_name` as keyof IFood] as string)).toBeInTheDocument()
    expect(screen.getByTestId("containers.layout.content.recipe_source_button")).toBeInTheDocument()
}

describe("Test of Recipe card rendering", () => {
    test("Breakfast - cs only recipe with cs locale", async () => {
        const menu = { ...mockedDailyMenuSuccessOnlyCs }

        await renderTest("breakfast", menu.foods.breakfast)
    })

    test("Lunch - cs only recipe with cs locale", async () => {
        const menu = { ...mockedDailyMenuSuccessOnlyCs }

        await renderTest("lunch", menu.foods.lunch)
    })

    test("Snack - cs only recipe with cs locale", async () => {
        const menu = { ...mockedDailyMenuSuccessOnlyCs }

        await renderTest("snack", menu.foods.snack as IFood)
    })

    test("Dinner - cs only recipe with cs locale", async () => {
        const menu = { ...mockedDailyMenuSuccessOnlyCs }

        await renderTest("dinner", menu.foods.dinner)
    })

    test("Card rendering - multi language recipe with non-cs locale", async () => {
        const menu = { ...mockedDailyMenuSuccessMultiLang }

        await renderTest("breakfast", menu.foods.breakfast, "en")
        
        const messages = messagesGetter("en")
        expect(screen.getByTestId("containers.layout.content.recipe_source_button")).toBeInTheDocument()
        expect(screen.queryByText(messages["containers.layout.content.recipe_card.only_cz"])).not.toBeInTheDocument()
        expect(screen.queryByTestId("WarningIcon")).not.toBeInTheDocument()
    })

    test("Card rendering - cs only recipe with non-cs locale", async () => {
        const menu = { ...mockedDailyMenuSuccessOnlyCs }

        await renderTest("breakfast", menu.foods.breakfast, "en")

        const messages = messagesGetter("en")
        expect(screen.getByTestId("containers.layout.content.recipe_source_button")).toBeInTheDocument()
        expect(screen.queryByTestId("WarningIcon")).not.toBeInTheDocument()
        expect(screen.queryByText(messages["containers.layout.content.recipe_card.only_cz"])).not.toBeInTheDocument()
    })
})