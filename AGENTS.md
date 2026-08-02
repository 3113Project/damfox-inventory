# DAMFOX Inventory — Codex bootstrap

Queste istruzioni sono obbligatorie per ogni attività svolta nel repository.

## 1. Rilevare l'ambiente

Prima di interpretare la richiesta, leggere:

- `docs/06_AI/WORKFLOWS/ENVIRONMENT_BOOTSTRAP.md`;
- le regole seguenti.

Verificare se il workspace dispone di un remote accessibile:

```bash
git remote get-url origin
```

L'assenza di `origin` è ammessa in Codex Cloud e non costituisce da sola una condizione di arresto.

## 2. Sincronizzare o usare lo snapshot corrente

### Remote `origin` presente e accessibile

Eseguire:

```bash
git fetch origin main
```

Se il fetch fallisce, fermarsi e riportare l'errore.

Leggere tramite `git show origin/main:<percorso>`:

- `AGENTS.md`;
- `docs/06_AI/AI_CONSTITUTION.md`;
- `docs/06_AI/AI_STATE.md`;
- `docs/06_AI/CODEX_WORKFLOW.md`;
- `docs/06_AI/GIT_WORKFLOW.md`;
- indice, TASK o OPS richiesti;
- decisioni, review e altri documenti AI indicati.

### Remote `origin` assente

Usare il workspace fornito dall'ambiente come snapshot operativo della sorgente selezionata all'avvio del task.

Leggere direttamente gli stessi file dal filesystem del workspace. Non tentare di configurare `origin`, non chiedere credenziali del server DAMFOX e non arrestarsi soltanto perché `git fetch origin main` non è disponibile.

Fermarsi invece se i documenti richiesti mancano o se `AI_STATE.md`, gli indici e l'attività richiesta sono incoerenti.

## 3. Documentazione tecnica su richiesta

Le cartelle seguenti non devono essere lette integralmente a ogni esecuzione:

- `docs/00_Project/`
- `docs/01_Development/`
- `docs/02_Database/`
- `docs/03_Business/`
- `docs/04_UI/`
- `docs/05_Project_Management/`

Leggere soltanto i documenti richiesti dal task o strettamente necessari.

## 4. Proteggere il workspace

Non usare automaticamente:

- `git pull`;
- merge;
- rebase;
- reset;
- stash;
- force push;
- checkout o restore massivi.

Queste operazioni sono consentite soltanto quando un file `OPS-XXXX.md` le autorizza esplicitamente.

Non sovrascrivere, includere nello staging o pubblicare modifiche non correlate.

## 5. Comandi sintetici

### `Esegui TASK-XXXX`

1. applicare il bootstrap adatto all'ambiente;
2. leggere `AI_STATE.md`, `TASK_INDEX.md` e il task richiesto;
3. applicare Costituzione, workflow e decisioni;
4. eseguire il task;
5. produrre la Engineering Review;
6. aggiornare lo stato previsto;
7. pubblicare secondo le capacità dell'ambiente: push locale autorizzato oppure branch/pull request cloud.

### `Esegui OPS-XXXX`

Leggere l'indice Operations e l'operation richiesta, verificare lo stato Git reale ed eseguire esclusivamente la procedura autorizzata.

### `Esegui l'ultimo task`

Usare `current_task` in `AI_STATE.md` e verificare che risulti `Planned` in `TASK_INDEX.md`.

### `Esegui l'ultima operation`

Individuare nell'indice la prima operation `Planned` con prerequisiti soddisfatti.

### `Controlla ed esegui tutti i nuovi task`

1. applicare il bootstrap adatto all'ambiente;
2. leggere `docs/06_AI/WORKFLOWS/AUTONOMOUS_TASK_QUEUE.md`;
3. eseguire in ordine i task `Planned` autorizzati;
4. rileggere stato e coda dopo ogni task usando la fonte disponibile;
5. proseguire finché la tranche è esaurita o si verifica una condizione di arresto.

## 6. Gerarchia delle regole

1. decisione esplicita del maintainer;
2. `AI_CONSTITUTION.md`;
3. `AGENTS.md`;
4. `CODEX_WORKFLOW.md` e `GIT_WORKFLOW.md`;
5. TASK o OPS richiesto;
6. altri documenti di progetto.

Non risolvere autonomamente contraddizioni sostanziali: segnalarle e fermarsi.
