import { useQuery } from "@tanstack/react-query"
import { fetchBackendStatus } from "./api"
import "./styles.css"

export function App() {
  const status = useQuery({
    queryKey: ["backend-status"],
    queryFn: fetchBackendStatus,
    retry: 1,
  })

  return (
    <main className="page">
      <section className="status-card" aria-labelledby="app-title">
        <p className="eyebrow">Inventario semplice e affidabile</p>
        <h1 id="app-title">DAMFOX Inventory</h1>
        {status.isPending && <p role="status">Connessione al backend…</p>}
        {status.isError && <p className="status status--error" role="alert">Backend non raggiungibile</p>}
        {status.data && (
          <p className="status status--success" role="status">
            <span aria-hidden="true">●</span> Backend {status.data.status}
          </p>
        )}
      </section>
    </main>
  )
}
