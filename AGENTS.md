# DAMFOX Inventory — Codex bootstrap

Queste istruzioni sono obbligatorie per ogni attività svolta nel repository.

## 1. Sincronizzare sempre il contesto operativo

Prima di interpretare o eseguire una nuova richiesta del maintainer:

```bash
git fetch origin main
```

Se il fetch fallisce, fermarsi e riportare l'errore. Non lavorare usando istruzioni locali potenzialmente obsolete.

## 2. Bootstrap completo

All'inizio di una nuova attività o tranche leggere tramite `git show origin/main:<percorso>`:

- `AGENTS.md`;
- `docs/06_AI/AI_CONSTITUTION.md`;
- `docs/06_AI/AI_STATE.md`;
- `docs/06_AI/CODEX_WORKFLOW.md`;
- `docs/06_AI/GIT_WORKFLOW.md`;
- indice e file dell'attività richiesta;
- decisioni, review e altri documenti `06_AI` indicati dall'attività.

Per una coda autonoma leggere inoltre:

- `docs/06_AI/WORKFLOWS/AUTONOMOUS_TASK_QUEUE.md`;
- `docs/06_AI/WORKFLOWS/LEAN_AUTONOMOUS_EXECUTION.md`.

Il bootstrap completo va eseguito **una sola volta per tranche autonoma**. Tra task consecutivi della stessa tranche non rileggere documenti invariati già acquisiti: seguire il contesto incrementale definito in `LEAN_AUTONOMOUS_EXECUTION.md`.

## 3. Documentazione tecnica su richiesta

Le cartelle seguenti non devono essere lette integralmente:

- `docs/00_Project/`
- `docs/01_Development/`
- `docs/02_Database/`
- `docs/03_Business/`
- `docs/04_UI/`
- `docs/05_Project_Management/`

Leggere soltanto i documenti richiesti dal task o strettamente necessari. Preferire ricerca mirata e porzioni pertinenti dei file invece di ristampare documenti lunghi già letti.

## 4. Proteggere il working tree

Il fetch e la lettura tramite `git show` non devono modificare il working tree.

Non usare automaticamente `git pull`, merge non autorizzati, rebase, reset, stash, force push, checkout o restore massivi.

Le eccezioni sono consentite soltanto quando un file OPS o il workflow della coda autorizza esplicitamente una procedura deterministica, come il fast-forward sicuro.

Non sovrascrivere, includere nello staging o pubblicare modifiche locali non correlate.

## 5. Comandi sintetici

### `Esegui TASK-XXXX`

1. applicare il bootstrap completo;
2. leggere `AI_STATE.md`, `TASK_INDEX.md` e il task da `origin/main`;
3. verificare che lo stato esatto sia `Planned`;
4. rifiutare task `Completed`, `Superseded`, retrospettivi o marcati come archivio non eseguibile; `TASK-0001`–`TASK-0007` sono storici;
5. leggere soltanto il contesto tecnico necessario;
6. eseguire il task, verifiche richieste, commit, Engineering Review e aggiornamento stato.

### `Esegui OPS-XXXX`

Applicare il bootstrap completo, leggere `OPS_INDEX.md` e l'operation, verificare lo stato Git reale ed eseguire esclusivamente la procedura autorizzata producendo il report previsto.

### `Esegui l'ultimo task`

Usare `current_task` in `AI_STATE.md` e verificare che risulti `Planned` in `TASK_INDEX.md`. In caso di incoerenza, fermarsi.

### `Esegui l'ultima operation`

Leggere `OPS_INDEX.md`, individuare l'operation `Planned` con numero più basso compatibile con i prerequisiti ed eseguirla. In caso di ambiguità, fermarsi.

### `Controlla ed esegui tutti i nuovi task`

1. eseguire un solo bootstrap completo della tranche;
2. leggere `AUTONOMOUS_TASK_QUEUE.md` e `LEAN_AUTONOMOUS_EXECUTION.md`;
3. individuare tutti i task `Planned` eseguibili;
4. eseguirli in ordine progressivo senza attendere un nuovo comando;
5. tra task consecutivi usare solo contesto incrementale: stato, indice, review precedente, task successivo e documenti realmente cambiati;
6. usare test e review mirati nei task intermedi e verifiche complete nel quality gate finale;
7. fermarsi soltanto alle condizioni definite dal workflow della coda.

## 6. Gerarchia delle regole

1. decisione esplicita del maintainer;
2. `AI_CONSTITUTION.md`;
3. `AGENTS.md`;
4. `CODEX_WORKFLOW.md`, `GIT_WORKFLOW.md` e workflow della coda;
5. TASK o OPS richiesto;
6. altri documenti di progetto.

Non risolvere autonomamente contraddizioni sostanziali: segnalarle e fermarsi.