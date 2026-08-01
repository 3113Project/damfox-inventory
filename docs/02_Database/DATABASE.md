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

Il modello `VATRate` è implementato con `id`, `description` univoca, `rate` numerico e `active`. Il CRUD REST è disponibile. La relativa migrazione crea `vat_rates`, ma non include i timestamp ereditati dal modello base.

### User

Il modello `User` è presente con username univoco, password e flag `is_admin`. Non sono presenti API o autenticazione. La revisione Alembic dedicata è vuota, quindi non crea la tabella.

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

Alembic è presente e configura `Base.metadata` come target. Tuttavia `main.py` esegue anche `Base.metadata.create_all()`, creando una seconda modalità di inizializzazione dello schema. Le migrazioni utenti e IVA non sono completamente coerenti con i modelli osservabili.

> TODO: verificare con il maintainer la strategia definitiva per rendere Alembic l'unica fonte di verità dello schema.

## Decisioni aperte

> TODO: verificare con il maintainer se quantità, ubicazione e scorta minima debbano vivere direttamente in Product o in entità dedicate.

> TODO: verificare con il maintainer il modello definitivo per allegati, immagini e barcode.

## Documenti correlati

- [Architettura](../00_Project/ARCHITECTURE.md)
- [Regole di business](../03_Business/BUSINESS_RULES.md)
- [Decisioni](../05_Project_Management/DECISIONS.md)
