# REVIEW-0014 — Consolidamento della baseline database e applicativa

## Metadati

- **Task:** TASK-0014
- **Titolo:** Consolidamento della baseline database e applicativa
- **Data:** 2026-08-02
- **Commit analizzato:** bd7a68e
- **Verdetto:** APPROVATO CON RISERVE
- **Rischio:** Medio

## Sintesi esecutiva

La baseline database e applicativa è stata consolidata e verificata con esito positivo su PostgreSQL vuoto. Alembic è l’unica fonte di verità dello schema: la metadata usa una naming convention valida, l’avvio non esegue più `create_all()`, User e VAT hanno migrazioni lineari coerenti e `DATABASE_URL` è condivisa tra applicazione e Alembic. Esiste una sola implementazione canonica di `get_db`.

Il database sacrificabile autorizzato da DECISION-0001 è stato ricreato. Upgrade, secondo upgrade idempotente, downgrade completo, ripristino a head e `alembic check` hanno avuto esito positivo. Gli endpoint `/`, `/docs` e `/openapi.json` rispondono HTTP 200.

La riserva è operativa: il branch locale è 10 commit indietro rispetto a `origin/main`. Pull, merge, rebase, reset e stash sono vietati; la pubblicazione non può quindi essere fast-forward. Le modifiche locali preesistenti sono rimaste intatte. TASK-0015 soddisfa i prerequisiti tecnici, ma resta bloccato fino alla pubblicazione.

## Indicatori

- Blocking issues applicativi: 0
- Alta priorità: 0
- Media priorità: 2
- Bassa priorità: 0
- Pronto per sviluppo o merge: NO, fino alla pubblicazione
- Migrazioni baseline: 2
- Endpoint verificati con HTTP 200: 3
- Differenze rilevate da Alembic: 0

## Problemi identificati

### BUG-014-001 — Pubblicazione non fast-forward

- **Priorità:** Media
- **Milestone o task di risoluzione:** operazione Git del maintainer
- **File interessati:** cronologia Git locale
- **Descrizione:** il branch locale è 10 commit indietro; le operazioni di riallineamento sono vietate dalle istruzioni.
- **Regola o documento violato:** nessuna; è applicato `CODEX_WORKFLOW.md`.
- **Intervento consigliato:** autorizzare un riallineamento che preservi il working tree, poi pubblicare senza force push.

### BUG-014-002 — Assenza di test automatici

- **Priorità:** Media
- **Milestone o task di risoluzione:** TASK-0015 / TASK-0017
- **File interessati:** suite test non presente
- **Descrizione:** i controlli sono ripetibili ma non appartengono a una suite automatica versionata.
- **Regola o documento violato:** Project Constitution, principio 11.
- **Intervento consigliato:** aggiungere test automatici di migrazione, metadata, avvio e OpenAPI.

## Review per file

| File | Esito |
| --- | --- |
| `backend/app/database/base.py` | Naming convention valida e deterministica. |
| `backend/app/database/session.py` | Contiene soltanto engine e session factory. |
| `backend/app/dependencies/db.py` | Unica implementazione canonica di `get_db`. |
| `backend/app/models/__init__.py` | Registra solo User e VATRate; Category esclusa. |
| `backend/app/main.py` | `create_all()` rimosso; backend avviabile; router VAT preservato. |
| `backend/app/core/config.py` | Settings condivise e documentate. |
| `backend/alembic.ini` | URL hardcoded rimosso. |
| `backend/alembic/env.py` | Usa settings applicative e `Base.metadata`. |
| Migrazioni User e VAT | Upgrade e downgrade coerenti con ID, timestamp e vincoli. |
| `docker-compose.yml` | `backend/.env` preservato; configurazione valida. |
| Documentazione autorizzata | Aggiornata allo stato verificato. |
| `docs/06_AI/TASK_INDEX.md` | TASK-0014 completato localmente; TASK-0015 bloccato fino alla pubblicazione. |

## Review end-to-end

1. PostgreSQL è stato ricreato da un bind mount vuoto.
2. Il primo `alembic upgrade head` ha creato `users` e `vat_rates`.
3. Il secondo upgrade non ha eseguito operazioni.
4. `alembic current` ha restituito `655402dd511f (head)`.
5. Metadata e database contengono soltanto User e VATRate.
6. Colonne, nullability, timestamp, PK e vincoli univoci coincidono.
7. `alembic check` non ha rilevato operazioni mancanti.
8. `alembic downgrade base` e il successivo upgrade hanno avuto esito positivo.
9. Il backend è partito senza creazione implicita dello schema.
10. `/`, `/docs` e `/openapi.json` hanno restituito HTTP 200.
11. OpenAPI 3.1.0 espone `/`, `/vat-rates/` e `/vat-rates/{vat_id}`.
12. Category è rimasta esclusa.

## Regressioni potenziali

- Le installazioni con la vecchia baseline devono ricreare il database come autorizzato da DECISION-0001.
- I problemi transazionali e di validazione VAT restano assegnati a TASK-0015.
- Category e gli altri file locali non tracciati restano incompleti ed esclusi dalla metadata.

## Checklist

- [x] Import e avvio
- [x] Modelli baseline
- [x] Unica dipendenza database
- [x] Upgrade e downgrade
- [x] Idempotenza
- [x] Configurazione unica
- [x] OpenAPI
- [x] Documentazione
- [ ] Test automatici
- [ ] Pubblicazione su `origin/main`

## Piano di consolidamento

1. Autorizzare il riallineamento Git preservando il working tree.
2. Pubblicare TASK-0014 e REVIEW-0014.
3. Portare TASK-0015 a Planned.
4. Consolidare transazioni, rollback, validazioni ed error handling VAT.
5. Aggiungere test automatici.
6. Rieseguire il quality gate prima di Categories.

## Decisioni richieste al maintainer

- Autorizzare la procedura Git necessaria a riallineare il branch locale senza force push e preservando tutte le modifiche preesistenti.

## Autorizzazione TASK-0015

La baseline soddisfa i prerequisiti tecnici di TASK-0015. L’esecuzione resta bloccata finché il consolidamento e REVIEW-0014 non sono pubblicati su `origin/main`.

## Conferma finale

Il database di sviluppo è stato ricreato secondo DECISION-0001. Nessun file Categories è stato modificato o incluso nella metadata. Le modifiche locali preesistenti fuori perimetro sono rimaste intatte. Non sono stati usati pull, merge, rebase, reset o stash.
