# REVIEW-0015 — Consolidamento del modulo VAT

## Metadati

- **Task:** TASK-0015
- **Titolo:** Consolidamento del modulo VAT
- **Data:** 2026-08-02
- **Commit analizzato:** 350b921
- **Verdetto:** APPROVATO
- **Rischio:** Basso

## Sintesi esecutiva

Il modulo VAT è stato consolidato end-to-end secondo DECISION-0004. Gli input
validano la descrizione e l’aliquota, gli update parziali usano PATCH e
rifiutano null espliciti, i service effettuano rollback su ogni errore
transazionale e le violazioni di integrità producono HTTP 409 deterministici.

Il modello e PostgreSQL applicano l’intervallo inclusivo `0.00–100.00`; una
migrazione correttiva reversibile aggiunge il vincolo
`ck_vat_rates_rate_range`. La suite automatica usa `unittest`, FastAPI e
PostgreSQL reali nel container: 6 test risultano verdi.

I file Categories locali sono rimasti invariati, come verificato tramite hash.
TASK-0016 è autorizzato dal punto di vista tecnico.

## Indicatori

- Blocking issues: 0
- Alta priorità: 0
- Media priorità: 0
- Bassa priorità: 0
- Test automatici: 6 verdi
- Migrazioni Alembic a head: `f3b1c2d4e5a6`
- Differenze rilevate da `alembic check`: 0
- Pronto per sviluppo o merge: SÌ

## Problemi identificati

Nessun problema residuo nel perimetro di TASK-0015.

## Review per file

| File | Esito |
| --- | --- |
| `backend/app/models/vat_rate.py` | Modello documentato, `Numeric(5,2)` e CHECK `0.00–100.00`. |
| `backend/app/schemas/vat_rate.py` | Descrizione normalizzata 1–50 caratteri; rate con range e scala; null PATCH vietati. |
| `backend/app/services/vat_rate_service.py` | Tipi, docstring, rollback e conflitti deterministici. |
| `backend/app/api/v1/vat_rates.py` | CRUD sottile, PATCH, HTTP 404/409 e risposta DELETE 204. |
| Package `__init__.py` | Esportazioni VAT esplicite; nessuna esportazione Categories. |
| `backend/app/core/exceptions.py` | Eccezioni applicative minime e riutilizzabili. |
| `backend/app/main.py` | Router VAT registrato; nessun router Categories. |
| Migrazione `f3b1c2d4e5a6` | CHECK aggiunto e rimosso correttamente. |
| `backend/tests/test_vat_rates.py` | CRUD, duplicati, rollback, null, limiti, range, scala, 404, PATCH e OpenAPI. |
| Documentazione e stato AI | Allineati allo stato verificato. |

## Review end-to-end

1. Create accetta descrizioni valide e rate inclusi tra `0.00` e `100.00`.
2. Stringhe vuote, spazi, oltre 50 caratteri, null e rate non validi restituiscono 422.
3. PATCH aggiorna soltanto i campi forniti e rifiuta null espliciti.
4. GET, PATCH e DELETE su risorse assenti restituiscono 404 coerente.
5. Duplicati in create e PATCH restituiscono 409.
6. Dopo un errore di integrità la stessa sessione resta utilizzabile, verificando il rollback.
7. Il CHECK PostgreSQL respinge inserimenti diretti fuori intervallo.
8. DELETE restituisce 204 senza body.
9. OpenAPI espone PATCH, non PUT, e documenta minimo e massimo.
10. Downgrade e nuovo upgrade della migrazione correttiva hanno esito positivo.
11. `alembic check` non rileva differenze tra modello e database.
12. Tutti i 6 test automatici sono verdi nel container.

## Regressioni potenziali

- I client che usavano PUT devono migrare a PATCH; il modulo non era ancora
  pubblicato come API stabile.
- I dati VAT fuori dall’intervallo approvato impedirebbero l’applicazione della
  migrazione; il database di sviluppo verificato non ne contiene.
- Categories resta intenzionalmente escluso dal modulo e dalla metadata.

## Checklist

- [x] Import e avvio
- [x] Modello
- [x] Schemi
- [x] Service
- [x] Router
- [x] Migrazione
- [x] Error handling e rollback
- [x] Test
- [x] OpenAPI
- [x] Documentazione
- [x] File Categories invariati

## Piano di consolidamento

1. Pubblicare il commit applicativo e REVIEW-0015.
2. Eseguire TASK-0016 per Categories secondo le decisioni dedicate.
3. Eseguire TASK-0017 come quality gate finale delle fondamenta.

## Decisioni richieste al maintainer

Nessuna.

## Autorizzazione TASK-0016

TASK-0016 è autorizzato: il modulo VAT costituisce ora un riferimento verticale
con validazioni, transazioni, errori, migrazione, test e documentazione coerenti.

## Conferma finale

Sono stati prodotti il commit applicativo `350b921` e questa Engineering
Review. Non sono stati usati pull, merge, rebase, reset o stash. I quattro file
Categories locali conservano gli hash registrati prima dell’intervento e non
sono stati inclusi nello staging.
