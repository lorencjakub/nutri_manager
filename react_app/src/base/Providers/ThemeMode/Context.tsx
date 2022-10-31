import React from "react"


interface IThemeContext {
    themeMode?: string,
    toggleThemeMode?: () => void
}

const ThemeContext = React.createContext<Partial<IThemeContext>>({})

export default ThemeContext