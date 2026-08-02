import { useQuery } from "@tanstack/react-query"
import { type FormEvent, useState } from "react"
import { Link } from "react-router-dom"
import { fetchProductLookups, fetchProducts, type Product } from "../api"
import { Badge, Card, EmptyState, ErrorState, Input, LoadingState, PageHeader, Select } from "../components/ui"

type Filters = { q: string; familyId: string; unitId: string }
const emptyFilters: Filters = { q: "", familyId: "", unitId: "" }

function lookupName<T extends { id: number; name: string }>(items: T[], id: number | null) {
  return id ? items.find((item) => item.id === id)?.name ?? "Non disponibile" : "—"
}

function ProductTable({ products, lookups }: {
  products: Product[]
  lookups: Awaited<ReturnType<typeof fetchProductLookups>>
}) {
  return (
    <div className="table-wrap">
      <table className="product-table">
        <thead>
          <tr><th>SKU</th><th>Nome</th><th>Categoria</th><th>Famiglia</th><th>IVA</th><th>Unità</th><th>Stato</th><th><span className="sr-only">Azioni</span></th></tr>
        </thead>
        <tbody>
          {products.map((product) => {
            const vat = lookups.vatRates.find((item) => item.id === product.vat_rate_id)
            const unit = lookups.units.find((item) => item.id === product.unit_of_measure_id)
            return (
              <tr key={product.id}>
                <td data-label="SKU"><code>{product.sku}</code></td>
                <td data-label="Nome"><strong>{product.name}</strong></td>
                <td data-label="Categoria">{lookupName(lookups.categories, product.category_id)}</td>
                <td data-label="Famiglia">{lookupName(lookups.families, product.family_id)}</td>
                <td data-label="IVA">{vat ? `${vat.description} (${vat.rate}%)` : "Non disponibile"}</td>
                <td data-label="Unità">{unit ? unit.symbol ?? unit.name : "Non disponibile"}</td>
                <td data-label="Stato"><Badge tone={product.is_active ? "success" : "neutral"}>{product.is_active ? "Attivo" : "Inattivo"}</Badge></td>
                <td className="table-action"><Link to={`/prodotti/${product.id}`} aria-label={`Apri ${product.name}`}>Apri →</Link></td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export function ProductCatalog() {
  const [draft, setDraft] = useState<Filters>(emptyFilters)
  const [filters, setFilters] = useState<Filters>(emptyFilters)
  const products = useQuery({ queryKey: ["products", filters], queryFn: () => fetchProducts(filters) })
  const lookups = useQuery({ queryKey: ["product-lookups"], queryFn: fetchProductLookups })
  const hasFilters = Boolean(filters.q || filters.familyId || filters.unitId)

  function submit(event: FormEvent) {
    event.preventDefault()
    setFilters({ ...draft, q: draft.q.trim() })
  }

  function reset() {
    setDraft(emptyFilters)
    setFilters(emptyFilters)
  }

  return (
    <>
      <PageHeader
        title="Prodotti"
        description="Consulta, cerca e aggiorna il catalogo collegato al backend."
        actions={<Link className="button button-link" to="/prodotti/nuovo">Nuovo prodotto</Link>}
      />
      <Card className="filters-card">
        <form className="filters-form" onSubmit={submit}>
          <Input
            label="Cerca"
            value={draft.q}
            placeholder="SKU, nome, barcode, codice produttore…"
            onChange={(event) => setDraft({ ...draft, q: event.target.value })}
          />
          <Select
            label="Famiglia"
            value={draft.familyId}
            options={[{ value: "", label: "Tutte le famiglie" }, ...(lookups.data?.families ?? []).map((item) => ({ value: String(item.id), label: item.name }))]}
            onChange={(event) => setDraft({ ...draft, familyId: event.target.value })}
          />
          <Select
            label="Unità di misura"
            value={draft.unitId}
            options={[{ value: "", label: "Tutte le unità" }, ...(lookups.data?.units ?? []).map((item) => ({ value: String(item.id), label: item.name }))]}
            onChange={(event) => setDraft({ ...draft, unitId: event.target.value })}
          />
          <div className="filter-actions">
            <button className="button" type="submit">Applica filtri</button>
            {hasFilters && <button className="text-button" type="button" onClick={reset}>Azzera</button>}
          </div>
        </form>
      </Card>
      {(products.isPending || lookups.isPending) && <LoadingState label="Caricamento catalogo…" />}
      {(products.isError || lookups.isError) && <ErrorState description="Non è stato possibile caricare il catalogo. Verifica il backend e riprova." />}
      {products.data && lookups.data && products.data.length > 0 && <ProductTable products={products.data} lookups={lookups.data} />}
      {products.data && lookups.data && products.data.length === 0 && (
        <EmptyState
          title={hasFilters ? "Nessun risultato" : "Il catalogo è vuoto"}
          description={hasFilters ? "Modifica o azzera i filtri per ampliare la ricerca." : "Crea il primo prodotto per iniziare a popolare il catalogo."}
        />
      )}
    </>
  )
}
