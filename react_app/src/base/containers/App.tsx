import React, { Suspense, lazy } from "react"
import CircularProgress from '@mui/material/CircularProgress'


const Layout = lazy(() => import("./Layout"))

const App = () => {
    return (
      <Suspense fallback={<CircularProgress />}>
        <Layout />
      </Suspense>
    )
  }
  
  export default App