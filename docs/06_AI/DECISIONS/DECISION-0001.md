# DECISION-0001 — Database di sviluppo ricreabile

## Stato

Accepted

## Contesto

Il progetto è ancora in fase iniziale e il database non contiene dati aziendali o operativi da preservare. Le migrazioni esistenti sono incoerenti con i modelli e `Base.metadata.create_all()` può mascherare tali difetti.

## Decisione del maintainer

Il database attuale può essere eliminato e ricreato durante il consolidamento della baseline. Fino a nuova decisione documentata, i dati presenti sono considerati dati di sviluppo ricreabili.

Alembic deve diventare l'unica fonte di verità per la creazione e l'evoluzione dello schema.

## Conseguenze

- È consentito ricreare il volume PostgreSQL durante TASK-0014.
- La baseline Alembic può essere riscritta in modo coerente.
- `Base.metadata.create_all()` deve essere rimosso.
- Dopo la nuova baseline, ogni modifica strutturale dovrà passare da una migrazione.
- Prima dell'introduzione di dati reali dovrà essere revocata esplicitamente la natura sacrificabile del database.

## Collegamenti

- REVIEW-0010
- TASK-0014
- PROJECT_CONSTITUTION.md, principi 3 e 8
