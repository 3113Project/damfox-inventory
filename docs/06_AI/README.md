# Sistema Task e collaborazione AI

La cartella `06_AI` contiene la memoria operativa per definire, eseguire e verificare i task di DAMFOX Inventory.

## Livelli del contesto

### Bootstrap permanente

[`../../AGENTS.md`](../../AGENTS.md) contiene le istruzioni minime che Codex deve applicare prima di ogni attività: fetch del remoto, lettura della memoria AI da `origin/main` e protezione del working tree.

### Stato operativo

[AI_STATE.md](AI_STATE.md) riassume il task corrente, l'ultima review, i prossimi task, i blocchi e le decisioni attive.

### Memoria operativa AI

La cartella `06_AI` contiene task, review, decisioni e workflow. Per Codex, la versione ufficiale deve essere letta da `origin/main` tramite `git show` dopo il fetch obbligatorio.

### Knowledge di progetto

Le cartelle `00_Project`–`05_Project_Management` contengono architettura, standard, database, regole di business, UI e gestione del progetto. Codex le legge solo quando il task le richiede o quando sono strettamente necessarie per comprenderne il perimetro.

## Workflow di collaborazione

Maintainer → ChatGPT prepara o revisiona il task e aggiorna GitHub → Codex legge bootstrap e stato remoto → Codex esegue il task localmente → Codex crea commit e push se autorizzato → Codex archivia una Engineering Review → ChatGPT legge GitHub ed esegue la review → il maintainer testa e approva.

Il maintainer mantiene sempre il controllo su priorità, autorizzazioni, test reali e release.

## Struttura

- [AI_STATE.md](AI_STATE.md): stato operativo corrente.
- [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md): workflow obbligatorio di esecuzione.
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md): regole Git, commit e push.
- [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md): schema per prompt deterministici.
- [TASK_TEMPLATE.md](TASK_TEMPLATE.md): modello standard di un task.
- [TASK_INDEX.md](TASK_INDEX.md): registro cronologico dei task.
- [TASKS/](TASKS/): task individuali.
- [REVIEWS/](REVIEWS/): Engineering Reviews collegate ai task.
- [DECISIONS/](DECISIONS/): decisioni operative nate dal lavoro AI.
- [PROMPTS/](PROMPTS/): prompt riutilizzabili o versionati.
- [WORKFLOWS/](WORKFLOWS/): workflow specializzati o storici.

## Regola task-review

Ogni task produce una review tecnica ufficiale:

`TASK-XXXX.md` → `REVIEWS/REVIEW-XXXX.md`

Le review usano uno dei verdetti:

- APPROVATO
- APPROVATO CON RISERVE
- NON APPROVATO
- NON APPLICABILE

## Comandi sintetici

Il maintainer può usare:

```text
Esegui TASK-XXXX
```

oppure:

```text
Esegui l'ultimo task
```

In entrambi i casi Codex deve prima applicare `AGENTS.md`, leggere `AI_STATE.md`, verificare `TASK_INDEX.md` e caricare il task da `origin/main`.
