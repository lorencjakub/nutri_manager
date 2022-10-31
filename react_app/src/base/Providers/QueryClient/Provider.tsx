import React, { FC, ReactNode } from "react"
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useSnackbar } from "notistack"
import { useErrors } from "../Errors"


const Provider: FC<{ children: ReactNode }> = ({ children }) => {
  const { enqueueSnackbar } = useSnackbar()
  const { parseErrorMessage } = useErrors()

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: Infinity,
        onError: (err: any) => {
          enqueueSnackbar(
            parseErrorMessage && parseErrorMessage(err?.response?.data),
            {
              variant: "error"
            }
          )
        }
      },
      mutations: {
        onError: (err: any) => {
          enqueueSnackbar(
            parseErrorMessage && parseErrorMessage(err?.response?.data),
            {
              variant: "error"
            }
          )
        }
      }
    },
  })
  
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

export default Provider