# AI State

Stato operativo sintetico del progetto DAMFOX Inventory per ChatGPT e Codex.

Questo file non sostituisce `TASK_INDEX.md`, le decisioni o le Engineering Reviews. Riassume soltanto lo stato corrente e deve essere aggiornato quando cambia il task attivo o un blocco principale.

## Stato corrente

```yaml
state_version: 1
current_milestone: Cloud Workflow Pilot
current_task: TASK-0023
current_task_status: Planned
last_completed_task: TASK-0022
last_review: REVIEW-0022
last_review_verdict: APPROVATO
next_tasks: []
blocked_tasks: []
active_decisions:
  - DECISION-0001
  - DECISION-0002
  - DECISION-0003
  - DECISION-0004
source_of_truth: origin/main
execution_mode: codex_cloud_pull_request
```

## Regole di interpretazione

- `current_task` è il task da eseguire quando il maintainer scrive `Esegui l’ultimo task`.
- Prima dell’esecuzione, verificare che il task risulti `Planned` anche in `TASK_INDEX.md`.
- `last_review` indica la review da leggere come prerequisito più recente.
- I task elencati in `blocked_tasks` non devono essere eseguiti finché la condizione indicata non è soddisfatta.
- Nella coda autonoma, un task successivo può passare da `Blocked` a `Planned` solo dopo una review approvata che lo autorizzi esplicitamente.
- In caso di incoerenza tra questo file e `TASK_INDEX.md`, fermarsi e segnalarla senza scegliere autonomamente quale stato applicare.
- Quando `execution_mode` è `codex_cloud_pull_request`, Codex deve lavorare in ambiente cloud su branch dedicata e aprire una pull request senza modificare direttamente `main`.

## Contesto corrente

- Le fondamenta database, VAT e Categories hanno superato il quality gate.
- Il catalogo prodotti base è completato.
- TASK-0022 ha consolidato dipendenze e readiness.
- TASK-0023 è un pilot controllato di Codex Cloud.
- L'obiettivo funzionale del pilot è introdurre le unità di misura base e il collegamento facoltativo ai prodotti.
- Il risultato deve arrivare tramite pull request; merge e quality gate sul server restano sotto controllo del maintainer.
