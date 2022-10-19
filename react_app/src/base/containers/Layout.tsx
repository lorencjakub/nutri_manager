import React, { FC, Suspense, lazy } from 'react'
import { CircularProgress, Grid } from '@mui/material'
import { useRoutes } from 'react-router-dom'
import routes from '../../app/utils/routes'


const NotFoundPage = lazy(() => import("../../app/pages/NotFound"))

export const Layout: FC<{}> = () => {
  return (
      <div style={{ display: 'flex', flexDirection: "column", backgroundColor: "green", margin: 30, height: "calc(100vh - 60px)" }}>
          <Suspense fallback={<CircularProgress />}>
              <Grid
                  data-testid="containers.layout.toolbar"
                  container
                  spacing={1}
                  justifyContent="center"
                  alignItems="center"
                  direction="row"
                  style={{
                      height: 85,
                      display: 'flex',
                      overflow: 'hidden',
                      backgroundColor: "red",
                      margin: 10,
                      maxWidth: "calc(100% - 20px)"
                  }}
              >
                  <h1>TOOLBAR</h1>
              </Grid>
              <Grid
                  data-testid="containers.layout.content"
                  container
                  spacing={1}
                  justifyContent="center"
                  alignItems="center"
                  direction="row"
                  style={{
                      height: 'calc(100% - 85px)',
                      display: 'flex',
                      overflow: 'hidden',
                      backgroundColor: "red",
                      margin: 10,
                      maxWidth: "calc(100% - 20px)"
                  }}
              >
                <Suspense fallback={<CircularProgress />}>
                    {useRoutes([...routes]) || <NotFoundPage />}
                </Suspense>
              </Grid>
          </Suspense>
      </div>
  )
}

export default Layout