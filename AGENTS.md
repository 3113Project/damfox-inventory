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
git show origin/main:docs/06_AI/AI_STATE.md
git show origin/main:docs/06_AI/CODEX_WORKFLOW.md
git show origin/main:docs/06_AI/GIT_WORKFLOW.md
```

Per un task numerato leggere inoltre:

```bash
git show origin/main:docs/06_AI/TASKS/TASK-XXXX.md
```

Leggere da `origin/main` anche decisioni, review e altri documenti sotto `docs/06_AI/` indicati dal task.

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

Non sovrascrivere, includere nello staging o pubblicare modifiche locali non correlate.

## 5. Esecuzione sintetica

Quando il maintainer scrive `Esegui TASK-XXXX`:

1. applicare questo bootstrap;
2. leggere `AI_STATE.md`;
3. leggere il task da `origin/main`;
4. applicare `CODEX_WORKFLOW.md` e `GIT_WORKFLOW.md`;
5. leggere soltanto il contesto tecnico richiesto;
6. eseguire il task;
7. produrre e pubblicare la Engineering Review secondo il workflow.

Quando il maintainer scrive `Esegui l'ultimo task`, usare `current_task` in `AI_STATE.md`; verificare poi che lo stesso task risulti eseguibile in `TASK_INDEX.md`. In caso di incoerenza, fermarsi e riportarla.
