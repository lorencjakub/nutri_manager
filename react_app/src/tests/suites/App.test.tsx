import { render, screen, act, waitFor } from "../testSetup"
import App from "../../base/containers/App"


test("Test of App component render", async () => {
    await act(async () => {
        render(<App />)
    })

    expect(screen.getByTestId("containers.layout.content")).toBeInTheDocument()
    expect(screen.getByTestId("containers.layout.toolbar")).toBeInTheDocument()
})