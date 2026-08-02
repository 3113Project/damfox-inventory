# AI State

Stato operativo sintetico del progetto DAMFOX Inventory per ChatGPT e Codex.

Questo file non sostituisce `TASK_INDEX.md`, le decisioni o le Engineering Reviews. Riassume soltanto lo stato corrente e deve essere aggiornato quando cambia il task attivo o un blocco principale.

## Stato corrente

```yaml
state_version: 1
current_milestone: Foundations Completed
current_task: null
current_task_status: null
last_completed_task: TASK-0017
last_review: REVIEW-0017
last_review_verdict: APPROVATO CON RISERVE
next_tasks: []
blocked_tasks: []
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
- In caso di incoerenza tra questo file e `TASK_INDEX.md`, fermarsi e segnalarla senza scegliere autonomamente quale stato applicare.

## Contesto corrente

- La baseline database è consolidata.
- Alembic è l’unica fonte di verità dello schema.
- Il modulo VAT è consolidato e coperto da test automatici.
- Categories è consolidato e coperto da test automatici.
- Il quality gate delle fondamenta è completato.
- Products è autorizzato dalla REVIEW-0017, ma richiede un task esplicito prima dell’implementazione.
- Il versionamento delle dipendenze resta una riserva non bloccante da risolvere prima della release 1.0.
