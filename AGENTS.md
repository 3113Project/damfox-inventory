# DAMFOX Inventory — Codex bootstrap

Queste istruzioni sono obbligatorie per ogni attività svolta nel repository.

## 1. Sincronizzare sempre il contesto operativo

Prima di interpretare o eseguire una richiesta del maintainer:

```bash
git fetch origin main
```

Se il fetch fallisce, fermarsi e riportare l'errore. Non lavorare usando istruzioni locali potenzialmente obsolete.

## 2. Leggere la fonte di verità da `origin/main`

Dopo il fetch, leggere sempre tramite `git show`:

```bash
git show origin/main:AGENTS.md
git show origin/main:docs/06_AI/AI_CONSTITUTION.md
git show origin/main:docs/06_AI/AI_STATE.md
git show origin/main:docs/06_AI/CODEX_WORKFLOW.md
git show origin/main:docs/06_AI/GIT_WORKFLOW.md
```

Per un task applicativo leggere inoltre:

```bash
git show origin/main:docs/06_AI/TASKS/TASK-XXXX.md
```

Per un'operation leggere:

```bash
git show origin/main:docs/06_AI/OPERATIONS/OPS-XXXX.md
```

Leggere da `origin/main` anche decisioni, review e altri documenti `06_AI` indicati dall'attività.

## 3. Documentazione tecnica su richiesta

Le cartelle seguenti non devono essere lette integralmente a ogni esecuzione:

- `docs/00_Project/`
- `docs/01_Development/`
- `docs/02_Database/`
- `docs/03_Business/`
- `docs/04_UI/`
- `docs/05_Project_Management/`

Leggere soltanto i documenti richiesti dal task o strettamente necessari per comprenderne il perimetro.

## 4. Proteggere il working tree

Il fetch e la lettura tramite `git show` non devono modificare il working tree.

Non usare automaticamente:

- `git pull`;
- merge;
- rebase;
- reset;
- stash;
- force push;
- checkout o restore massivi.

Queste operazioni sono consentite soltanto quando un file `OPS-XXXX.md` le autorizza esplicitamente e ne definisce la procedura.

Non sovrascrivere, includere nello staging o pubblicare modifiche locali non correlate.

## 5. Comandi sintetici

### `Esegui TASK-XXXX`

1. applicare questo bootstrap;
2. leggere `AI_STATE.md` e `TASK_INDEX.md` da `origin/main`;
3. leggere il task da `origin/main`;
4. applicare `AI_CONSTITUTION.md`, `CODEX_WORKFLOW.md` e `GIT_WORKFLOW.md`;
5. leggere soltanto il contesto tecnico richiesto;
6. eseguire il task;
7. produrre e pubblicare la Engineering Review;
8. aggiornare lo stato operativo previsto dal task.

### `Esegui OPS-XXXX`

1. applicare questo bootstrap;
2. leggere `OPERATIONS/OPS_INDEX.md` e l'operation da `origin/main`;
3. verificare lo stato Git reale;
4. eseguire esclusivamente la procedura autorizzata;
5. produrre il report operativo previsto.

### `Esegui l'ultimo task`

Usare `current_task` in `AI_STATE.md` e verificare che lo stesso task risulti `Planned` in `TASK_INDEX.md`. In caso di incoerenza, fermarsi.

### `Esegui l'ultima operation`

Leggere `OPERATIONS/OPS_INDEX.md`, individuare l'operation `Planned` con numero più basso compatibile con i prerequisiti ed eseguirla. In caso di ambiguità, fermarsi.

## 6. Gerarchia delle regole

In caso di conflitto tra istruzioni applicare questo ordine:

1. decisione esplicita del maintainer;
2. `AI_CONSTITUTION.md`;
3. `AGENTS.md`;
4. `CODEX_WORKFLOW.md` e `GIT_WORKFLOW.md`;
5. TASK o OPS richiesto;
6. altri documenti di progetto.

Non risolvere autonomamente contraddizioni sostanziali: segnalarle e fermarsi.
