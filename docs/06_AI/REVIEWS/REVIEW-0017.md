# REVIEW-0017

## Metadati

- **Task:** TASK-0017
- **Titolo:** Quality gate delle fondamenta
- **Data:** 2026-08-02
- **Commit analizzato:** `102091d` — baseline pubblicata dopo TASK-0016
- **Verdetto:** APPROVATO CON RISERVE
- **Rischio:** Basso

## Sintesi esecutiva

Le fondamenta database, VAT e Categories superano il quality gate. L’immagine backend è stata ricostruita senza cache, PostgreSQL è stato ricreato da zero, tutte le migrazioni sono state applicate e la suite completa ha superato 12 test. Import, avvio, endpoint di stato, Swagger, OpenAPI, metadata, vincoli, transazioni e rollback risultano operativi. Non sono presenti `create_all()` nel percorso applicativo, segreti sensibili tracciati o file applicativi non tracciati necessari all’avvio.

Tutti i problemi bloccanti e di priorità alta o media di REVIEW-0010 risultano risolti. Restano soltanto placeholder dichiarati per funzionalità future e una riserva di riproducibilità: `backend/requirements.txt` non vincola le versioni. La ricostruzione pulita ha avuto esito positivo con le versioni correnti, quindi la riserva non blocca Products, ma deve essere consolidata prima di una release stabile.

## Indicatori

- Blocking issues: 0
- Alta priorità: 0
- Media priorità: 0
- Bassa priorità: 1
- Pronto per sviluppo o merge: SÌ

## Problemi identificati

### BUG-0017-001

- **Priorità:** Bassa
- **Milestone o task di risoluzione:** Prima della release 1.0, mediante task dedicato
- **File interessati:** `backend/requirements.txt`
- **Descrizione:** Le dipendenze Python sono dichiarate senza versioni o intervalli, quindi una ricostruzione futura può installare combinazioni differenti da quelle verificate.
- **Regola o documento violato:** PROJECT_CONSTITUTION.md, principi 11 e 12 sulla qualità verificabile e installabilità.
- **Intervento consigliato:** Definire una strategia di versionamento o lock delle dipendenze e verificarla con una build senza cache.

## Review per file e area

- `backend/app/main.py`: import e avvio corretti; nessuna creazione implicita dello schema; router VAT e Categories registrati.
- `backend/app/database/`, `backend/alembic/`: configurazione unica, metadata deterministica e catena lineare fino a `a4c5d6e7f8b9`.
- `backend/app/models/`: metadata con `users`, `vat_rates` e `categories`, coerente con PostgreSQL.
- `backend/app/services/`: commit protetti da rollback e regole applicative verificate dai test.
- `backend/app/api/v1/`: CRUD VAT e Categories, PATCH, 404/409/422 e OpenAPI verificati.
- `backend/tests/`: 12 test end-to-end e transazionali superati.
- `docker-compose.yml`: ambiente locale avviabile; la password visibile è una credenziale dichiaratamente di sviluppo, non un segreto operativo. Nessun token o materiale di chiave privata è tracciato.
- `backend/.env` e `postgres/`: correttamente ignorati da Git.
- Placeholder vuoti in auth, pagination, security e logging: differiti perché le relative funzionalità non sono attive e non impediscono import o avvio.
- Architettura, Features, Roadmap, Database, Business Rules, Changelog e decisioni: coerenti dopo due correzioni testuali deterministiche e la registrazione del quality gate.

## Review end-to-end

Sequenza verificata:

1. `docker compose down`;
2. eliminazione mirata dei dati nel solo volume locale `postgres/`;
3. `docker compose up -d db`;
4. `docker compose run --rm backend alembic upgrade head`;
5. `docker compose build --no-cache backend`;
6. `docker compose up -d --force-recreate backend` e attesa del completamento dell’avvio Uvicorn;
7. `docker compose exec backend python -m unittest discover -s tests -v`;
8. verifica HTTP di `/`, `/docs` e `/openapi.json`;
9. `alembic upgrade head`, `alembic current`, `alembic heads` e `alembic check`;
10. confronto tramite SQLAlchemy Inspector fra metadata e schema PostgreSQL;
11. scansione di `create_all()`, file vuoti, file non tracciati e pattern di segreti.

Risultati:

- build backend senza cache: completata;
- migrazioni da database vuoto: 4 revisioni applicate fino a `a4c5d6e7f8b9`;
- secondo upgrade: idempotente;
- `alembic check`: `No new upgrade operations detected`;
- metadata applicativa: `categories`, `users`, `vat_rates`;
- schema: le stesse tre tabelle più `alembic_version`;
- FK Categories: `parent_id → categories.id` con `ON DELETE RESTRICT`;
- indici Categories: parent, unicità normalizzata radici e unicità normalizzata fratelli;
- check VAT e Category: presenti;
- test: 12 su 12 superati;
- stato, Swagger e OpenAPI: HTTP 200;
- `create_all()`: nessuna occorrenza nel backend;
- file applicativi non tracciati: nessuno;
- token, chiavi private o segreti sensibili tracciati: nessuno.

La prima invocazione dei test immediatamente dopo la ricreazione del container ha incontrato `Connection refused` prima del completamento dell’avvio Uvicorn; dopo il messaggio `Application startup complete`, la stessa suite è passata integralmente. La sequenza ripetibile deve quindi includere una verifica di readiness prima dei test.

## Riesame completo di REVIEW-0010

### Problemi bloccanti BUG-001—BUG-009

| Problema | Stato | Evidenza |
| --- | --- | --- |
| BUG-001 import model Category | Risolto | Usa `app.models.base_model`; import verificato. |
| BUG-002 import schema Category | Risolto | Usa Pydantic direttamente; import verificato. |
| BUG-003 service Categories assente | Risolto | CRUD e regole gerarchiche implementati e testati. |
| BUG-004 router Categories assente | Risolto | Router CRUD operativo. |
| BUG-005 router non registrato | Risolto | Registrato in `api.v1` e `main.py`; OpenAPI verificata. |
| BUG-006 Category fuori metadata | Risolto | `categories` presente in `Base.metadata.tables`. |
| BUG-007 migrazione Categories assente | Risolto | Revisione `a4c5d6e7f8b9` applicata e coerente. |
| BUG-008 naming convention non valida | Risolto | Mapping SQLAlchemy deterministica e `alembic check` pulito. |
| BUG-009 `create_all()` all’avvio | Risolto | Nessuna occorrenza nel backend. |

### Punti ad alta priorità

| Punto REVIEW-0010 | Stato |
| --- | --- |
| Duplicati Category radice | Risolto con indice univoco normalizzato dedicato. |
| Auto-parenting | Risolto e testato con 409. |
| Cicli diretti o indiretti | Risolto e testato. |
| Eliminazione Category con figli | Risolto secondo DECISION-0003 con 409. |
| Politica `ondelete` | Risolto con `RESTRICT` e controllo service. |
| Esistenza del padre | Risolto con 404 deterministico. |
| Rollback VAT | Risolto e testato con riuso della sessione. |
| Duplicati e integrità VAT | Risolto con 409 e rollback. |
| Null espliciti VAT | Risolto con 422. |
| Timestamp VAT | Risolto nella baseline Alembic. |
| Migrazione User vuota | Risolto: la baseline crea `users` coerentemente. |

### Punti a media priorità

| Punto REVIEW-0010 | Stato |
| --- | --- |
| Limite nome Category | Risolto a 100 caratteri. |
| Limiti e intervallo VAT | Risolto secondo DECISION-0004 e testato. |
| Semantica campo omesso/null Category | Risolto con `exclude_unset=True` e test. |
| PUT usato per update parziale | Risolto: PATCH presente, PUT assente. |
| Docstring VAT | Risolto nei moduli consolidati. |
| Tipi di ritorno VAT service | Risolto. |
| Due implementazioni `get_db` | Risolto con dependency canonica unica. |
| Registrazione modelli non uniforme | Risolto tramite `app.models`. |
| URL Alembic separato | Risolto tramite settings applicative. |
| Whitespace Compose | Risolto. |
| Test automatici assenti | Risolto con 12 test. |

### Punti a bassa priorità

| Punto REVIEW-0010 | Stato |
| --- | --- |
| Header descrittivi | Risolto nei moduli consolidati. |
| Newline finali | Risolto nei file applicativi interessati. |
| Ordine import | Risolto funzionalmente; resta solo uniformità cosmetica non bloccante in alcuni file Categories. |
| Righe vuote VAT model | Risolto. |
| Commenti separatori Category | Risolto. |
| Placeholder auth/pagination/logging/security | Differito: funzionalità future, dichiarate in architettura e non bloccanti. |

## Regressioni potenziali

- La mancata versione delle dipendenze può modificare il risultato di build future; BUG-0017-001 ne traccia il consolidamento.
- I test end-to-end richiedono che Uvicorn abbia completato l’avvio; eseguire una readiness check prima della suite.
- Auth, autorizzazione e sicurezza utenti non sono ancora implementati e non devono essere considerati disponibili nel modulo Products.

## Checklist

- [x] Import e avvio
- [x] Modelli
- [x] Schemi
- [x] Service
- [x] Router
- [x] Migrazioni
- [x] Error handling e rollback
- [x] Test
- [x] OpenAPI
- [x] Documentazione

## Piano di consolidamento

1. Pianificare un task dedicato al versionamento riproducibile delle dipendenze Python prima della release 1.0.
2. Conservare una readiness check esplicita nelle esecuzioni end-to-end.
3. Implementare autenticazione, autorizzazione e hashing password esclusivamente nel futuro task dedicato agli utenti.

## Decisioni richieste al maintainer

- Definire in un task successivo la strategia di versionamento o lock delle dipendenze.
- Definire il perimetro esatto del primo task Products prima dell’implementazione.

## Conferma finale

Le fondamenta sono approvate con una riserva non bloccante. Products può iniziare: database, VAT e Categories sono sufficientemente affidabili e verificati. Il modulo Products dovrà restare un verticale completo e non dovrà includere auth o altre funzionalità non pianificate. BUG-0017-001 deve essere risolto prima della release 1.0.
