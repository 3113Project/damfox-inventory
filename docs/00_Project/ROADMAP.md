# Roadmap

## Principi della roadmap

La roadmap è incrementale, non assegna date e non sostituisce le regole di business. Uno stato `Completed` indica soltanto ciò che è verificabile nel repository; `In progress` indica artefatti presenti ma non completi; `Planned` indica lavoro futuro; `Blocked` richiede una decisione o un prerequisito.

## Milestone 0.1 — Fondamenta tecniche

- Completed — Struttura backend FastAPI.
- Completed — Docker Compose e PostgreSQL 17.
- Completed — SQLAlchemy, configurazione Pydantic Settings e struttura Alembic.
- Completed — Modulo IVA CRUD.
- In progress — Consolidamento migrazioni: la migrazione utenti è vuota e la migrazione IVA non riflette i timestamp del modello.
- Planned — Test minimi automatizzati.

## Milestone 0.2 — Categorie

- In progress — Modello gerarchico e schemi iniziali nel working tree.
- Planned — Service, API, migrazione, validazioni, test e documentazione operativa.

## Milestone 0.3 — Catalogo prodotti

- Planned — Prodotti con SKU immutabile, categoria e IVA.
- Planned — Famiglie, barcode, documenti, immagini e ricerca, secondo BUSINESS_RULES.md.

## Milestone 0.4 — Fornitori e prezzi

- Planned — Fornitori, relazione prodotto-fornitore e storico prezzi.
- Planned — Ricarichi, listini, prezzi manuali, sconti e margini.

## Milestone 0.5 — Magazzino

- Planned — Giacenze, scorte minime, ubicazioni, confezioni e movimenti.
- Planned — Lista acquisti, miglior fornitore e riordino.

## Milestone 0.6 — Sicurezza e utenti

- In progress — Modello User presente.
- Planned — Migrazione utenti, autenticazione, autorizzazione e gestione sicura delle password.

## Milestone 0.7 — Frontend operativo

- Planned — Frontend responsivo, ricerca, tabelle e flussi conformi alle linee guida UI.

## Milestone 1.0 — Prima release stabile

- Planned — Catalogo, fornitori, prezzi e magazzino integrati.
- Planned — Migrazioni affidabili, test, sicurezza e documentazione operativa consolidate.

## Documenti correlati

- [Funzionalità](FEATURES.md)
- [Architettura](ARCHITECTURE.md)
- [Attività](../05_Project_Management/TASKS.md)
