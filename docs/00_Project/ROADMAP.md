# Roadmap

## Principi della roadmap

La roadmap è incrementale, non assegna date e non sostituisce le regole di business. Uno stato `Completed` indica soltanto ciò che è verificabile nel repository; `In progress` indica artefatti presenti ma non completi; `Planned` indica lavoro futuro; `Blocked` richiede una decisione o un prerequisito.

## Milestone 0.1 — Fondamenta tecniche

- Completed — Struttura backend FastAPI.
- Completed — Docker Compose e PostgreSQL 17.
- Completed — SQLAlchemy, configurazione Pydantic Settings e struttura Alembic.
- Completed — Modulo IVA consolidato con validazioni, transazioni sicure, errori HTTP, PATCH e test automatici.
- Completed — Baseline Alembic ripetibile per User e VAT, metadata deterministica e configurazione database unica.
- Completed — Test automatici VAT eseguiti nel container.
- Completed — Quality gate delle fondamenta su immagine backend senza cache e database ricreato da zero.

## Milestone 0.2 — Categorie

- Completed — Modello gerarchico, service, API, migrazione, validazioni, rollback e test automatici.

## Milestone 0.3 — Catalogo prodotti base

- Completed — Nucleo Products con SKU immutabile, Category facoltativa e VAT obbligatoria.
- Completed — Famiglie prodotto facoltative e filtro Products per famiglia.
- Completed — Barcode, codice produttore e ricerca catalogo base.
- Completed — Quality gate del catalogo base da build e database puliti.
- Completed — Unità di misura, requisito sui nuovi prodotti, filtri, ricerca e quality gate end-to-end.
- Planned — Documenti, immagini e ricerca avanzata, secondo BUSINESS_RULES.md.

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
