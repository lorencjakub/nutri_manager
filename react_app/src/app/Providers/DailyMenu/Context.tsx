import React from "react"
import { IDailyMenu } from '../../../base/utils/Axios/types'


interface IDailyMenuContext {
    fetchedMenu: IDailyMenu | null,
    setFetchedMenu?: (data: IDailyMenu | null) => void,
    isFetching: boolean,
    setIsFetching?: (isFetching: boolean) => void
}

const DailyMenuContext = React.createContext<Partial<IDailyMenuContext>>({
    fetchedMenu: undefined,
    isFetching: false
})

export default DailyMenuContext