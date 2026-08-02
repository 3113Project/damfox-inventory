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

Il runtime verificabile è composto da Docker Compose, un servizio PostgreSQL 17 (`db`) e un servizio backend FastAPI (`backend`). Il backend dipende dal database, riceve il codice sorgente tramite volume `./backend:/app` e pubblica `18000:8000`. PostgreSQL persiste i dati nel volume locale `./postgres:/var/lib/postgresql/data`.

Il client web o mobile è futuro: non è presente nel repository.

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

`app.core.config.Settings` legge `DATABASE_URL` e `SQL_ECHO` dalla configurazione esterna. Docker Compose passa `backend/.env` al servizio backend e Alembic usa la stessa `DATABASE_URL` tramite `alembic/env.py`; `alembic.ini` non contiene un URL concorrente.

## API

L'API è impostata come FastAPI versione `0.1.0`. Sono presenti i router `v1` per `/vat-rates`, `/categories` e `/products`, entrambi con operazioni di elenco, dettaglio, creazione, aggiornamento PATCH e cancellazione. L'endpoint `/` restituisce lo stato del software. FastAPI espone OpenAPI e Swagger nel percorso standard `/docs`.

## Sicurezza

Non risultano autenticazione o autorizzazione operative: esiste un modello User ma `dependencies/auth.py`, `core/security.py` e il logging sono vuoti.

## Frontend

Il frontend è pianificato e non è implementato. Consultare [UI_GUIDELINES.md](../04_UI/UI_GUIDELINES.md).

## Readiness e dipendenze

Le dipendenze Python runtime dirette sono fissate a versioni esatte. PostgreSQL espone un healthcheck `pg_isready`; l’immagine backend verifica lo stato applicativo tramite `scripts/wait_for_backend.py`, riutilizzabile anche prima dei test.

## Deployment attuale

L'unico ambiente verificabile è Docker Compose con backend e PostgreSQL, rete predefinita Compose, volume dati locale e porta host `18000` per l'API.

## Documenti correlati

- [Contesto AI](AI_CONTEXT.md)
- [Funzionalità](FEATURES.md)
- [Modello dati](../02_Database/DATABASE.md)
- [Regole di business](../03_Business/BUSINESS_RULES.md)
