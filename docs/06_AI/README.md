# Sistema Task, Operation e collaborazione AI

La cartella `06_AI` contiene la memoria operativa per definire, eseguire e verificare le attività assistite da AI di DAMFOX Inventory.

## Livelli del contesto

### Bootstrap permanente

[`../../AGENTS.md`](../../AGENTS.md) contiene le istruzioni minime che Codex deve applicare prima di ogni attività: fetch del remoto, lettura della memoria AI da `origin/main` e protezione del working tree.

### Costituzione AI

[AI_CONSTITUTION.md](AI_CONSTITUTION.md) definisce ruoli, fonti di verità, regole non negoziabili, differenza tra task e operation e criteri di completamento.

### Stato operativo

[AI_STATE.md](AI_STATE.md) riassume il task corrente, l'ultima review, i prossimi task, i blocchi e le decisioni attive.

### Memoria operativa AI

La versione ufficiale di task, operation, review, decisioni e workflow deve essere letta da `origin/main` tramite `git show` dopo il fetch obbligatorio.

### Knowledge di progetto

Le cartelle `00_Project`–`05_Project_Management` contengono architettura, standard, database, regole di business, UI e gestione del progetto. Codex le legge solo quando richieste dall'attività o strettamente necessarie.

## Ruoli

Maintainer → decide e approva.

ChatGPT → Tech Lead: prepara task, operation e decisioni; revisiona GitHub.

Codex → Developer: opera localmente, implementa, testa, pubblica review e report.

## Tipi di attività

### Task applicativi

I file `TASK-XXXX.md` riguardano sviluppo del prodotto, database, test, refactoring e documentazione funzionale.

Ogni task produce:

`TASK-XXXX.md` → `REVIEWS/REVIEW-XXXX.md`

### Operation tecniche

I file `OPS-XXXX.md` riguardano rebase, conflitti, sincronizzazione, pubblicazione, release, infrastruttura e manutenzione del repository.

Quando previsto producono:

`OPS-XXXX.md` → `OPERATIONS/REPORTS/OPS-XXXX-REPORT.md`

## Struttura

- [AI_CONSTITUTION.md](AI_CONSTITUTION.md): costituzione del workflow AI.
- [AI_STATE.md](AI_STATE.md): stato operativo corrente.
- [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md): workflow obbligatorio di esecuzione.
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md): regole Git, commit e push.
- [TASK_INDEX.md](TASK_INDEX.md): registro dei task applicativi.
- [TASKS/](TASKS/): task individuali.
- [REVIEWS/](REVIEWS/): Engineering Review dei task.
- [OPERATIONS/](OPERATIONS/): operation tecniche, indice, template e report.
- [DECISIONS/](DECISIONS/): decisioni operative e architetturali.
- [PROMPTS/](PROMPTS/): prompt riutilizzabili o versionati.
- [WORKFLOWS/](WORKFLOWS/): workflow specializzati o storici.

## Comandi sintetici

```text
Esegui TASK-XXXX
Esegui l'ultimo task
Esegui OPS-XXXX
Esegui l'ultima operation
```

In ogni caso Codex deve prima applicare `AGENTS.md`, leggere la Costituzione AI e lo stato remoto, verificare l'indice pertinente e caricare l'attività da `origin/main`.
