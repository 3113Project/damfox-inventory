# REVIEW-0024

## Metadati

- **Task:** TASK-0024
- **Titolo:** Unità di misura obbligatoria per i nuovi prodotti
- **Data:** 2026-08-02
- **Commit analizzato:** `bc40e8f`
- **Verdetto:** APPROVATO
- **Rischio:** Basso

## Sintesi esecutiva

Il requisito API è applicato senza migrazione né backfill: ProductCreate richiede un'unità valida, ProductUpdate resta parziale ma rifiuta NULL, mentre la colonna database rimane nullable per le righe storiche.

## Indicatori

- Blocking issues: 0
- Alta priorità: 0
- Media priorità: 0
- Bassa priorità: 0
- Pronto per sviluppo o merge: SÌ

## Problemi identificati

Nessuno.

## Review per file

- Schema Product: campo richiesto in create e null vietato in update.
- Test Products/Families/Identifiers: fixture esplicite senza unità implicite.
- Test UnitOfMeasure: 422 su omissione/null, 404 su FK assente, PATCH valido su record storico e OpenAPI.
- Documentazione: distinzione tra compatibilità DB e requisito API esplicita.

## Review end-to-end

- Build Docker backend: riuscita.
- Suite completa PostgreSQL: 26 test superati.
- OpenAPI ProductCreate: unit_of_measure_id richiesto.
- Alembic check: pulito; nessuna modifica schema.

## Regressioni potenziali

I client che creavano prodotti senza unità ricevono ora 422 come richiesto. Nessun dato storico è stato modificato.

## Checklist

- [x] ProductCreate obbligatorio
- [x] ProductUpdate parziale
- [x] Null PATCH vietato
- [x] Database nullable
- [x] Nessun backfill
- [x] 422 e 404
- [x] Record storico aggiornabile
- [x] OpenAPI
- [x] Suite completa
- [x] Documentazione

## Piano di consolidamento

TASK-0025 può integrare filtri e ricerca per unità.

## Decisioni richieste al maintainer

Nessuna.

## Conferma finale

TASK-0024 è APPROVATO senza problemi bloccanti. TASK-0025 è autorizzato e può passare a Planned.
