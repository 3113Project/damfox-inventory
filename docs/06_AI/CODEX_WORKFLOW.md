# Workflow ufficiale di esecuzione per Codex

Codex esegue solo attività esplicitamente richieste e rispetta sempre:

1. `docs/06_AI/AI_CONSTITUTION.md`;
2. `AGENTS.md`;
3. `docs/06_AI/GIT_WORKFLOW.md`;
4. il TASK o OPS richiesto.

Per una coda autonoma applica inoltre `WORKFLOWS/AUTONOMOUS_TASK_QUEUE.md` e `WORKFLOWS/LEAN_AUTONOMOUS_EXECUTION.md`.

## Bootstrap

Per una nuova attività eseguire `git fetch origin main` e leggere da `origin/main` i documenti operativi, indice, attività, decisioni e fonti richieste.

In una tranche autonoma il bootstrap completo viene eseguito una sola volta. Tra task consecutivi rileggere soltanto stato, indice, review precedente, task successivo ed eventuali documenti realmente cambiati. Non ristampare o rileggere file lunghi invariati solo per conferma.

Il bootstrap non autorizza automaticamente pull, merge non previsti, rebase, reset, stash o force push. Se il fetch fallisce, fermarsi.

## Comandi sintetici

### `Esegui TASK-XXXX`

Leggere `TASK_INDEX.md`, `TASKS/TASK-XXXX.md` e i prerequisiti indicati. Eseguire il task e produrre `REVIEWS/REVIEW-XXXX.md` soltanto se lo stato esatto nell'indice è `Planned`.

I task `Completed`, `Superseded`, retrospettivi o marcati come archivio non eseguibile devono essere rifiutati. `TASK-0001`–`TASK-0007` sono storici.

### `Esegui l'ultimo task`

Leggere `AI_STATE.md` e verificare che `current_task` risulti `Planned` anche in `TASK_INDEX.md`.

### `Esegui OPS-XXXX`

Leggere `OPERATIONS/OPS_INDEX.md` e `OPERATIONS/OPS-XXXX.md`. Eseguire soltanto la procedura operativa autorizzata e produrre il report richiesto.

### `Esegui l'ultima operation`

Individuare in `OPS_INDEX.md` la prima operation `Planned` i cui prerequisiti sono soddisfatti. In caso di ambiguità, fermarsi.

## Workflow TASK

1. **Contesto mirato:** leggere soltanto fonti necessarie al task; usare ricerca e diff prima di aprire file interi.
2. **Perimetro:** verificare file autorizzati, criteri, arresti e istruzioni Git.
3. **Git:** controllare `git status` e proteggere modifiche non correlate.
4. **Implementazione:** applicare esclusivamente le modifiche richieste.
5. **Verifica proporzionata:**
   - task intermedio di tranche: test mirati e regressioni direttamente dipendenti;
   - task standalone: verifiche richieste dal task;
   - quality gate: suite completa, build/runtime, migrazioni ed end-to-end previsti.
6. **Git pre-push:** seguire `GIT_WORKFLOW.md`, fetch e controllo fast-forward.
7. **Engineering Review:**
   - task intermedio: review compatta;
   - quality gate o task con problemi: review completa.
8. **Stato:** aggiornare `TASK_INDEX.md`, `AI_STATE.md` e documentazione solo quando previsto.
9. **Pubblicazione:** completamento solo dopo commit, review e stato pubblicati oppure blocco documentato.
10. **Output:** rispondere in modo sintetico; nella coda autonoma non produrre lunghi riepiloghi intermedi se il task successivo può partire.

## Review compatta per task intermedi

Deve contenere almeno:

- task, commit, verdetto e rischio;
- sintesi delle modifiche;
- test mirati realmente eseguiti;
- problemi/rischi residui;
- conferma che il perimetro è rispettato;
- autorizzazione o blocco del task successivo.

Non è obbligatorio ripetere review file-per-file, checklist generiche o piano di consolidamento quando non aggiungono informazione.

## Review completa

È obbligatoria per quality gate, regressioni significative, verdetto con riserve o non approvato. Include quando pertinenti: indicatori, problemi con ID stabile, review per file ed end-to-end, regressioni, checklist, piano di consolidamento, decisioni richieste e stato finale.

## Workflow OPS

1. leggere lo stato reale;
2. verificare autorizzazioni e prerequisiti;
3. proteggere il lavoro locale quando richiesto;
4. eseguire gli step nell'ordine indicato;
5. fermarsi sulle condizioni previste;
6. verificare stato Git, diff, commit e push;
7. produrre il report operativo richiesto.

## Efficienza del contesto

- Preferire `rg`, `grep`, `git diff --name-only` e `git diff --stat` prima di leggere file completi.
- Leggere intervalli pertinenti quando possibile.
- Usare output test sintetici e aprire log estesi solo in caso di fallimento.
- Non rieseguire suite complete già coperte da un quality gate successivo, salvo requisito esplicito o rischio concreto.
- Non rileggere documenti invariati già presenti nel contesto della sessione.
- La qualità e la sicurezza prevalgono sempre sul risparmio di token.

## Regole comuni

- Non usare `git add .` o `git add -A`.
- Non usare force push.
- Non alterare file fuori perimetro.
- Non decidere autonomamente requisiti funzionali o architetturali.
- La risposta mostrata al maintainer deve essere coerente con la review o il report pubblicato.