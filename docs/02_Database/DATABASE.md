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

Il modello `VATRate` è implementato con `id`, `description` univoca fino a 50 caratteri, `rate`, `active`, `created_at` e `updated_at`. Il campo `rate` accetta valori da `0.00` a `100.00` inclusi, con massimo due decimali, secondo DECISION-0004. Il vincolo è applicato sia dagli schemi API sia da un `CHECK` PostgreSQL. Il CRUD usa PATCH per gli aggiornamenti parziali e dispone di test automatici.

### User

Il modello `User` è presente con username univoco, password, flag `is_admin`, `created_at` e `updated_at`. La migrazione della baseline crea la tabella in modo coerente. Non sono presenti API o autenticazione.

### BaseModel

Il modello base fornisce `id`, `created_at` e `updated_at` ai modelli che lo ereditano.

### ProductFamily

`ProductFamily` organizza facoltativamente i prodotti senza influenzare IVA, prezzi, fornitori o magazzino. Il nome è univoco in forma normalizzata e una famiglia usata non può essere eliminata.

### Product

Il modello `Product` è implementato con SKU immutabile, nome, descrizione facoltativa, Category facoltativa, VAT obbligatoria, stato attivo e timestamp. Lo SKU è univoco senza distinzione tra maiuscole e minuscole tramite indice PostgreSQL normalizzato. La cancellazione fisica è consentita finché non esistono riferimenti operativi e sarà rivalutata con prezzi, fornitori e magazzino.

### Category

Il modello `Category` è implementato con `name`, `description`, `parent_id`, `active`, ID e timestamp. La gerarchia non ha profondità fissa; auto-parenting e cicli diretti o indiretti sono vietati. I nomi sono univoci fra fratelli ignorando maiuscole e spazi iniziali/finali, ma possono ripetersi sotto padri diversi. La cancellazione di un nodo con figli restituisce conflitto. Il CRUD usa PATCH ed è coperto da test automatici.

## Entità pianificate

- Barcode, Image, Document, UnitOfMeasure e Packaging.
- Supplier, ProductSupplier e PurchasePriceHistory.
- InventoryMovement e i dati necessari a giacenza, scorta minima e ubicazione.

## Relazioni principali

| Relazione | Stato |
| --- | --- |
| Category gerarchica (`parent_id`) | Implementata. |
| Product → VATRate | Implementata; richiesta da BR-022. |
| Product → ProductFamily | Implementata e facoltativa. |
| Product → Category | Implementata e facoltativa. |
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

Alembic è l’unica fonte di verità dello schema. La catena lineare crea `users`, `vat_rates`, `categories`, `products` e `product_families`; tutte le tabelle includono ID, timestamp,
nullability e vincoli coerenti con i modelli ORM registrati in `app.models`.

`DATABASE_URL` proviene dalla configurazione applicativa anche durante le
migrazioni. La baseline è stata verificata su database vuoto, una seconda
esecuzione di `alembic upgrade head` è risultata idempotente e
`alembic check` non ha rilevato operazioni mancanti.

Una migrazione correttiva applica il vincolo `ck_vat_rates_rate_range`; la revisione `a4c5d6e7f8b9` crea Categories, la chiave esterna gerarchica, il vincolo sul nome e gli indici univoci normalizzati per radici e fratelli.

## Decisioni aperte

> TODO: verificare con il maintainer se quantità, ubicazione e scorta minima debbano vivere direttamente in Product o in entità dedicate.

> TODO: verificare con il maintainer il modello definitivo per allegati, immagini e barcode.

## Documenti correlati

- [Architettura](../00_Project/ARCHITECTURE.md)
- [Regole di business](../03_Business/BUSINESS_RULES.md)
- [Decisioni](../05_Project_Management/DECISIONS.md)
