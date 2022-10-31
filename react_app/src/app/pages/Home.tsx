import React, { FC } from 'react'
import {
    Button,
    Paper,
    Grid,
    Typography
} from "@mui/material"
import { useNavigate } from 'react-router-dom'
import { useTheme as useMuiTheme } from "@mui/material/styles"
import { useIntl } from "react-intl"


const HomePage: FC<{}> = () => {
    const navigate = useNavigate()
    const theme = useMuiTheme()
    const intl = useIntl()

    return (
        <Paper
            elevation={0}
            style={{
                display: 'flex',
                overflow: 'hidden'
            }}
            sx={{
                px: 5,
                py: 2,
                m: 1,
                width: "100%",
                height: "100%",
                backgroundColor: "background.default",
                borderRadius: 5
            }}
        >
            <Grid
                data-testid="pages.homepage.container"
                container
                direction="column"
                spacing={1}
                justifyContent="center"
                alignItems="center"
            >
                <Grid
                    data-testid="pages.homepage.title"
                    item
                    style={{
                        display: "flex",
                        justifyContent: "center"
                    }}
                >
                    <Typography
                        variant="h6"
                        color="text.primary"
                    >
                        {intl.formatMessage({ id: "pages.homepage.title", defaultMessage: "Welcome!" })}
                    </Typography>
                </Grid>
                <Grid
                    data-testid="pages.homepage.about"
                    item
                    style={{
                        display: "flex",
                        justifyContent: "flex-start"
                    }}
                >
                    <Typography
                        variant="body1"
                        color="text.primary"
                    >
                        {intl.formatMessage({ id: "pages.homepage.about", defaultMessage: "There should be some important text probably. However, there is only one button, so just click it and let the app serve you :)" })}
                    </Typography>
                </Grid>
                <Grid
                    data-testid="pages.homepage.menu_button"
                    item
                    style={{
                        display: "flex",
                        justifyContent: "center"
                    }}
                >
                    <Button
                        onClick={() => navigate("/menu")}
                        variant="contained"
                        sx={{
                            backgroundColor: theme.palette.text.primary,
                            m: 3
                        }}
                    >
                        {intl.formatMessage({ id: "pages.homepage.menu_button", defaultMessage: "Get your daily menu" })}
                    </Button>
                </Grid>
                <Grid
                    data-testid="pages.homepage.warning"
                    item
                    style={{
                        display: "flex",
                        justifyContent: "flex-start"
                    }}
                >
                    <Typography
                        variant="body2"
                        color="text.primary"
                        sx={{
                            mt: 2
                        }}
                    >
                        {intl.formatMessage({ id: "pages.homepage.warning", defaultMessage: "This app should serve as the inspirating recipe generator and it does not substitute the nutrition expert!" })}
                    </Typography>
                </Grid>
            </Grid>
        </Paper>
    )
}

export default HomePage