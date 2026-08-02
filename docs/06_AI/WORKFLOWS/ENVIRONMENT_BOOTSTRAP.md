# Bootstrap Codex indipendente dall'ambiente

Questo workflow rende identici i comandi del maintainer in VS Code locale, Codex Web/Cloud, container e CI.

## Principio

GitHub `main` resta la fonte condivisa di verità. Il workspace corrente è la copia operativa su cui Codex lavora.

Codex deve rilevare le capacità reali dell'ambiente senza assumere che esista un remote Git chiamato `origin`.

## Rilevamento

1. Verificare che la root del workspace contenga `AGENTS.md` e `docs/06_AI/`.
2. Verificare se esiste un remote accessibile:

```bash
git remote get-url origin
```

3. Se `origin` esiste ed è accessibile, usare il bootstrap sincronizzato locale.
4. Se `origin` è assente, come può accadere in Codex Cloud, usare il workspace fornito come snapshot della fonte selezionata all'avvio del task.
5. L'assenza di `origin` non è un errore nel cloud e non deve arrestare il task.

## Bootstrap con remote accessibile

```bash
git fetch origin main
```

Leggere i documenti operativi da `origin/main` tramite `git show`.

Se il fetch fallisce nonostante `origin` sia configurato, fermarsi: il workspace locale potrebbe essere obsoleto.

## Bootstrap senza remote

Leggere direttamente dal workspace corrente:

- `AGENTS.md`;
- `docs/06_AI/AI_CONSTITUTION.md`;
- `docs/06_AI/AI_STATE.md`;
- `docs/06_AI/CODEX_WORKFLOW.md`;
- `docs/06_AI/GIT_WORKFLOW.md`;
- indice, task o operation richiesti;
- decisioni, review e knowledge indicate dall'attività.

Prima di procedere verificare che il task richiesto esista e che lo stato locale sia coerente. Non tentare di creare artificialmente `origin` e non chiedere credenziali del server DAMFOX.

## Pubblicazione

- Ambiente locale con remote: seguire `GIT_WORKFLOW.md` e verificare il fast-forward.
- Codex Cloud: lavorare sulla branch gestita dall'ambiente e aprire una pull request quando il task lo richiede; non è necessario che il workspace esponga un remote `origin` alla shell.
- CI o sandbox senza pubblicazione: produrre commit, patch o artefatti secondo il task e dichiarare chiaramente il limite.

## Comandi invarianti

I seguenti comandi del maintainer devono avere lo stesso significato in ogni ambiente:

- `Esegui TASK-XXXX`;
- `Esegui l'ultimo task`;
- `Controlla ed esegui tutti i nuovi task`;
- `Esegui OPS-XXXX`.

Codex adatta soltanto il bootstrap e la modalità di pubblicazione, non requisiti, test, criteri o condizioni di arresto.

## Arresto obbligatorio

Fermarsi quando:

- mancano i documenti operativi nel workspace;
- task, indice e stato sono incoerenti;
- un remote configurato non è accessibile e la copia locale potrebbe essere obsoleta;
- è richiesta una decisione funzionale o architetturale;
- la pubblicazione prevista non è supportata dall'ambiente;
- esiste rischio di perdita di dati o di modifiche non correlate.
