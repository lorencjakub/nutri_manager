import React, { FC, useEffect } from 'react'
import {
    Button,
    Paper,
    Typography,
    Grid,
    useMediaQuery
} from "@mui/material"
import { useQuery } from '@tanstack/react-query'
import ApiClient from '../../base/utils/Axios/ApiClient'
import {
    IFood,
    IDailyMenu
} from '../../base/utils/Axios/types'
import { AxiosError } from 'axios'
import RecipeCard from '../components/RecipeCard'
import NutrientsTable from '../components/NutrientTable'
import { useTheme as useMuiTheme } from '@mui/material/styles'
import { useIntl } from "react-intl"
import ProcessingBackdrop from '../components/ProcessingBackdrop'
import { useDailyMenu } from '../Providers/DailyMenu'


const NewMenuButton: FC<{}> =()=> {
    const { setFetchedMenu, setIsFetching } = useDailyMenu()
    const theme = useMuiTheme()
    const intl = useIntl()

    const {
        refetch: handleGenerateMenuClick,
        fetchStatus: generatingMenu
    } = useQuery<IDailyMenu, AxiosError>(
        ["query_daily_menu"],
        async () => await ApiClient.getDailyMenu(),
        {
            retry: 0,
            cacheTime: 0,
            enabled: false,
            onSuccess: (data) => {
                setFetchedMenu && setFetchedMenu(data)
            }
        }
    )

    useEffect(() => {
        setIsFetching && setIsFetching((generatingMenu === "fetching"))
    }, [generatingMenu])

    return (
        <Button
            onClick={() => {
                setFetchedMenu && setFetchedMenu(null)
                handleGenerateMenuClick()
            }}
            data-testid="pages.daily_menu.info.buttons.generate_new_menu"
            sx={{
                backgroundColor: theme.palette.text.primary,
                maxWidth: 160,
                m: 2
            }}
        >
            <Typography
                variant="body2"
                color="primary.dark"
                noWrap
            >
                {intl.formatMessage({ id: "pages.daily_menu.info.buttons.generate_new_menu", defaultMessage: "New Menu" })}
            </Typography>
        </Button>
    )
} 

const DailyMenuInfo: FC<{}> =() => {
    const intl = useIntl()

    return (
        <React.Fragment>
            <Grid
                data-testid="pages.daily_menu.info"
                item
                xs={10}
                justifyContent="center"
                alignItems="center"
                style={{
                    display: 'flex',
                    overflow: 'hidden',
                    flexDirection: "column"
                }}
                sx={{
                    backgroundColor: "background.default"
                }}
            >
                <Grid
                    data-testid="pages.daily_menu.info.title"
                    item
                    xs={10}
                    style={{
                        display: 'flex',
                        overflow: 'hidden',
                        flexDirection: "column",
                        justifyItems: "flex-start"
                    }}
                    sx={{
                        backgroundColor: "background.default"
                    }}
                >
                    <Typography
                        variant="h4"
                        color="text.primary"
                        noWrap
                    >
                        {intl.formatMessage({ id: "pages.daily_menu.info.title", defaultMessage: "Daily Menu Generator" })}
                    </Typography>
                </Grid>
                <Grid
                    data-testid="pages.daily_menu.info.description"
                    item
                    xs={10}
                    style={{
                        display: 'flex',
                        overflow: 'hidden',
                        flexDirection: "column",
                        justifyItems: "flex-start"
                    }}
                    sx={{
                        backgroundColor: "background.default"
                    }}
                >
                    <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                            my: 2
                        }}
                    >
                        {intl.formatMessage({
                            id: "pages.daily_menu.info.description.generator",
                            defaultMessage: "This tool generates random menu in loop until all conditions are fulfilled. Default conditions are:"
                        })}
                    </Typography>
                    <Typography
                        variant="body2"
                        color="text.secondary"
                    >
                        {intl.formatMessage({
                            id: "pages.daily_menu.info.description.first_condition",
                            defaultMessage: "Summ of daily energy is between 80% and 100% of maximum allowed energy for a day (default maximum energy value is 2000 kcal)."
                        })}
                    </Typography>
                    <Typography
                        variant="body2"
                        color="text.secondary"
                    >
                        {intl.formatMessage({
                            id: "pages.daily_menu.info.description.second_condition",
                            defaultMessage: "Ratios of fats, proteins and carbs are less or equal of maximum allowed ratio +2.5% tolerance (default ratios are 40% for both of proteins and carbs and 20% for fats)."
                        })}
                    </Typography>
                    <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                            my: 2
                        }}
                    >
                        {intl.formatMessage({
                            id: "pages.daily_menu.info.description.ratios",
                            defaultMessage: "An error message will appear if conditions are not fulfilled in allowed count of iterations (300 by default). Then you can try generate menu again."
                        })}
                    </Typography>
                    <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                            my: 2
                        }}
                    >
                        {intl.formatMessage({
                            id: "pages.daily_menu.info.description.session",
                            defaultMessage: "Generated menu will be here for you until you will close this browser tab or generate a new menu."
                        })}
                    </Typography>
                </Grid>
                <Grid
                    data-testid="pages.daily_menu.info.buttons"
                    item
                    justifyItems="center"
                    style={{
                        display: 'flex',
                        flexDirection: "row"
                    }}
                    sx={{
                        backgroundColor: "background.default"
                    }}
                >
                    <NewMenuButton />
                </Grid>
            </Grid>
        </React.Fragment>
    )
}

const DailyMenuData: FC<{}> =() => {
    const intl = useIntl()
    const theme = useMuiTheme()
    const { fetchedMenu } = useDailyMenu()
    const isLarge = useMediaQuery(theme.breakpoints.up('lg'))

    return (
        <React.Fragment>
            <Grid
                data-testid="pages.daily_menu.meals"
                item
                xs={8}
                lg={5}
                justifyContent="center"
                alignItems="center"
                style={{
                    display: 'flex',
                    overflow: 'hidden',
                    flexDirection: "column"
                }}
                sx={{
                    backgroundColor: "background.default"
                }}
            >
                <Typography
                    variant="h5"
                    color="text.primary"
                    noWrap
                    sx={{
                        m: 1
                    }}
                >
                    {intl.formatMessage({ id: "pages.daily_menu.meals.title", defaultMessage: "Here is your menu for today. Enjoy!" })}
                </Typography>
                {fetchedMenu?.foods && Object.entries(fetchedMenu?.foods).map(([mealName, food]: [string, IFood]) => {
                    return (
                        <RecipeCard
                            mealName={mealName}
                            food={food}
                            key={mealName}
                        />
                    )
                })}
            </Grid>
            <Grid
                data-testid="pages.daily_menu.nutrients_table"
                item
                xs={8}
                lg={5}
                justifyContent="center"
                alignItems="center"
                style={{
                    display: 'flex',
                    overflow: 'hidden',
                    flexDirection: "column"
                }}
                sx={{
                    backgroundColor: "background.default"
                }}
            >
                <Typography
                    variant="h5"
                    color="text.primary"
                    noWrap
                    sx={{
                        m: 1,
                        mt: (isLarge) ? 1 : 5
                    }}
                >
                    {intl.formatMessage({ id: "pages.daily_menu.nutrients_table.title", defaultMessage: "Nutrients table for this day" })}
                </Typography>
                {
                    (!fetchedMenu?.nutrients) ? null:
                    <NutrientsTable nutrients={fetchedMenu?.nutrients} tableName="daily_menu" />
                }
                
                <Typography
                    variant="body2"
                    color="text.primary"
                    sx={{
                        m: 1,
                        px: 5
                    }}
                >
                    {intl.formatMessage({ id: "pages.daily_menu.nutrients_table.amount_note", defaultMessage: "Ratio of energy is calculated with refferency value 2000 kcal, the refferency value for fiber is 30 g." })}
                </Typography>
                <NewMenuButton />
            </Grid>
        </React.Fragment>
    )
}

const DailyMenuPage: FC<{}> = () => {
    const intl = useIntl()
    const theme = useMuiTheme()
    const isLarge = useMediaQuery(theme.breakpoints.up('lg'))
    const { fetchedMenu, isFetching } = useDailyMenu()

    var processingMessages = [
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.chopping_vegetable", defaultMessage: "Chopping vegetable..." }),
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.pepper", defaultMessage: "Little black pepper..." }),
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.not_little_not_much", defaultMessage: "Not too little and not too much - that's important!" }),
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.listers_sandwich", defaultMessage: "Triple fried egg, chilli, chutney sandwich - inspired by reading a book on bacterialogical warfare." }),
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.kebab_diablo", defaultMessage: "Shami kebab diablo - it's like eating molten lava." }),
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.that_hot", defaultMessage: "Do you really like them that hot sir?" }),
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.taters", defaultMessage: "What's taters, precious? What's taters, eh?" }),
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.lembas", defaultMessage: "Lembas bread. One small bite will fill the stomach of a grown man." }),
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.pea_soup", defaultMessage: "If you have pea soup, make sure you eat it before it eats you." }),
        intl.formatMessage({ id: "containers.layout.content.processing_backdrop.messages.white_wolf", defaultMessage: "White wolf, did you eat Red Riding Hood?" })
    ]

    const shuffleMessages = (messages: string[]): string[] => {
        let currentIndex = messages.length, randomIndex

        while (currentIndex != 0) {
            randomIndex = Math.floor(Math.random() * currentIndex)
            currentIndex--

            [messages[currentIndex], messages[randomIndex]] = [
            messages[randomIndex], messages[currentIndex]]
        }

        return messages
    }

    return (
        <Paper
            elevation={0}
            sx={{ m: 2, p: 2 }}
        >
            <Grid
                data-testid="pages.daily_menu"
                container
                spacing={1}
                justifyContent="center"
                alignItems={(isLarge) ? "flex-start" : "center"}
                direction={(isLarge) ? "row" : "column"}
                style={{
                    display: 'flex',
                    overflow: 'hidden'
                }}
                sx={{
                    backgroundColor: "background.default"
                }}
            >
                {(!fetchedMenu) ? <DailyMenuInfo /> : <DailyMenuData />}
            </Grid>
            {(!isFetching) ? null :
                <ProcessingBackdrop
                    messages={shuffleMessages(processingMessages)}
                />
            }
        </Paper>
    )
}

export default DailyMenuPage