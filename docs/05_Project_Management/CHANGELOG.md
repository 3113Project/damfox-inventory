# Changelog

## Unreleased

### Changed

- Consolidata la baseline Alembic per `users` e `vat_rates`, inclusi timestamp e vincoli deterministici.
- Rimossa la creazione implicita dello schema dall’avvio FastAPI.
- Unificata la configurazione `DATABASE_URL` tra applicazione e Alembic.
- Ridotta a una sola implementazione canonica la dipendenza `get_db`.

### Verified

- Ricreazione completa del database di sviluppo da zero tramite Alembic.
- Idempotenza di `alembic upgrade head`.
- Coerenza tra metadata ORM e schema PostgreSQL.
- Disponibilità degli endpoint `/`, `/docs` e `/openapi.json`.
