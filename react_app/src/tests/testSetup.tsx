import React, { FC, Fragment, ReactElement } from 'react'
import { render, RenderOptions } from '@testing-library/react'


const AllTheProviders: FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <Fragment>
            {children}
        </Fragment>
    )
}

const customRender = (ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) =>
  render(ui, { wrapper: AllTheProviders, ...options })

// re-export everything
export * from '@testing-library/react'

// override render method
export { customRender as render }