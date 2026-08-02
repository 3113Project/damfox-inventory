# Architettura

## Scopo

Descrivere l'architettura effettivamente presente e il debito tecnico osservabile, senza presentare come implementati i moduli pianificati.

## Principi architetturali

- Modularità.
- Separazione delle responsabilità.
- API-first.
- Configurazione esterna.
- Migrazioni controllate.
- Crescita incrementale.
- Facilità d'uso per utenti non tecnici.

## Architettura runtime

Il runtime verificabile è composto da Docker Compose, PostgreSQL 17 (`db`), FastAPI (`backend`) e React/Vite (`frontend`). Il backend dipende dal database e pubblica `18000:8000`; il frontend dipende dalla readiness backend e pubblica `15173:5173`. PostgreSQL persiste i dati in `./postgres:/var/lib/postgresql/data`.

Il client web usa TypeScript strict, React Router e TanStack Query. `VITE_API_BASE_URL` centralizza l'indirizzo pubblico dell'API visto dal browser.

## Architettura applicativa

| Area | Responsabilità osservabile |
| --- | --- |
| `api/` | Router FastAPI e versione `v1`; i router IVA, Categories e Products sono attivi. |
| `services/` | Query e operazioni CRUD; i service IVA, Categories e Products sono attivi. |
| `schemas/` | Schemi Pydantic per input e risposte API. |
| `models/` | Modelli SQLAlchemy; esistono User, VATRate, Category e Product integrati nella metadata. |
| `database/` | Base ORM, engine e session factory. |
| `dependencies/` | Dipendenza di sessione DB; auth e paginazione sono placeholder vuoti. |
| `core/` | Configurazione con Pydantic Settings ed eccezioni applicative condivise; sicurezza e logging sono placeholder vuoti. |

## Flusso di una richiesta

Per i CRUD IVA e Categories, i router `api/v1/vat_rates.py` e `api/v1/categories.py` ricevono e validano la richiesta tramite schemi Pydantic, ottengono una sessione DB tramite dipendenza, delegano al service e restituiscono il modello ORM convertito nello schema di risposta. Il service usa SQLAlchemy per interrogare o modificare PostgreSQL; gli errori di risorsa non trovata sono gestiti dal router con HTTP 404.

## Database e migrazioni

Alembic è l’unica fonte di verità dello schema. Le revisioni lineari creano `users`, `vat_rates`, `categories` e `products` con ID, timestamp, chiavi primarie e vincoli univoci
coerenti con i modelli inclusi nella metadata. L’avvio FastAPI non esegue
`Base.metadata.create_all()`.

La baseline è stata verificata partendo da PostgreSQL vuoto, applicando due volte
`alembic upgrade head` e controllando con `alembic check` l’assenza di
differenze tra metadata e database.

Category è inclusa nella metadata e nella migrazione `a4c5d6e7f8b9`, verificata anche con downgrade e nuovo upgrade.

## Configurazione

`app.core.config.Settings` legge `DATABASE_URL`, `SQL_ECHO` e `CORS_ORIGINS` dalla configurazione esterna. Docker Compose autorizza esplicitamente `http://localhost:15173`, senza wildcard, e passa `backend/.env` al backend. Alembic usa la stessa `DATABASE_URL` tramite `alembic/env.py`.

## API

L'API è impostata come FastAPI versione `0.1.0`. Sono presenti i router `v1` per `/vat-rates`, `/categories` e `/products`, entrambi con operazioni di elenco, dettaglio, creazione, aggiornamento PATCH e cancellazione. L'endpoint `/` restituisce lo stato del software. FastAPI espone OpenAPI e Swagger nel percorso standard `/docs`.

## Sicurezza

Non risultano autenticazione o autorizzazione operative: esiste un modello User ma `dependencies/auth.py`, `core/security.py` e il logging sono vuoti.

## Frontend

Il frontend in `frontend/` offre una app shell responsiva e un verticale operativo per il catalogo prodotti. La lista, ricerca e filtri interrogano il backend tramite TanStack Query; dettaglio, creazione e modifica usano i contratti API reali e lookup server-side. Lo SKU resta immutabile e l'unità di misura è obbligatoria nel form. Le altre sezioni usano empty state espliciti. Consultare [UI_GUIDELINES.md](../04_UI/UI_GUIDELINES.md).

## Readiness e dipendenze

Le dipendenze runtime backend e frontend sono fissate tramite `requirements.txt` e `package-lock.json`. PostgreSQL espone `pg_isready`; backend e frontend hanno healthcheck applicativi. Il gate finale ha verificato build senza cache, database vuoto, migrazioni complete e idempotenti, 27 test backend, 6 test frontend, build TypeScript e stack interamente healthy.

## Deployment attuale

L'ambiente verificabile è Docker Compose con frontend, backend e PostgreSQL sulla rete predefinita Compose. Le porte host sono `15173` per il client e `18000` per l'API.

## Documenti correlati

- [Contesto AI](AI_CONTEXT.md)
- [Funzionalità](FEATURES.md)
- [Modello dati](../02_Database/DATABASE.md)
- [Regole di business](../03_Business/BUSINESS_RULES.md)
