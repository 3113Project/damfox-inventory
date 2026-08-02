# Workflow ufficiale di esecuzione per Codex

Codex rispetta sempre:

1. `docs/06_AI/AI_CONSTITUTION.md`;
2. `AGENTS.md`;
3. `docs/06_AI/WORKFLOWS/ENVIRONMENT_BOOTSTRAP.md`;
4. `docs/06_AI/GIT_WORKFLOW.md`;
5. il TASK o OPS richiesto.

## Bootstrap obbligatorio

### Ambiente con remote `origin` accessibile

Eseguire:

```bash
git fetch origin main
```

Leggere da `origin/main` tramite `git show` i documenti operativi e l'attività richiesta. Se il fetch fallisce, fermarsi.

### Ambiente senza remote `origin`

Leggere direttamente dal workspace corrente gli stessi documenti. Questa modalità è prevista per Codex Web/Cloud e non richiede la configurazione manuale di un remote.

In entrambe le modalità verificare la coerenza tra `AI_STATE.md`, indice e attività richiesta.

## Comandi sintetici

### `Esegui TASK-XXXX`

Leggere indice, task, prerequisiti e knowledge dalla fonte disponibile; eseguire il task e produrre `REVIEWS/REVIEW-XXXX.md`.

### `Esegui l'ultimo task`

Verificare che `current_task` sia `Planned` anche in `TASK_INDEX.md`.

### `Esegui OPS-XXXX`

Leggere indice Operations e operation richiesta; eseguire soltanto la procedura autorizzata.

### `Esegui l'ultima operation`

Individuare la prima operation `Planned` con prerequisiti soddisfatti.

### `Controlla ed esegui tutti i nuovi task`

Eseguire la tranche autonoma prevista, in ordine, fino a esaurimento o condizione di arresto. In cloud ogni task deve rispettare la strategia branch/PR prevista dalla coda o dal task.

## Workflow TASK

1. **Rilevare ambiente e fonte:** applicare `ENVIRONMENT_BOOTSTRAP.md`.
2. **Leggere il contesto:** solo documenti richiesti o necessari.
3. **Verificare il perimetro:** file autorizzati, criteri, arresti e pubblicazione.
4. **Controllare il workspace:** proteggere modifiche non correlate.
5. **Implementare:** applicare solo le modifiche richieste.
6. **Verificare e testare:** eseguire i test supportati; documentare quelli impossibili nell'ambiente.
7. **Preparare la Engineering Review.**
8. **Aggiornare stato e documentazione** quando previsto.
9. **Pubblicare:**
   - locale: commit e push fast-forward autorizzato;
   - cloud: branch dedicata e pull request verso `main` quando richiesto;
   - ambiente limitato: patch/commit e blocco documentato.
10. **Mostrare il report e fermarsi**, oppure proseguire con la coda autonoma.

La review deve contenere metadati, verdetto, rischio, sintesi, problemi, review per file ed end-to-end, regressioni, checklist, decisioni richieste e conferma finale.

## Workflow OPS

1. leggere lo stato reale;
2. verificare autorizzazioni e prerequisiti;
3. proteggere il lavoro locale quando applicabile;
4. eseguire gli step nell'ordine indicato;
5. fermarsi sulle condizioni previste;
6. verificare stato Git, diff, commit e pubblicazione;
7. produrre il report operativo richiesto.

## Regole cloud

- Non assumere che la shell disponga di `origin`.
- Non tentare di aggiungere credenziali o remote del server DAMFOX.
- Usare la branch/snapshot predisposta da Codex Cloud.
- Aprire pull request quando il task lo richiede.
- Non dichiarare superati test Docker o PostgreSQL non eseguiti; indicare chiaramente limiti e verifiche residue locali.

## Regole comuni

- Non usare `git add .` o `git add -A`.
- Non usare force push.
- Non alterare file fuori perimetro.
- Non decidere autonomamente requisiti funzionali o architetturali.
- La risposta al maintainer deve coincidere con la review o il report pubblicato.
