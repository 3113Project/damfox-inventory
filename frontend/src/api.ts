export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "http://localhost:18000").replace(/\/$/, "")

export interface BackendStatus { software: string; version: string; status: string }
export interface Product {
  id: number; sku: string; name: string; description: string | null
  manufacturer_code: string | null; category_id: number | null; vat_rate_id: number
  family_id: number | null; unit_of_measure_id: number | null; is_active: boolean
  created_at: string; updated_at: string
}
export interface Category { id: number; name: string; active: boolean }
export interface ProductFamily { id: number; name: string }
export interface VATRate { id: number; description: string; rate: string; active: boolean }
export interface UnitOfMeasure { id: number; code: string; name: string; symbol: string | null; is_active: boolean }
export interface ProductPayload {
  sku?: string; name: string; description: string | null; manufacturer_code: string | null
  category_id: number | null; vat_rate_id: number; family_id: number | null
  unit_of_measure_id: number; is_active: boolean
}

type ValidationIssue = { msg?: string }

export class ApiError extends Error {
  constructor(public status: number, public detail: unknown) {
    super(apiErrorMessage(status, detail))
  }
}

export function apiErrorMessage(status: number, detail: unknown): string {
  if (status === 404) return "La risorsa richiesta non esiste più."
  if (status === 409) return typeof detail === "string" ? detail : "Esiste già un elemento con questi dati."
  if (status === 422 && Array.isArray(detail)) {
    const messages = (detail as ValidationIssue[]).map((issue) => issue.msg).filter(Boolean)
    return messages.length ? `Controlla i dati inseriti: ${messages.join("; ")}` : "Controlla i dati inseriti."
  }
  if (typeof detail === "string") return detail
  return "Il server non ha completato la richiesta. Riprova."
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: init?.body ? { "Content-Type": "application/json", ...init.headers } : init?.headers,
  })
  if (!response.ok) {
    let detail: unknown
    try { detail = (await response.json() as { detail?: unknown }).detail } catch { detail = undefined }
    throw new ApiError(response.status, detail)
  }
  return response.json() as Promise<T>
}

export async function fetchBackendStatus(): Promise<BackendStatus> {
  return request("/")
}

export function fetchProducts(filters: { q?: string; familyId?: string; unitId?: string }): Promise<Product[]> {
  const params = new URLSearchParams()
  if (filters.q) params.set("q", filters.q)
  if (filters.familyId) params.set("family_id", filters.familyId)
  if (filters.unitId) params.set("unit_of_measure_id", filters.unitId)
  const query = params.toString()
  return request(`/products${query ? `?${query}` : ""}`)
}

export function fetchProduct(id: string): Promise<Product> {
  return request(`/products/${id}`)
}

export function createProduct(payload: ProductPayload): Promise<Product> {
  return request("/products", { method: "POST", body: JSON.stringify(payload) })
}

export function updateProduct(id: string, payload: ProductPayload): Promise<Product> {
  const mutablePayload = {
    name: payload.name,
    description: payload.description,
    manufacturer_code: payload.manufacturer_code,
    category_id: payload.category_id,
    vat_rate_id: payload.vat_rate_id,
    family_id: payload.family_id,
    unit_of_measure_id: payload.unit_of_measure_id,
    is_active: payload.is_active,
  }
  return request(`/products/${id}`, { method: "PATCH", body: JSON.stringify(mutablePayload) })
}

export async function fetchProductLookups() {
  const [categories, families, vatRates, units] = await Promise.all([
    request<Category[]>("/categories"),
    request<ProductFamily[]>("/product-families"),
    request<VATRate[]>("/vat-rates/"),
    request<UnitOfMeasure[]>("/unit-measures"),
  ])
  return { categories, families, vatRates, units }
}
