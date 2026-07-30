# DAMFOX Inventory

## Obiettivo

Gestionale professionale per ferramenta.

Il progetto deve poter crescere nel tempo senza richiedere una riprogettazione del database o dell'architettura.

---

## Architettura

Backend:
- FastAPI

Database:
- PostgreSQL

ORM:
- SQLAlchemy 2.x

Migrazioni:
- Alembic

Frontend:
- (in sviluppo)

Mobile:
- previsto

Docker:
- ogni servizio separato

---

## Regole generali

- Tutte le modifiche al database passano da Alembic.
- Nessun dato sensibile nel codice.
- Configurazione centralizzata.
- API REST per ogni funzionalità.
- Ogni modifica importante viene documentata.