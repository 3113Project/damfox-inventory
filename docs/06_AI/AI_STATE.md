# AI State

Stato operativo sintetico del progetto DAMFOX Inventory per ChatGPT e Codex.

Questo file non sostituisce `TASK_INDEX.md`, le decisioni o le Engineering Reviews. Riassume soltanto lo stato corrente e deve essere aggiornato quando cambia il task attivo o un blocco principale.

## Stato corrente

```yaml
state_version: 1
current_milestone: Catalogo operativo — Unità di misura
current_task: null
current_task_status: null
last_completed_task: TASK-0026
last_review: REVIEW-0026
last_review_verdict: APPROVATO
next_tasks: []
blocked_tasks: []
active_decisions:
  - DECISION-0001
  - DECISION-0002
  - DECISION-0003
  - DECISION-0004
source_of_truth: origin/main
execution_mode: local_vscode_server
```

## Regole di interpretazione

- `current_task` è il task da eseguire quando il maintainer scrive `Esegui l’ultimo task`.
- Prima dell’esecuzione, verificare che il task risulti `Planned` anche in `TASK_INDEX.md`.
- `last_review` indica la review da leggere come prerequisito più recente.
- I task elencati in `blocked_tasks` non devono essere eseguiti finché la condizione indicata non è soddisfatta.
- Nella coda autonoma, il task successivo passa da `Blocked` a `Planned` soltanto dopo una review approvata che lo autorizzi esplicitamente.
- In caso di incoerenza tra questo file e `TASK_INDEX.md`, fermarsi senza scegliere autonomamente quale stato applicare.
- Questa tranche deve essere eseguita localmente in VS Code sul server, con Docker e PostgreSQL reali.

## Contesto corrente

- Fondamenta, VAT, Categories e catalogo prodotti base hanno superato i rispettivi quality gate.
- TASK-0022 ha consolidato dipendenze e readiness.
- La nuova tranche è limitata a TASK-0023–TASK-0026 e a una durata stimata complessiva massima di circa cinque ore.
- TASK-0023 introduce le unità di misura con collegamento inizialmente facoltativo.
- TASK-0024 rende l’unità obbligatoria per la creazione di nuovi prodotti senza invalidare dati storici.
- TASK-0025 integra filtri e ricerca.
- TASK-0026 esegue il quality gate end-to-end e chiude la tranche.
