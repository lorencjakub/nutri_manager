import React, { FC } from "react"
import Context from "./Context"
import { FormattedMessage } from "react-intl"


const ErrorProvider: FC<{ children: any }> = ({ children }) => {
    const errorList: { [key: string] : JSX.Element } = {
        "no_menu": <FormattedMessage id="api_errors.no_menu" defaultMessage="No generated menu does suit defined nutrient parameters. Please, try it again or change your parameters." />,
        "wrong_menu_inputs": <FormattedMessage id="api_errors.wrong_menu_inputs" defaultMessage="Wrong inputs" />
    }

    const parseErrorMessage = (error: string): JSX.Element => {
        var message: JSX.Element

        try {
            message = errorList[error]
        } catch {
            message = <FormattedMessage id="errors.unspecified" defaultMessage="An unspecified error" />
        }

        return message
    }
    
    return (
        <Context.Provider value={{ parseErrorMessage }}>
            {children}
        </Context.Provider>
    )
}

export default ErrorProvider