# Sistema Task e collaborazione AI

La cartella `06_AI` contiene il sistema documentale con cui maintainer, ChatGPT e Codex definiscono, eseguono e verificano i task di DAMFOX Inventory.

## Documenti del sistema

- `TASK_INDEX.md`: registro cronologico e descrittivo dei task esistenti.
- `TASK_TEMPLATE.md`: modello standard di un task.
- `PROMPT_TEMPLATE.md`: schema per scrivere prompt completi per Codex.
- `CODEX_WORKFLOW.md`: processo obbligatorio di esecuzione di un task.
- `TASKS/`: archivio dei file di task individuali quando verranno creati.

## Come usare il sistema Task

1. Assegnare il prossimo identificativo progressivo e registrarlo in `TASK_INDEX.md`.
2. Creare, quando necessario, un file in `TASKS/` a partire da `TASK_TEMPLATE.md`.
3. Preparare il prompt per Codex usando `PROMPT_TEMPLATE.md`.
4. Indicare contesto, obiettivo, file coinvolti, operazioni, vincoli, autoverifica e formato dell'output.
5. Codex applica `CODEX_WORKFLOW.md`, verifica i criteri di completamento e si ferma al termine.

## Collaborazione tra ChatGPT, Codex e maintainer

Il maintainer definisce priorità, autorizzazioni e decisioni. ChatGPT può aiutare a chiarire requisiti, organizzare il task e preparare il prompt. Codex esegue esclusivamente il task autorizzato e restituisce il riepilogo richiesto. Ogni modifica o attività successiva richiede un nuovo incarico esplicito.
