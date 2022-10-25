import React, { FC, ReactNode } from "react"
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useSnackbar } from "notistack"


const Provider: FC<{ children: ReactNode }> = ({ children }) => {
  const { enqueueSnackbar } = useSnackbar()

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: Infinity,
        onError: (err: any) => {
          enqueueSnackbar(
            err?.response?.data || "Nespecifikovaná chyba",
            {
              variant: "error"
            }
          )
        }
      },
      mutations: {
        onError: (err: any) => {
          enqueueSnackbar(
            err?.response?.data || "Nespecifikovaná chyba",
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