export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "http://localhost:18000").replace(/\/$/, "")

export type BackendStatus = {
  software: string
  version: string
  status: string
}

export async function fetchBackendStatus(): Promise<BackendStatus> {
  const response = await fetch(`${API_BASE_URL}/`)
  if (!response.ok) {
    throw new Error(`Backend status request failed: ${response.status}`)
  }
  return response.json() as Promise<BackendStatus>
}
