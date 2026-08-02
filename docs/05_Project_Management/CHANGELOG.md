# Changelog

## Unreleased

### Changed

- Fissate le versioni delle dipendenze Python dirette e aggiunti healthcheck PostgreSQL/backend con script readiness riutilizzabile.

- Aggiunti barcode multipli, codice produttore e ricerca catalogo case-insensitive senza dipendenze esterne.

- Aggiunte Product Families, associazione facoltativa Products, cancellazione protetta e filtro per famiglia.

- Implementato il nucleo Products con SKU immutabile, Category facoltativa, VAT obbligatoria, CRUD PATCH e migrazione reversibile.

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

- Build senza cache con versioni fissate, readiness con timeout, database vuoto e suite catalogo verificati.

- Quality gate catalogo base: build senza cache, database vuoto, 22 test, OpenAPI, metadata e ciclo completo delle revisioni catalogo verificati.

- Suite catalogo identificativi: 22 test verdi; ricerca multi-campo, unicità barcode e zeri iniziali verificati.

- Suite con Product Families: 19 test verdi e migrazione reversibile verificata.

- Suite backend con Products: 16 test verdi; verificati SKU normalizzato, FK, OpenAPI e ciclo migrazione Products.

- Completato il quality gate delle fondamenta su immagine backend ricostruita senza cache e database PostgreSQL ricreato da zero.
- Confermati import, avvio, stato, Swagger, OpenAPI, metadata, migrazioni, rollback e assenza di segreti tracciati.

- Suite Categories: 6 test automatici verdi nel container; suite backend completa: 12 test verdi.
- Verificati database vuoto → upgrade, downgrade/upgrade Categories e `alembic check`.

- Suite VAT: 6 test automatici verdi nel container.
- Validati estremi `0.00` e `100.00`, fuori intervallo, scala, null e duplicati.
- Verificati rollback, CRUD, PATCH, 404, OpenAPI e migrazione reversibile.

- Ricreazione completa del database di sviluppo da zero tramite Alembic.
- Idempotenza di `alembic upgrade head`.
- Coerenza tra metadata ORM e schema PostgreSQL.
- Disponibilità degli endpoint `/`, `/docs` e `/openapi.json`.
