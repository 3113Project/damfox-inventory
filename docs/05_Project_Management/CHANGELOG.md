# Changelog

## Unreleased

### Changed

- Completato il modulo Categories con modello gerarchico, schemi, service CRUD, router e PATCH parziale.
- Applicate unicità normalizzata per fratelli, protezione da cicli e conflitto sulla cancellazione dei nodi con figli.
- Aggiunta la migrazione reversibile `a4c5d6e7f8b9` e registrata Category nella metadata ORM.

- Consolidato il modulo VAT con validazioni di descrizione e aliquota.
- Sostituito PUT con PATCH per gli aggiornamenti parziali VAT.
- Aggiunti rollback transazionali ed errori HTTP 404 e 409 deterministici.
- Aggiunto il vincolo PostgreSQL `ck_vat_rates_rate_range`.

- Consolidata la baseline Alembic per `users` e `vat_rates`, inclusi timestamp e vincoli deterministici.
- Rimossa la creazione implicita dello schema dall’avvio FastAPI.
- Unificata la configurazione `DATABASE_URL` tra applicazione e Alembic.
- Ridotta a una sola implementazione canonica la dipendenza `get_db`.

### Verified

- Suite Categories: 6 test automatici verdi nel container; suite backend completa: 12 test verdi.
- Verificati database vuoto → upgrade, downgrade/upgrade Categories e `alembic check`.

- Suite VAT: 6 test automatici verdi nel container.
- Validati estremi `0.00` e `100.00`, fuori intervallo, scala, null e duplicati.
- Verificati rollback, CRUD, PATCH, 404, OpenAPI e migrazione reversibile.

- Ricreazione completa del database di sviluppo da zero tramite Alembic.
- Idempotenza di `alembic upgrade head`.
- Coerenza tra metadata ORM e schema PostgreSQL.
- Disponibilità degli endpoint `/`, `/docs` e `/openapi.json`.
