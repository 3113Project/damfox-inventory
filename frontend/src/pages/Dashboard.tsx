import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router-dom"
import { fetchBackendStatus } from "../api"
import { Badge, Card, ErrorState, LoadingState, PageHeader } from "../components/ui"

const shortcuts = [
  { to: "/prodotti", label: "Apri prodotti", detail: "Consulta il catalogo quando sarà disponibile." },
  { to: "/categorie", label: "Vai alle categorie", detail: "Accedi alla struttura del catalogo." },
  { to: "/unita-di-misura", label: "Unità di misura", detail: "Raggiungi l'anagrafica delle unità." },
]

export function Dashboard() {
  const status = useQuery({
    queryKey: ["backend-status"],
    queryFn: fetchBackendStatus,
    retry: 1,
  })

  return (
    <>
      <PageHeader
        title="Dashboard"
        description="Il punto di partenza per gestire il catalogo DAMFOX."
        actions={<Badge tone="neutral">Versione iniziale</Badge>}
      />
      <div className="dashboard-grid">
        <Card className="service-card">
          <div className="card-heading">
            <div>
              <p className="section-label">Stato servizi</p>
              <h2>Connessione backend</h2>
            </div>
            {status.data && <Badge tone="success">Operativo</Badge>}
          </div>
          {status.isPending && <LoadingState label="Verifica del backend…" />}
          {status.isError && (
            <ErrorState
              title="Backend non raggiungibile"
              description="Controlla che lo stack Docker Compose sia avviato."
            />
          )}
          {status.data && (
            <p className="service-message" role="status">
              <span className="status-dot" aria-hidden="true" />
              {status.data.software} risponde correttamente.
            </p>
          )}
        </Card>

        <Card>
          <p className="section-label">Scorciatoie</p>
          <h2>Esplora il workspace</h2>
          <div className="shortcut-list">
            {shortcuts.map((shortcut) => (
              <Link className="shortcut" key={shortcut.to} to={shortcut.to}>
                <span><strong>{shortcut.label}</strong><small>{shortcut.detail}</small></span>
                <span aria-hidden="true">→</span>
              </Link>
            ))}
          </div>
        </Card>
      </div>
    </>
  )
}
