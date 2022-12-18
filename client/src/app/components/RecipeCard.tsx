import React, { FC, useState } from "react"
import {
    Button,
    Paper,
    Typography,
    Grid
} from "@mui/material"
import { useTheme as useMuiTheme } from '@mui/material/styles'
import { IFood } from '../../base/utils/Axios/types'
import { useIntl, FormattedMessage } from "react-intl"
import { useLocale } from "../../base/Providers/Locales"
import WarningIcon from '@mui/icons-material/Warning'


const RecipeCard: FC<{ mealName: string, food: IFood }> = ({ mealName, food }) => {
    const theme = useMuiTheme()
    const intl = useIntl()
    const { locale } = useLocale()
    const [onlyCz, setOnlyCz] = useState<boolean>(false)
    
    const handleOpenRecipeClick = (url: string) => {
        window.open(url, "_blank", "noopener,noreferrer")
    }

    const mealNames: { [key: string] : string } = {
        breakfast: intl.formatMessage({ id: "containers.layout.content.recipe_card.breakfast", defaultMessage: "Breakfast" }),
        lunch: intl.formatMessage({ id: "containers.layout.content.recipe_card.lunch", defaultMessage: "Lunch" }),
        snack: intl.formatMessage({ id: "containers.layout.content.recipe_card.snack", defaultMessage: "Snack" }),
        dinner: intl.formatMessage({ id: "containers.layout.content.recipe_card.dinner", defaultMessage: "Dinner" }),
    }

    var localRecipeName = food[`${locale}_name` as keyof IFood]
    var localRecipeUrl = food[`${locale}_url` as keyof IFood]

    if (!localRecipeName || !localRecipeUrl) {
        localRecipeName = food.cs_name
        localRecipeUrl = food.cs_url

        if (!onlyCz) setOnlyCz(true)
    }

    return (
        <Paper
            elevation={1}
            key={`${mealName}_recipe_key`}
            style={{
                display: 'flex',
                overflow: 'hidden'
            }}
            sx={{
                px: 5,
                py: 2,
                m: 1,
                width: "95%",
                backgroundColor: "primary.dark",
                borderRadius: 5
            }}
        >
            <Grid
                data-testid={`containers.layout.content.recipe_card.${mealName}`}
                container
                direction="column"
            >
                <Typography
                    variant="h6"
                    color="text.primary"
                    noWrap
                    sx={{
                        mb: 1
                    }}
                >
                    {mealNames[mealName]}
                </Typography>
                <Typography
                    variant="body2"
                    color="text.secondary"
                >
                    {localRecipeName as string}
                </Typography>
                <Typography
                    variant="body2"
                    color="text.secondary"
                    noWrap
                >
                    <FormattedMessage
                        id="containers.layout.content.recipe_card.portions"
                        defaultMessage="Portions: {portions}"
                        values={{ portions: food.portions }}
                    />
                </Typography>
                <Button
                    variant="outlined"
                    data-testid="containers.layout.content.recipe_source_button"
                    onClick={() => handleOpenRecipeClick(localRecipeUrl as string)}
                    sx={{
                        borderColor: theme.palette.primary.light,
                        maxWidth: 120,
                        mt: 1
                    }}
                >
                    <Typography
                        variant="body2"
                        color="text.primary"
                        noWrap
                    >
                        {intl.formatMessage({ id: "containers.layout.content.recipe_card.recipe", defaultMessage: "Recipe" })}
                    </Typography>
                </Button>
                {(onlyCz && (locale !== "cs")) ? 
                    <Grid
                        data-testid={`containers.layout.content.recipe_card.${mealName}.only_cz`}
                        container
                        direction="column"
                        alignItems="center"
                        sx={{
                            mt: 3
                        }}
                    >
                        <WarningIcon />
                        <Typography
                            variant="body2"
                            color="error"
                            noWrap
                        >
                            {intl.formatMessage({ id: "containers.layout.content.recipe_card.only_cz", defaultMessage: "Sadly, this recipe exists in the database only in the czech version." })}
                        </Typography>
                    </Grid>
                    : null
                }
            </Grid>
        </Paper>
    )
}

export default RecipeCard