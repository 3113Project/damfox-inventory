import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { type FormEvent, useEffect, useState } from "react"
import { Link, useHistory, useParams } from "react-router-dom"
import {
  createProduct,
  fetchProduct,
  fetchProductLookups,
  type ProductPayload,
  updateProduct,
} from "../api"
import { Card, ErrorState, Input, LoadingState, PageHeader, Select } from "../components/ui"

type Values = {
  sku: string; name: string; description: string; manufacturerCode: string
  categoryId: string; vatRateId: string; familyId: string; unitId: string; isActive: boolean
}

const emptyValues: Values = {
  sku: "", name: "", description: "", manufacturerCode: "",
  categoryId: "", vatRateId: "", familyId: "", unitId: "", isActive: true,
}

export function ProductForm() {
  const { productId } = useParams<{ productId?: string }>()
  const editing = Boolean(productId)
  const history = useHistory()
  const queryClient = useQueryClient()
  const [values, setValues] = useState<Values>(emptyValues)
  const [validation, setValidation] = useState("")
  const lookups = useQuery({ queryKey: ["product-lookups"], queryFn: fetchProductLookups })
  const product = useQuery({
    queryKey: ["product", productId],
    queryFn: () => fetchProduct(productId!),
    enabled: editing,
  })

  useEffect(() => {
    if (!product.data) return
    // eslint-disable-next-line react-hooks/set-state-in-effect -- hydrate the editable draft after the API response
    setValues({
      sku: product.data.sku,
      name: product.data.name,
      description: product.data.description ?? "",
      manufacturerCode: product.data.manufacturer_code ?? "",
      categoryId: product.data.category_id ? String(product.data.category_id) : "",
      vatRateId: String(product.data.vat_rate_id),
      familyId: product.data.family_id ? String(product.data.family_id) : "",
      unitId: product.data.unit_of_measure_id ? String(product.data.unit_of_measure_id) : "",
      isActive: product.data.is_active,
    })
  }, [product.data])

  const mutation = useMutation({
    mutationFn: (payload: ProductPayload) => editing ? updateProduct(productId!, payload) : createProduct(payload),
    onSuccess: async (saved) => {
      await queryClient.invalidateQueries({ queryKey: ["products"] })
      queryClient.setQueryData(["product", String(saved.id)], saved)
      history.push(`/prodotti/${saved.id}`)
    },
  })

  function submit(event: FormEvent) {
    event.preventDefault()
    if (!values.sku.trim() || !values.name.trim() || !values.vatRateId || !values.unitId) {
      setValidation("Compila SKU, nome, aliquota IVA e unità di misura.")
      return
    }
    setValidation("")
    mutation.mutate({
      sku: values.sku.trim(),
      name: values.name.trim(),
      description: values.description.trim() || null,
      manufacturer_code: values.manufacturerCode.trim() || null,
      category_id: values.categoryId ? Number(values.categoryId) : null,
      vat_rate_id: Number(values.vatRateId),
      family_id: values.familyId ? Number(values.familyId) : null,
      unit_of_measure_id: Number(values.unitId),
      is_active: values.isActive,
    })
  }

  if (lookups.isPending || (editing && product.isPending)) return <LoadingState label="Caricamento modulo…" />
  if (lookups.isError || product.isError) return <ErrorState description={product.error?.message ?? "Impossibile preparare il modulo."} />

  const data = lookups.data
  const option = (id: number, label: string) => ({ value: String(id), label })

  return (
    <>
      <PageHeader
        title={editing ? "Modifica prodotto" : "Nuovo prodotto"}
        description={editing ? "Aggiorna i dati modificabili. Lo SKU resta protetto." : "Inserisci i dati richiesti dal catalogo."}
      />
      <Card className="form-card">
        <form className="product-form" onSubmit={submit}>
          <div className="form-grid">
            <Input
              label="SKU"
              required
              maxLength={64}
              value={values.sku}
              readOnly={editing}
              hint={editing ? "Lo SKU è immutabile e non può essere modificato." : "Identificativo interno univoco."}
              onChange={(event) => setValues({ ...values, sku: event.target.value })}
            />
            <Input label="Nome" required maxLength={200} value={values.name} onChange={(event) => setValues({ ...values, name: event.target.value })} />
            <Input label="Codice produttore" maxLength={100} value={values.manufacturerCode} onChange={(event) => setValues({ ...values, manufacturerCode: event.target.value })} />
            <Select
              label="Categoria"
              value={values.categoryId}
              options={[{ value: "", label: "Nessuna categoria" }, ...data.categories.map((item) => option(item.id, item.name))]}
              onChange={(event) => setValues({ ...values, categoryId: event.target.value })}
            />
            <Select
              label="Famiglia"
              value={values.familyId}
              options={[{ value: "", label: "Nessuna famiglia" }, ...data.families.map((item) => option(item.id, item.name))]}
              onChange={(event) => setValues({ ...values, familyId: event.target.value })}
            />
            <Select
              label="Aliquota IVA"
              required
              value={values.vatRateId}
              options={[{ value: "", label: "Seleziona aliquota" }, ...data.vatRates.map((item) => option(item.id, `${item.description} — ${item.rate}%`))]}
              onChange={(event) => setValues({ ...values, vatRateId: event.target.value })}
            />
            <Select
              label="Unità di misura"
              required
              value={values.unitId}
              options={[{ value: "", label: "Seleziona unità" }, ...data.units.map((item) => option(item.id, `${item.name}${item.symbol ? ` (${item.symbol})` : ""}`))]}
              onChange={(event) => setValues({ ...values, unitId: event.target.value })}
            />
            <label className="field field-wide" htmlFor="product-description">
              <span className="field-label">Descrizione</span>
              <textarea id="product-description" className="textarea" maxLength={2000} rows={5} value={values.description} onChange={(event) => setValues({ ...values, description: event.target.value })} />
            </label>
          </div>
          <label className="check-field">
            <input type="checkbox" checked={values.isActive} onChange={(event) => setValues({ ...values, isActive: event.target.checked })} />
            <span>Prodotto attivo</span>
          </label>
          {validation && <div className="error-state" role="alert">{validation}</div>}
          {mutation.isError && <ErrorState title="Salvataggio non riuscito" description={mutation.error.message} />}
          <div className="form-actions">
            <button className="button" disabled={mutation.isPending} type="submit">{mutation.isPending ? "Salvataggio…" : "Salva prodotto"}</button>
            <Link className="text-button" to={editing ? `/prodotti/${productId}` : "/prodotti"}>Annulla</Link>
          </div>
        </form>
      </Card>
    </>
  )
}
