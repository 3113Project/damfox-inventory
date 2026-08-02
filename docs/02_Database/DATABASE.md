# Modello dati

## Scopo

Descrivere lo stato reale delle entità persistenti e la direzione del modello dati senza anticipare la progettazione definitiva di tutte le tabelle.

## Principi del modello dati

- PostgreSQL è il database previsto.
- SQLAlchemy rappresenta i modelli ORM.
- Alembic è la fonte di verità prevista per le modifiche strutturali.
- Le relazioni devono rispettare BUSINESS_RULES.md e mantenere tracciabilità dei dati rilevanti.

## Entità implementate

### VATRate

Il modello `VATRate` è implementato con `id`, `description` univoca, `rate`, `active`, `created_at` e `updated_at`. Il CRUD REST è disponibile e la migrazione della baseline è coerente con il modello.

### User

Il modello `User` è presente con username univoco, password, flag `is_admin`, `created_at` e `updated_at`. La migrazione della baseline crea la tabella in modo coerente. Non sono presenti API o autenticazione.

### BaseModel

Il modello base fornisce `id`, `created_at` e `updated_at` ai modelli che lo ereditano.

## Entità in sviluppo

### Category

Nel working tree esiste un modello per categorie gerarchiche con `name`, `description`, `parent_id`, `active`, vincolo di unicità per padre/nome e relazione padre-figli. Non è integrato nella metadata, non ha migrazione, service o router funzionanti e contiene riferimenti a moduli non presenti.

## Entità pianificate

- Product, ProductFamily, Barcode, Image, Document, UnitOfMeasure e Packaging.
- Supplier, ProductSupplier e PurchasePriceHistory.
- InventoryMovement e i dati necessari a giacenza, scorta minima e ubicazione.

## Relazioni principali

| Relazione | Stato |
| --- | --- |
| Category gerarchica (`parent_id`) | In sviluppo. |
| Product → VATRate | Pianificata; richiesta da BR-022. |
| Product → Category | Pianificata. |
| Product ↔ Supplier tramite ProductSupplier | Pianificata; il costo appartiene a questa relazione. |
| ProductSupplier → PurchasePriceHistory | Pianificata; lo storico non deve essere eliminato. |
| Product → InventoryMovement | Pianificata; necessaria alla tracciabilità del magazzino. |

## Regole invarianti

- Ogni prodotto avrà uno SKU univoco e immutabile.
- L'IVA appartiene al prodotto.
- Il prezzo di acquisto appartiene alla relazione prodotto-fornitore.
- Lo storico dei prezzi e delle vendite non deve essere eliminato.
- Il magazzino usa una sola unità di riferimento; le confezioni sono conversioni.

## Migrazioni

Alembic è l’unica fonte di verità dello schema. La baseline lineare crea prima
`users` e poi `vat_rates`; entrambe le tabelle includono ID, timestamp,
nullability e vincoli coerenti con i modelli ORM registrati in `app.models`.

`DATABASE_URL` proviene dalla configurazione applicativa anche durante le
migrazioni. La baseline è stata verificata su database vuoto, una seconda
esecuzione di `alembic upgrade head` è risultata idempotente e
`alembic check` non ha rilevato operazioni mancanti.

Category non è inclusa nella baseline.

## Decisioni aperte

> TODO: verificare con il maintainer se quantità, ubicazione e scorta minima debbano vivere direttamente in Product o in entità dedicate.

> TODO: verificare con il maintainer il modello definitivo per allegati, immagini e barcode.

## Documenti correlati

- [Architettura](../00_Project/ARCHITECTURE.md)
- [Regole di business](../03_Business/BUSINESS_RULES.md)
- [Decisioni](../05_Project_Management/DECISIONS.md)
