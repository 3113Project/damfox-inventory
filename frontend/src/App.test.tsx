import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { cleanup, fireEvent, render, screen } from "@testing-library/react"
import { MemoryRouter } from "react-router-dom"
import { afterEach, beforeEach, expect, test, vi } from "vitest"
import { App } from "./App"

function renderApp(path = "/") {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <MemoryRouter initialEntries={[path]}>
      <QueryClientProvider client={client}>
        <App />
      </QueryClientProvider>
    </MemoryRouter>,
  )
}

beforeEach(() => {
  vi.restoreAllMocks()
})
afterEach(() => {
  cleanup()
})


test("renders dashboard and connected backend status", async () => {
  vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ software: "DAMFOX Inventory", version: "0.1.0", status: "online" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    }),
  )
  renderApp()
  expect(screen.getByRole("heading", { name: "Dashboard" })).toBeInTheDocument()
  expect(await screen.findByText("DAMFOX Inventory risponde correttamente.")).toBeInTheDocument()
})

test("navigates to a clear product empty state", () => {
  vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"))
  renderApp()
  fireEvent.click(screen.getByRole("link", { name: /Apri prodotti/ }))
  expect(screen.getByRole("heading", { name: "Prodotti" })).toBeInTheDocument()
  expect(screen.getByRole("heading", { name: "Sezione in preparazione" })).toBeInTheDocument()
})
