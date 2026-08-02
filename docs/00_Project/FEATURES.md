# Funzionalità

## Implementato

- **Backend FastAPI:** applicazione avviabile con endpoint di stato `GET /`.
- **Aliquote IVA:** CRUD REST end-to-end su `/vat-rates/`, con PATCH parziale, validazioni `0.00–100.00`, errori deterministici, rollback transazionale, vincolo database e test automatici.
- **Categorie:** CRUD REST gerarchico su `/categories`, PATCH parziale, nomi univoci per fratelli ignorando maiuscole e spazi esterni, cicli vietati, cancellazione dei nodi padre protetta e test automatici.
- **Prodotti:** CRUD REST su `/products` con SKU immutabile e univoco senza distinzione di maiuscole, Category facoltativa, VAT obbligatoria e PATCH parziale.
- **Famiglie prodotto:** CRUD su `/product-families`, associazione facoltativa e filtro Products; nessun effetto commerciale.
- **Identificativi e ricerca:** barcode multipli univoci, codice produttore e ricerca case-insensitive su campi catalogo disponibili.

## In sviluppo

- **Utenti:** esiste il modello ORM, senza API o autenticazione; la tabella è presente nella baseline Alembic.

## Pianificato

### Catalogo

- Ricerca e classificazione tecnica degli articoli (BR-001, BR-007, BR-009).
- Famiglie, immagini, documenti, codici produttore e barcode (BR-003, BR-004, BR-006, BR-008).

### Fornitori

- Fornitori multipli e dati del rapporto prodotto-fornitore (BR-010, BR-011, BR-012).

### Prezzi

- Storico prezzi, ricarichi, prezzo manuale, sconti e margini (BR-020—BR-025, BR-040, BR-042).

### Magazzino

- Quantità, scorta minima, ubicazioni, confezioni e movimenti (BR-050—BR-056).

### Acquisti

- Lista acquisti, suggerimento del miglior fornitore e riordino (BR-051, BR-052).

### Clienti

- Condizioni commerciali e prezzi personalizzati (BR-030, BR-031).

### Frontend

- Interfaccia responsiva conforme a [UI_GUIDELINES.md](../04_UI/UI_GUIDELINES.md).

### Mobile

- Scanner barcode, carico magazzino e inventario.

### Automazione e AI

- Import listini, dashboard, statistiche e OCR di DDT/fatture (BR-100).

## Futuro

- Applicazione mobile completa.
- Integrazioni di intelligenza artificiale e OCR.
- Dashboard e statistiche avanzate.

## Documenti correlati

- [Roadmap](ROADMAP.md)
- [Regole di business](../03_Business/BUSINESS_RULES.md)
- [Architettura](ARCHITECTURE.md)
