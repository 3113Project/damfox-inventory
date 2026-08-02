# AI State

Stato operativo sintetico del progetto DAMFOX Inventory per ChatGPT e Codex.

Questo file non sostituisce `TASK_INDEX.md`, le decisioni o le Engineering Reviews. Riassume soltanto lo stato corrente e deve essere aggiornato quando cambia il task attivo o un blocco principale.

## Stato corrente

```yaml
state_version: 1
current_milestone: Primo frontend operativo
current_task: TASK-0030
current_task_status: Planned
last_completed_task: TASK-0029
last_review: REVIEW-0029
last_review_verdict: APPROVATO
next_tasks: []
blocked_tasks: []
active_decisions:
  - DECISION-0001
  - DECISION-0002
  - DECISION-0003
  - DECISION-0004
  - DECISION-0005
source_of_truth: origin/main
execution_mode: local_vscode_server
```

## Regole di interpretazione

- `current_task` è il task da eseguire quando il maintainer scrive `Esegui l’ultimo task`.
- Prima dell’esecuzione, verificare che il task risulti `Planned` anche in `TASK_INDEX.md`.
- `last_review` indica la review da leggere come prerequisito più recente.
- I task elencati in `blocked_tasks` non devono essere eseguiti finché la review precedente non li autorizza.
- In caso di incoerenza tra questo file e `TASK_INDEX.md`, fermarsi senza scegliere autonomamente quale stato applicare.
- La tranche deve essere eseguita localmente in VS Code sul server, con Docker e backend reali.
- La coda deve arrestarsi dopo TASK-0030.

## Contesto corrente

- Fondamenta, catalogo prodotti e unità di misura hanno superato i rispettivi quality gate.
- DECISION-0005 stabilisce React, TypeScript, Vite, React Router e TanStack Query come fondazione frontend.
- TASK-0027 ha creato il progetto frontend e l'integrazione runtime.
- TASK-0028 ha prodotto il primo app shell visibile e responsivo.
- TASK-0029 ha reso operativo il catalogo prodotti dal browser.
- TASK-0030 esegue il quality gate end-to-end, è il task attivo e chiude la tranche.
