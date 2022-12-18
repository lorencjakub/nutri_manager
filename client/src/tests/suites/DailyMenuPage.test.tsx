import React from "react"
import { render, screen, act, fireEvent, waitFor } from "../testSetup"
import DialyMenuPage from "../../app/pages/DailyMenu"
import { messagesGetter } from "../../base/Providers/Locales/Provider"
import LocaleComponent from "../LocaleTestComponent"
import ApiClient from "../../base/utils/Axios/ApiClient"
import {
    mockedDailyMenuSuccessOnlyCs,
    mockedDailyMenuSuccessMultiLang
} from "../MockedApiValues"
import { DailyMenuProvider } from "../../app/Providers/DailyMenu"


beforeEach(() => {
    jest.clearAllMocks()
    document.body.innerHTML = ""
    localStorage.clear()
    sessionStorage.clear()
})

async function renderTest(locale: string) {
    localStorage.setItem("locale", locale)

    await act(async () => {
        render(
            <LocaleComponent locale={locale}>
                <DailyMenuProvider>
                    <DialyMenuPage />
                </DailyMenuProvider>
            </LocaleComponent>
        )
    })

    expect(screen.getByTestId("pages.daily_menu.info")).toBeInTheDocument()
    const messages = messagesGetter(locale)

    expect(localStorage.getItem("locale")).toEqual(locale)
    expect(screen.getByText(messages["pages.daily_menu.info.title"])).toBeInTheDocument()
    expect(screen.getByText(messages["pages.daily_menu.info.description.generator"])).toBeInTheDocument()
    expect(screen.getByText(messages["pages.daily_menu.info.description.first_condition"])).toBeInTheDocument()
    expect(screen.getByText(messages["pages.daily_menu.info.description.second_condition"])).toBeInTheDocument()
    expect(screen.getByText(messages["pages.daily_menu.info.description.ratios"])).toBeInTheDocument()
    expect(screen.getByText(messages["pages.daily_menu.info.description.session"])).toBeInTheDocument()
    expect(screen.getByText(messages["pages.daily_menu.info.buttons.generate_new_menu"])).toBeInTheDocument()

    expect(screen.queryByTestId("pages.daily_menu.meals")).not.toBeInTheDocument()
    expect(screen.queryByTestId("containers.layout.content.daily_menu.nutrients_table")).not.toBeInTheDocument()
}

describe("Test of DailyMenuPage render", () => {
    test("Initial render test - cs", async () => {
        await renderTest("cs")
    })

    test("Initial render test - en", async () => {
        await renderTest("en")
    })

    test("Initial render test - de", async () => {
        await renderTest("de")
    })
})

describe("Test of DailyMenuPage functionalities", () => {
    test("Menu generating", async () => {
        jest.spyOn(ApiClient, "getDailyMenu").mockResolvedValue(mockedDailyMenuSuccessOnlyCs)

        render(
            <LocaleComponent>
                <DailyMenuProvider>
                    <DialyMenuPage />
                </DailyMenuProvider>
            </LocaleComponent>
        )
    
        const button = screen.getByTestId("pages.daily_menu.info.buttons.generate_new_menu")
        if (!button) throw Error("Button not found")
        waitFor(() => fireEvent.click(button as HTMLButtonElement))
        expect(ApiClient.getDailyMenu).toBeCalled()
    })
})