# DAMFOX Inventory

## Descrizione

DAMFOX Inventory è un gestionale open source per catalogo tecnico, fornitori, prezzi e magazzino. Nasce per una ferramenta, ma è pensato per estendersi a contesti simili senza perdere semplicità operativa.

## Visione

Il progetto punta a rendere accessibili attività di catalogo e magazzino a utenti non tecnici, mantenendo dati tracciabili, API chiare e un'architettura incrementale.

I principi non negoziabili del progetto sono definiti nella [Project Constitution](00_Project/PROJECT_CONSTITUTION.md).

## Stato del progetto

Il progetto è in fase iniziale.

- **Fondamenta tecniche disponibili:** backend FastAPI, PostgreSQL in Docker Compose, SQLAlchemy, configurazione con Pydantic Settings e Alembic.
- **Modulo IVA disponibile:** modello, schemi, servizio e router CRUD per le aliquote IVA.
- **Categorie in sviluppo:** nel working tree sono presenti modello e schemi iniziali, ma service e router non sono completi né integrati; manca inoltre la migrazione.
- **Frontend:** non ancora implementato.
- **Altri moduli:** catalogo prodotti, fornitori, prezzi, magazzino, acquisti, clienti e mobile sono pianificati.

## Stack tecnologico

- Python 3.13 (`python:3.13-slim` nel Dockerfile).
- FastAPI e Uvicorn.
- SQLAlchemy.
- PostgreSQL 17 (`postgres:17` in Docker Compose).
- Alembic.
- Pydantic Settings.
- Docker Compose.

Le dipendenze Python non sono fissate a versioni specifiche in `backend/requirements.txt`.

## Architettura sintetica

```text
Client → FastAPI Router → Service → SQLAlchemy Model → PostgreSQL
                    ↕
              Schemi Pydantic
```

I router espongono l'API, i servizi raccolgono logica e query, i modelli rappresentano la persistenza e gli schemi Pydantic validano input e definiscono le risposte.

## Struttura della documentazione

- [00_Project/](00_Project/): costituzione, contesto, architettura, funzionalità e roadmap.
- [01_Development/](01_Development/): standard e workflow di sviluppo.
- [02_Database/](02_Database/): stato e direzione del modello dati.
- [03_Business/](03_Business/): regole funzionali vincolanti.
- [04_UI/](04_UI/): linee guida per il frontend pianificato.
- [05_Project_Management/](05_Project_Management/): changelog, decisioni e attività.
- [06_AI/](06_AI/): task, prompt e workflow di collaborazione AI.

## Avvio del progetto

### Requisiti

- Docker e Docker Compose.
- Un file `backend/.env` con almeno `DATABASE_URL`; il backend legge anche opzionalmente `SQL_ECHO`.

Esempio non sensibile:

```env
DATABASE_URL=postgresql://<utente>:<password>@db:5432/<database>
SQL_ECHO=false
```

### Esecuzione

Dalla radice del repository:

```bash
docker compose up --build
```

Docker Compose pubblica il backend su `http://localhost:18000`. La documentazione OpenAPI generata da FastAPI è disponibile su `http://localhost:18000/docs`; lo schema OpenAPI è disponibile nel percorso standard `/openapi.json`.

## Workflow di sviluppo

Maintainer → ChatGPT → Task → Codex → GitHub → Review → Test.

Il processo operativo, il template dei task e le regole Git sono definiti in [06_AI/README.md](06_AI/README.md).

## Contribuire

Il progetto intende essere open source. Prima di contribuire, leggere:

- [Project Constitution](00_Project/PROJECT_CONSTITUTION.md)
- [AI_PROMPT.md](01_Development/AI_PROMPT.md)
- [DEVELOPMENT_WORKFLOW.md](01_Development/DEVELOPMENT_WORKFLOW.md)
- [BUSINESS_RULES.md](03_Business/BUSINESS_RULES.md)
- [Sistema AI e Task](06_AI/)

> Licenza: da definire con il maintainer.

## Documenti correlati

- [Project Constitution](00_Project/PROJECT_CONSTITUTION.md)
- [Architettura](00_Project/ARCHITECTURE.md)
- [Funzionalità](00_Project/FEATURES.md)
- [Roadmap](00_Project/ROADMAP.md)
- [Modello dati](02_Database/DATABASE.md)
- [Regole di business](03_Business/BUSINESS_RULES.md)
