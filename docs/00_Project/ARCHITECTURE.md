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
| `api/` | Router FastAPI e versione `v1`; il router IVA è attivo. |
| `services/` | Query e operazioni CRUD; il service IVA è attivo. |
| `schemas/` | Schemi Pydantic per input e risposte API. |
| `models/` | Modelli SQLAlchemy; esistono User, VATRate e un Category non integrato. |
| `database/` | Base ORM, engine e session factory. |
| `dependencies/` | Dipendenza di sessione DB; auth e paginazione sono placeholder vuoti. |
| `core/` | Configurazione con Pydantic Settings; sicurezza, logging ed eccezioni sono placeholder vuoti. |

## Flusso di una richiesta

Per il CRUD IVA, il router `api/v1/vat_rates.py` riceve e valida la richiesta tramite schemi Pydantic, ottiene una sessione DB tramite dipendenza, delega al service e restituisce il modello ORM convertito nello schema di risposta. Il service usa SQLAlchemy per interrogare o modificare PostgreSQL; gli errori di risorsa non trovata sono gestiti dal router con HTTP 404.

## Database e migrazioni

SQLAlchemy e Alembic sono presenti. `alembic/env.py` espone la metadata ORM per l'autogenerazione. Esistono revisioni per utenti e aliquote IVA.

Debito tecnico osservabile:

- `main.py` esegue `Base.metadata.create_all(bind=engine)`, mentre Alembic è la fonte di verità prevista dalla documentazione.
- La revisione `create_users_table` non crea alcuna tabella.
- La revisione IVA non contiene i timestamp ereditati da `BaseModel`.
- Il modello Category non è importato nella metadata, non ha migrazione e usa import di moduli non presenti (`app.models.base` e `app.schemas.base`).

> TODO: verificare con il maintainer la strategia definitiva di inizializzazione e allineamento schema/migrazioni.

## Configurazione

`app.core.config.Settings` legge `DATABASE_URL` e `SQL_ECHO` dal file `.env`. Docker Compose passa `backend/.env` al servizio backend. Alembic possiede anche un URL nel proprio file di configurazione.

## API

L'API è impostata come FastAPI versione `0.1.0`. È presente il router `v1` per `/vat-rates` con operazioni di elenco, dettaglio, creazione, aggiornamento e cancellazione. L'endpoint `/` restituisce lo stato del software. FastAPI espone OpenAPI e Swagger nel percorso standard `/docs`.

## Sicurezza

Non risultano autenticazione o autorizzazione operative: esiste un modello User ma `dependencies/auth.py`, `core/security.py` ed eccezioni/logging sono vuoti.

## Frontend

Il frontend è pianificato e non è implementato. Consultare [UI_GUIDELINES.md](../04_UI/UI_GUIDELINES.md).

## Deployment attuale

L'unico ambiente verificabile è Docker Compose con backend e PostgreSQL, rete predefinita Compose, volume dati locale e porta host `18000` per l'API.

## Decisioni ancora aperte

> TODO: verificare con il maintainer la configurazione unica dell'URL database fra backend e Alembic.

> TODO: verificare con il maintainer il modello dati definitivo per categorie e il piano di integrazione del relativo modulo.

## Documenti correlati

- [Contesto AI](AI_CONTEXT.md)
- [Funzionalità](FEATURES.md)
- [Modello dati](../02_Database/DATABASE.md)
- [Regole di business](../03_Business/BUSINESS_RULES.md)
