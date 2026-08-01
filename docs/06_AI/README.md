# Sistema Task e collaborazione AI

La cartella `06_AI` contiene il sistema documentale per definire, eseguire e verificare i task di DAMFOX Inventory.

## Workflow di collaborazione

Maintainer → ChatGPT prepara o revisiona il task → Codex esegue il task localmente → Codex crea il commit e, se autorizzato, il push → GitHub diventa la fonte di verità → ChatGPT legge GitHub ed esegue la review → il maintainer testa e approva.

Il maintainer mantiene sempre il controllo su priorità, autorizzazioni, test reali e release.

## Documenti del sistema

- [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md): workflow obbligatorio di esecuzione per Codex.
- [GIT_WORKFLOW.md](GIT_WORKFLOW.md): regole Git, commit e push.
- [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md): schema per prompt deterministici destinati a Codex.
- [TASK_TEMPLATE.md](TASK_TEMPLATE.md): modello standard di un task.
- [TASK_INDEX.md](TASK_INDEX.md): registro cronologico dei task.
- [TASKS/](TASKS/): archivio dei file di task individuali.

## Come utilizzare il sistema Task

1. Il maintainer o ChatGPT definisce il task con [TASK_TEMPLATE.md](TASK_TEMPLATE.md).
2. Il task dichiara perimetro, verifiche, condizioni di arresto e istruzioni Git.
3. Codex legge i documenti obbligatori e applica [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md) e [GIT_WORKFLOW.md](GIT_WORKFLOW.md).
4. Il task storico viene registrato in [TASKS/](TASKS/) e l'indice viene aggiornato.
5. Dopo il push autorizzato, GitHub rappresenta la versione ufficiale da analizzare e revisionare.
