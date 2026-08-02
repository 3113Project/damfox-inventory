# Workflow ufficiale di esecuzione per Codex

Codex esegue solo attività esplicitamente richieste e rispetta sempre:

1. `docs/06_AI/AI_CONSTITUTION.md`;
2. `AGENTS.md`;
3. `docs/06_AI/GIT_WORKFLOW.md`;
4. il TASK o OPS richiesto.

## Bootstrap obbligatorio

Prima di interpretare qualsiasi comando:

```bash
git fetch origin main
```

Poi leggere da `origin/main` mediante `git show`:

- `AGENTS.md`;
- `docs/06_AI/AI_CONSTITUTION.md`;
- `docs/06_AI/AI_STATE.md`;
- `docs/06_AI/CODEX_WORKFLOW.md`;
- `docs/06_AI/GIT_WORKFLOW.md`;
- l'indice e il file dell'attività richiesta;
- decisioni, review e documenti AI indicati dall'attività.

Il bootstrap non modifica il working tree e non autorizza automaticamente pull, merge, rebase, reset, stash o force push.

Se il fetch fallisce, fermarsi.

## Comandi sintetici

### `Esegui TASK-XXXX`

Leggere da `origin/main` `TASK_INDEX.md`, `TASKS/TASK-XXXX.md` e i prerequisiti indicati. Eseguire il task e produrre `REVIEWS/REVIEW-XXXX.md`.

### `Esegui l'ultimo task`

Leggere `AI_STATE.md` e verificare che `current_task` risulti `Planned` anche in `TASK_INDEX.md`.

### `Esegui OPS-XXXX`

Leggere da `origin/main` `OPERATIONS/OPS_INDEX.md` e `OPERATIONS/OPS-XXXX.md`. Eseguire soltanto la procedura operativa autorizzata e produrre il report richiesto.

### `Esegui l'ultima operation`

Individuare in `OPS_INDEX.md` la prima operation `Planned` i cui prerequisiti sono soddisfatti. In caso di ambiguità, fermarsi.

## Workflow TASK

1. **Leggere il contesto:** soltanto i documenti tecnici richiesti o strettamente necessari.
2. **Verificare il perimetro:** file autorizzati, criteri, condizioni di arresto e istruzioni Git.
3. **Controllare Git:** eseguire `git status` e proteggere tutte le modifiche non correlate.
4. **Implementare:** applicare esclusivamente le modifiche richieste.
5. **Verificare e testare:** eseguire i test richiesti e controllare i criteri di completamento.
6. **Applicare le istruzioni Git:** seguire `GIT_WORKFLOW.md`; prima del push eseguire un nuovo fetch e verificare il fast-forward.
7. **Preparare la Engineering Review:** creare `docs/06_AI/REVIEWS/REVIEW-XXXX.md` usando il template ufficiale.
8. **Aggiornare lo stato:** aggiornare, quando previsto, `TASK_INDEX.md`, `AI_STATE.md` e la documentazione pertinente.
9. **Pubblicare:** il task è completato soltanto quando commit applicativo, review e stato sono pubblicati oppure il blocco è documentato.
10. **Mostrare il report e fermarsi:** indicare review, verdetto, SHA ed esito push.

La Engineering Review deve contenere, quando pertinenti: metadati, verdetto, rischio, sintesi, problemi con ID stabile, review per file ed end-to-end, regressioni, checklist, piano di consolidamento, decisioni richieste, autorizzazione o blocco del task successivo e conferma finale.

## Workflow OPS

1. **Leggere lo stato reale:** eseguire i comandi diagnostici definiti dall'operation.
2. **Verificare autorizzazioni e prerequisiti:** operazioni Git normalmente vietate sono consentite soltanto se il file OPS le autorizza esplicitamente.
3. **Proteggere il lavoro locale:** creare backup o stash solo quando l'operation lo richiede; non duplicare backup già esistenti.
4. **Eseguire gli step nell'ordine indicato:** non saltare, riordinare o ampliare le operazioni.
5. **Fermarsi sulle condizioni previste:** conflitto non deterministico, errore fuori perimetro o rischio di perdita dati.
6. **Verificare:** controllare stato Git, marcatori di conflitto, diff, commit, push e working tree.
7. **Produrre il report operativo:** creare il report in `docs/06_AI/OPERATIONS/REPORTS/` quando richiesto e aggiornare `OPS_INDEX.md` se autorizzato.

## Regole comuni

- Non usare `git add .` o `git add -A`.
- Non usare force push.
- Non alterare file fuori perimetro.
- Non decidere autonomamente requisiti funzionali o architetturali.
- La risposta mostrata al maintainer deve essere coerente con la review o il report pubblicato.
