import React, { Suspense, lazy } from "react"
import CircularProgress from '@mui/material/CircularProgress'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { QueryClientProvider, NotistackProvider } from "../Providers"
import { CacheProvider } from '@emotion/react'
import createCache from '@emotion/cache'


const Layout = lazy(() => import("./Layout"))
const cache = createCache({
  key: "nutri-react-cache-key",
  nonce: process.env.NONCE || "rAnd0mNonce",
  prepend: true
})

const App = () => {
  return (
  <Suspense fallback={<CircularProgress />}>
    <CacheProvider value={cache}>
      <NotistackProvider>
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
      </NotistackProvider>
    </CacheProvider>
  </Suspense>
  )
}

export default App