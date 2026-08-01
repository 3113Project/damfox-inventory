# DAMFOX Inventory — Contesto per agenti AI

## Identità e obiettivo

DAMFOX Inventory è un gestionale open source per una ferramenta, estendibile a contesti simili. L'obiettivo è gestire catalogo tecnico, fornitori, prezzi e magazzino con un'architettura che cresca senza riprogettazioni premature.

## Utenti destinatari

Operatori di ferramenta e magazzino, personale d'ufficio e tecnici: utenti che devono lavorare con dati tecnici senza essere esperti di database.

## Filosofia

Semplicità operativa, tracciabilità, API-first, separazione delle responsabilità e crescita incrementale. Il progetto intende essere open source.

## Stack e architettura

- Python 3.13, FastAPI, Uvicorn, SQLAlchemy, PostgreSQL 17, Alembic, Pydantic Settings e Docker Compose.
- Flusso: Client → Router FastAPI → Service → Model SQLAlchemy → PostgreSQL.
- La configurazione è esterna tramite `.env`; le modifiche strutturali devono passare da Alembic.

## Stato attuale

- Implementati: backend base, endpoint di stato e CRUD delle aliquote IVA.
- In sviluppo nel working tree: artefatti iniziali per categorie; non sono ancora integrati end-to-end.
- Pianificati: prodotti, fornitori, prezzi, magazzino, frontend, mobile e automazioni.

## Regole invarianti

- Non inserire segreti nel codice.
- Non rompere API o rinominare campi database senza migrazione approvata.
- Il prezzo d'acquisto appartiene al rapporto prodotto-fornitore, non al prodotto.
- SKU univoco e immutabile per ogni prodotto.
- Storico prezzi e vendite devono essere tracciabili.
- Non inventare decisioni: in caso di ambiguità usare `TODO: verificare con il maintainer`.

## Documenti da leggere prima di modificare codice

1. [Architettura](ARCHITECTURE.md), [funzionalità](FEATURES.md) e [roadmap](ROADMAP.md).
2. [Regole di business](../03_Business/BUSINESS_RULES.md) e [modello dati](../02_Database/DATABASE.md).
3. [Standard](../01_Development/CODING_STANDARDS.md) e [workflow](../01_Development/DEVELOPMENT_WORKFLOW.md).
4. [Sistema Task e Git](../06_AI/README.md).

## Documenti correlati

- [README documentazione](../README.md)
- [Decisioni progettuali](../05_Project_Management/DECISIONS.md)
- [Git Workflow](../06_AI/GIT_WORKFLOW.md)
