import React from "react"


interface IErrorContext {
    parseErrorMessage: (error: string) => JSX.Element
}

const Context = React.createContext<Partial<IErrorContext>>({})

export default Context