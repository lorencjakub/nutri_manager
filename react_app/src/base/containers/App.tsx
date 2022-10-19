import React, { Suspense, lazy } from "react"
import CircularProgress from '@mui/material/CircularProgress'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { QueryClientProvider } from "../Providers"


const Layout = lazy(() => import("./Layout"))

const App = () => {
  return (
  <Suspense fallback={<CircularProgress />}>
    <QueryClientProvider>
      <BrowserRouter>
          <Routes>
              <Route
                  path="*"
                  element={
                      <Suspense fallback={<CircularProgress />}>
                          {<Layout />}
                      </Suspense>
                  }
              />
          </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  </Suspense>
  )
}

export default App