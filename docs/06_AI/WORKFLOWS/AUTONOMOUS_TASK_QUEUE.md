# Autonomous Task Queue

## Scopo

Definire la modalità con cui Codex esegue in sequenza tutti i task applicativi disponibili senza richiedere un nuovo comando del maintainer dopo ogni task.

Per le tranche con più task applicare anche `WORKFLOWS/LEAN_AUTONOMOUS_EXECUTION.md`: un solo bootstrap completo iniziale, contesto incrementale, verifiche mirate intermedie e quality gate completo finale.

## Comando di avvio

Il maintainer avvia la coda con:

```text
Controlla ed esegui tutti i nuovi task.
```

Sono accettate come equivalenti:

```text
Esegui tutti i task pianificati.
```

```text
Avvia la coda dei task.
```

## Autorizzazione al riallineamento iniziale sicuro

Il comando di avvio della coda costituisce autorizzazione esplicita a riallineare `main` con `origin/main` mediante **solo fast-forward**, prima di eseguire il primo task.

Dopo `git fetch origin main`, Codex deve verificare:

- branch corrente esatto: `main`;
- working tree e indice puliti;
- nessun rebase o merge in corso;
- nessun commit locale assente da `origin/main`;
- relazione tra `HEAD` e `origin/main` compatibile con un avanzamento fast-forward.

Se tutte le condizioni sono soddisfatte e il branch locale è indietro, è autorizzato esclusivamente:

```bash
git merge --ff-only origin/main
```

Dopo il comando deve verificare che `HEAD` coincida con `origin/main`.

Questa autorizzazione non consente merge commit, `git pull` generico, rebase, reset, stash, force push o risoluzione automatica di divergenze e conflitti.

Se il working tree non è pulito, il branch non è `main`, esistono commit locali, compare divergenza oppure `git merge --ff-only` fallisce, Codex deve fermarsi senza modificare nulla e riportare lo stato Git completo.

La stessa autorizzazione vale dopo un push della coda quando `origin/main` contiene soltanto nuovi commit fast-forward pubblicati da ChatGPT o da un altro agente e il workspace locale è pulito e privo di commit esclusivamente locali.

## Algoritmo della coda

1. Eseguire il bootstrap obbligatorio definito in `AGENTS.md`.
2. Applicare, se necessario, il riallineamento iniziale sicuro autorizzato in questo documento.
3. Leggere una sola volta all'avvio `AI_STATE.md`, `TASK_INDEX.md`, i task della tranche e il contesto richiesto, secondo `LEAN_AUTONOMOUS_EXECUTION.md`.
4. Ordinare i task eseguibili per numero progressivo crescente.
5. Selezionare il primo task i cui prerequisiti risultano soddisfatti.
6. Eseguire integralmente il task secondo `CODEX_WORKFLOW.md`.
7. Per task intermedi eseguire verifiche mirate e produrre una Engineering Review compatta; riservare suite completa, rebuild, database pulito ed end-to-end al quality gate finale salvo requisito esplicito del task.
8. Dopo ogni push riuscito, eseguire `git fetch origin main` e, quando necessario e sicuro, `git merge --ff-only origin/main`.
9. Tra task della stessa tranche rileggere soltanto `AI_STATE.md`, `TASK_INDEX.md`, la review appena prodotta, il task successivo e gli eventuali documenti operativi effettivamente cambiati.
10. Non rileggere file invariati già acquisiti nel bootstrap completo e non ristampare interi documenti lunghi per conferma.
11. Se esiste un altro task `Planned` eseguibile, proseguire automaticamente senza attendere il maintainer.
12. Terminare soltanto quando si verifica una condizione di arresto.

## Condizioni di arresto obbligatorie

Codex deve fermare la coda e riportare lo stato completo quando:

- non esistono più task con stato `Planned`;
- tutti i task rimanenti sono `Blocked`;
- un task richiede una decisione funzionale, architetturale o commerciale non registrata;
- una Engineering Review produce verdetto `NON APPROVATO` o non autorizza il task successivo;
- un test richiesto fallisce e il task non autorizza la correzione necessaria;
- il push non è fast-forward;
- è necessaria una operation Git o infrastrutturale diversa dal fast-forward sicuro già autorizzato;
- esiste un conflitto non deterministico;
- il fetch fallisce;
- sussiste un rischio di perdita o sovrascrittura di dati o lavoro locale;
- il task richiede un'azione distruttiva o una release che necessita approvazione esplicita del maintainer.

## Regole di sicurezza

- La modalità autonoma non amplia il perimetro dei singoli task.
- Solo i task con stato esatto `Planned` possono essere selezionati ed eseguiti.
- I task `Completed`, `Superseded`, retrospettivi o marcati come archivio non eseguibile sono sempre ignorati; la presenza fisica del relativo file non costituisce autorizzazione.
- `TASK-0001`–`TASK-0007` sono documenti storici non eseguibili e non possono entrare nella coda senza una nuova autorizzazione esplicita del maintainer registrata in un nuovo task o operation.
- Codex non crea nuovi task applicativi di propria iniziativa.
- Codex non trasforma automaticamente task `Blocked` in `Planned` salvo che una review o una regola già approvata lo autorizzi esplicitamente.
- Codex non inventa requisiti mancanti.
- Ogni task conserva commit, review e verifiche separati e identificabili.
- Prima di iniziare il task successivo, il task precedente deve risultare pubblicato e lo stato remoto deve essere coerente.
- L'ottimizzazione dei token non autorizza a saltare controlli necessari alla sicurezza, al criterio di completamento o al quality gate finale.
- Le operation non vengono eseguite automaticamente, salvo che siano già `Planned`, necessarie alla prosecuzione e prive di decisioni discrezionali; in caso contrario la coda si arresta.

## Report finale della coda

Al termine Codex deve mostrare un riepilogo unico e sintetico contenente:

- task eseguiti nell'ordine;
- verdetto di ogni review;
- commit applicativi e commit delle review;
- test mirati intermedi e verifiche complete del quality gate;
- task rimasti `Blocked` o `Planned`;
- motivo dell'arresto;
- stato finale di branch e working tree.