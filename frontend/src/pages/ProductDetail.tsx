import { useQuery } from "@tanstack/react-query"
import { Link, useParams } from "react-router-dom"
import { fetchProduct, fetchProductLookups } from "../api"
import { Badge, Card, ErrorState, LoadingState, PageHeader } from "../components/ui"

export function ProductDetail() {
  const { productId } = useParams<{ productId: string }>()
  const product = useQuery({ queryKey: ["product", productId], queryFn: () => fetchProduct(productId) })
  const lookups = useQuery({ queryKey: ["product-lookups"], queryFn: fetchProductLookups })

  if (product.isPending || lookups.isPending) return <LoadingState label="Caricamento prodotto…" />
  if (product.isError || lookups.isError) return <ErrorState description={product.error?.message ?? "Impossibile caricare il prodotto."} />

  const item = product.data
  const data = lookups.data
  const category = data.categories.find((entry) => entry.id === item.category_id)?.name ?? "Nessuna"
  const family = data.families.find((entry) => entry.id === item.family_id)?.name ?? "Nessuna"
  const vat = data.vatRates.find((entry) => entry.id === item.vat_rate_id)
  const unit = data.units.find((entry) => entry.id === item.unit_of_measure_id)

  return (
    <>
      <PageHeader
        title={item.name}
        description={`SKU ${item.sku}`}
        actions={<Link className="button button-link" to={`/prodotti/${item.id}/modifica`}>Modifica</Link>}
      />
      <Card className="detail-card">
        <div className="detail-status"><Badge tone={item.is_active ? "success" : "neutral"}>{item.is_active ? "Attivo" : "Inattivo"}</Badge></div>
        <dl className="detail-grid">
          <div><dt>SKU</dt><dd><code>{item.sku}</code></dd></div>
          <div><dt>Codice produttore</dt><dd>{item.manufacturer_code ?? "—"}</dd></div>
          <div><dt>Categoria</dt><dd>{category}</dd></div>
          <div><dt>Famiglia</dt><dd>{family}</dd></div>
          <div><dt>Aliquota IVA</dt><dd>{vat ? `${vat.description} (${vat.rate}%)` : "Non disponibile"}</dd></div>
          <div><dt>Unità di misura</dt><dd>{unit ? `${unit.name}${unit.symbol ? ` (${unit.symbol})` : ""}` : "Non disponibile"}</dd></div>
          <div className="detail-wide"><dt>Descrizione</dt><dd>{item.description ?? "Nessuna descrizione."}</dd></div>
        </dl>
      </Card>
      <Link className="back-link" to="/prodotti">← Torna ai prodotti</Link>
    </>
  )
}
