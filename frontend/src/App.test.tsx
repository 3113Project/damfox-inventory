import "@testing-library/jest-dom/vitest"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { render, screen } from "@testing-library/react"
import { beforeEach, expect, test, vi } from "vitest"
import { App } from "./App"

beforeEach(() => {
  vi.restoreAllMocks()
})

test("shows application name and connected backend status", async () => {
  vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ software: "DAMFOX Inventory", version: "0.1.0", status: "online" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    }),
  )
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  render(<QueryClientProvider client={client}><App /></QueryClientProvider>)
  expect(screen.getByRole("heading", { name: "DAMFOX Inventory" })).toBeInTheDocument()
  expect(await screen.findByText("Backend online")).toBeInTheDocument()
})
