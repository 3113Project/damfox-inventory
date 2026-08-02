import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react"
import { MemoryRouter } from "react-router-dom"
import { afterEach, expect, test, vi } from "vitest"
import { App } from "./App"

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
})

test("completes create, list, detail and edit flow", async () => {
  const lookups = {
    categories: [{ id: 1, name: "Ferramenta", active: true }],
    families: [{ id: 2, name: "Viteria" }],
    vats: [{ id: 3, description: "IVA ordinaria", rate: "22.00", active: true }],
    units: [{ id: 4, code: "PZ", name: "Pezzo", symbol: "pz", is_active: true }],
  }
  let products: Array<Record<string, unknown>> = []
  const json = (data: unknown, status = 200) => new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  })

  vi.spyOn(globalThis, "fetch").mockImplementation(async (input, init) => {
    const path = new URL(String(input)).pathname
    if (path === "/categories") return json(lookups.categories)
    if (path === "/product-families") return json(lookups.families)
    if (path === "/vat-rates/") return json(lookups.vats)
    if (path === "/unit-measures") return json(lookups.units)
    if (path === "/products" && (!init?.method || init.method === "GET")) return json(products)
    if (path === "/products" && init?.method === "POST") {
      const payload = JSON.parse(String(init.body)) as Record<string, unknown>
      const created = {
        ...payload,
        id: 10,
        created_at: "2026-08-02T00:00:00Z",
        updated_at: "2026-08-02T00:00:00Z",
      }
      products = [created]
      return json(created, 201)
    }
    if (path === "/products/10" && init?.method === "PATCH") {
      const payload = JSON.parse(String(init.body)) as Record<string, unknown>
      products[0] = { ...products[0], ...payload }
      return json(products[0])
    }
    if (path === "/products/10") return json(products[0])
    return json({ detail: "Not found" }, 404)
  })

  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  render(
    <MemoryRouter initialEntries={["/prodotti"]}>
      <QueryClientProvider client={client}><App /></QueryClientProvider>
    </MemoryRouter>,
  )

  expect(await screen.findByRole("heading", { name: "Il catalogo è vuoto" })).toBeInTheDocument()
  fireEvent.click(screen.getByRole("link", { name: "Nuovo prodotto" }))
  expect(await screen.findByRole("heading", { name: "Nuovo prodotto" })).toBeInTheDocument()

  fireEvent.change(screen.getByLabelText(/^SKU/), { target: { value: "VITE-001" } })
  fireEvent.change(screen.getByLabelText("Nome"), { target: { value: "Vite zincata" } })
  fireEvent.change(screen.getByLabelText("Aliquota IVA"), { target: { value: "3" } })
  fireEvent.change(screen.getByLabelText("Unità di misura"), { target: { value: "4" } })
  fireEvent.click(screen.getByRole("button", { name: "Salva prodotto" }))

  expect(await screen.findByRole("heading", { name: "Vite zincata" })).toBeInTheDocument()
  expect(screen.getByText("VITE-001")).toBeInTheDocument()
  fireEvent.click(screen.getByRole("link", { name: "Modifica" }))

  expect(await screen.findByRole("heading", { name: "Modifica prodotto" })).toBeInTheDocument()
  expect(screen.getByLabelText(/^SKU/)).toHaveAttribute("readonly")
  fireEvent.change(screen.getByLabelText("Nome"), { target: { value: "Vite zincata M6" } })
  fireEvent.click(screen.getByRole("button", { name: "Salva prodotto" }))

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: "Vite zincata M6" })).toBeInTheDocument()
  })
  expect(products[0].sku).toBe("VITE-001")

  fireEvent.click(screen.getByRole("link", { name: /Torna ai prodotti/ }))
  expect(await screen.findByText("Vite zincata M6")).toBeInTheDocument()
})
