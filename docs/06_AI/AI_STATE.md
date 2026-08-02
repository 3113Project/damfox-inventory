# AI State

Stato operativo sintetico del progetto DAMFOX Inventory per ChatGPT e Codex.

Questo file non sostituisce `TASK_INDEX.md`, le decisioni o le Engineering Reviews. Riassume soltanto lo stato corrente e deve essere aggiornato quando cambia il task attivo o un blocco principale.

## Stato corrente

```yaml
state_version: 1
current_milestone: Product Catalog
current_task: TASK-0019
current_task_status: Planned
last_completed_task: TASK-0018
last_review: REVIEW-0018
last_review_verdict: APPROVATO
next_tasks:
  - TASK-0020
  - TASK-0021
  - TASK-0022
blocked_tasks:
  - task: TASK-0020
    reason: Richiede REVIEW-0019 approvata.
  - task: TASK-0021
    reason: Richiede REVIEW-0020 approvata.
  - task: TASK-0022
    reason: Richiede REVIEW-0021 approvata.
active_decisions:
  - DECISION-0001
  - DECISION-0002
  - DECISION-0003
  - DECISION-0004
source_of_truth: origin/main
```

## Regole di interpretazione

- `current_task` è il task da eseguire quando il maintainer scrive `Esegui l’ultimo task`.
- Prima dell’esecuzione, verificare che il task risulti `Planned` anche in `TASK_INDEX.md`.
- `last_review` indica la review da leggere come prerequisito più recente.
- I task elencati in `blocked_tasks` non devono essere eseguiti finché la condizione indicata non è soddisfatta.
- Nella coda autonoma, un task successivo può passare da `Blocked` a `Planned` solo dopo una review approvata che lo autorizzi esplicitamente.
- In caso di incoerenza tra questo file e `TASK_INDEX.md`, fermarsi e segnalarla senza scegliere autonomamente quale stato applicare.

## Contesto corrente

- Le fondamenta database, VAT e Categories hanno superato il quality gate.
- La milestone attiva è il catalogo prodotti.
- TASK-0018 ha completato il nucleo Products.
- TASK-0019 realizza Product Families.
- TASK-0019–TASK-0022 formano una coda sequenziale; ciascun task deve essere sbloccato dalla review del precedente.
- Il versionamento delle dipendenze resta una riserva non bloccante e verrà affrontato da TASK-0022.
