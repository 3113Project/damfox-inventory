# Funzionalità

## Implementato

- **Backend FastAPI:** applicazione avviabile con endpoint di stato `GET /`.
- **Aliquote IVA:** CRUD REST end-to-end su `/vat-rates/`, con PATCH parziale, validazioni `0.00–100.00`, errori deterministici, rollback transazionale, vincolo database e test automatici.

## In sviluppo

- **Categorie:** il working tree contiene modello gerarchico e schemi iniziali, ma service e router sono vuoti, il router non è registrato e non esiste una migrazione. Il modulo non è disponibile end-to-end.
- **Utenti:** esiste il modello ORM, senza API, autenticazione o migrazione effettiva della tabella.

## Pianificato

### Catalogo

- Ricerca e classificazione tecnica degli articoli (BR-001, BR-007, BR-009).
- Famiglie, immagini, documenti, codici produttore e barcode (BR-003, BR-004, BR-006, BR-008).

### Categorie

- Categorie operative gerarchiche e campi specifici per categoria (BR-009).

### Prodotti

- SKU univoco e immutabile, varianti indipendenti, IVA e unità di misura (BR-002, BR-005, BR-022, BR-053).

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
