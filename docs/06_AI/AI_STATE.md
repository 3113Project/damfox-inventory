# AI State

Stato operativo sintetico del progetto DAMFOX Inventory per ChatGPT e Codex.

Questo file non sostituisce `TASK_INDEX.md`, le decisioni o le Engineering Reviews. Riassume soltanto lo stato corrente e deve essere aggiornato quando cambia il task attivo o un blocco principale.

## Stato corrente

```yaml
state_version: 1
current_milestone: Foundations
current_task: TASK-0015
current_task_status: Planned
last_completed_task: TASK-0014
last_review: REVIEW-0014
last_review_verdict: APPROVATO_CON_RISERVE
next_tasks:
  - TASK-0016
  - TASK-0017
blocked_tasks:
  - task: TASK-0016
    reason: Richiede REVIEW-0015 approvata.
  - task: TASK-0017
    reason: Richiede REVIEW-0016 approvata.
active_decisions:
  - DECISION-0001
  - DECISION-0002
  - DECISION-0003
  - DECISION-0004
source_of_truth: origin/main
```

## Regole di interpretazione

- `current_task` è il task da eseguire quando il maintainer scrive `Esegui l'ultimo task`.
- Prima dell'esecuzione, verificare che il task risulti `Planned` anche in `TASK_INDEX.md`.
- `last_review` indica la review da leggere come prerequisito più recente.
- I task elencati in `blocked_tasks` non devono essere eseguiti finché la condizione indicata non è soddisfatta.
- In caso di incoerenza tra questo file e `TASK_INDEX.md`, fermarsi e segnalarla senza scegliere autonomamente quale stato applicare.

## Contesto corrente

- La baseline database è stata consolidata e pubblicata.
- Alembic è l'unica fonte di verità dello schema.
- Il database di sviluppo può essere ricreato secondo `DECISION-0001`.
- Il modulo VAT è il task attivo.
- L'intervallo valido per `rate` è `0.00–100.00` inclusi, con massimo due cifre decimali, secondo `DECISION-0004`.
- I file Categories locali devono restare fuori dal perimetro di TASK-0015.
