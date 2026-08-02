# Sistema Task e collaborazione AI

La cartella `06_AI` contiene il sistema documentale per definire, eseguire e verificare i task di DAMFOX Inventory.

## Workflow di collaborazione

Maintainer → ChatGPT prepara o revisiona il task → Codex esegue il task localmente → Codex crea commit e push se autorizzato → Codex archivia una Engineering Review → GitHub diventa la fonte di verità → ChatGPT legge GitHub ed esegue la review → il maintainer testa e approva.

Il maintainer mantiene sempre il controllo su priorità, autorizzazioni, test reali e release.

## Struttura

- [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md): workflow obbligatorio di esecuzione per Codex.
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

## Come utilizzare il sistema

1. Il maintainer o ChatGPT definisce il task.
2. Codex legge il task, il workflow e i documenti richiesti.
3. Codex esegue soltanto il perimetro autorizzato.
4. Codex verifica il risultato e applica le istruzioni Git.
5. Codex crea o aggiorna la Engineering Review del task.
6. Dopo il push, GitHub rappresenta la versione ufficiale da analizzare.
7. ChatGPT legge task, codice e review direttamente da GitHub.
8. Il maintainer prende le decisioni funzionali e approva il risultato.
