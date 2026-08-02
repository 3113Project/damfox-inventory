# Autonomous Task Queue

## Scopo

Definire la modalità con cui Codex esegue in sequenza tutti i task applicativi disponibili senza richiedere un nuovo comando del maintainer dopo ogni task.

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

## Algoritmo della coda

1. Eseguire il bootstrap obbligatorio definito in `AGENTS.md`.
2. Leggere da `origin/main` `AI_STATE.md`, `TASK_INDEX.md` e tutti i task con stato `Planned`.
3. Ordinare i task eseguibili per numero progressivo crescente.
4. Selezionare il primo task i cui prerequisiti risultano soddisfatti.
5. Eseguire integralmente il task secondo `CODEX_WORKFLOW.md`.
6. Eseguire test, creare commit, Engineering Review, aggiornare stato e pubblicare quanto previsto.
7. Dopo ogni push riuscito, eseguire nuovamente `git fetch origin main`.
8. Rileggere da `origin/main` `AI_STATE.md`, `TASK_INDEX.md`, le review appena pubblicate e gli eventuali nuovi task o decisioni.
9. Se esiste un altro task `Planned` eseguibile, proseguire automaticamente senza attendere il maintainer.
10. Terminare soltanto quando si verifica una condizione di arresto.

## Condizioni di arresto obbligatorie

Codex deve fermare la coda e riportare lo stato completo quando:

- non esistono più task con stato `Planned`;
- tutti i task rimanenti sono `Blocked`;
- un task richiede una decisione funzionale, architetturale o commerciale non registrata;
- una Engineering Review produce verdetto `NON APPROVATO` o non autorizza il task successivo;
- un test richiesto fallisce e il task non autorizza la correzione necessaria;
- il push non è fast-forward;
- è necessaria una operation Git o infrastrutturale non già autorizzata;
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
- Le operation non vengono eseguite automaticamente, salvo che siano già `Planned`, necessarie alla prosecuzione e prive di decisioni discrezionali; in caso contrario la coda si arresta.

## Report finale della coda

Al termine Codex deve mostrare un riepilogo unico contenente:

- task eseguiti nell'ordine;
- verdetto di ogni review;
- commit applicativi e commit delle review;
- test eseguiti;
- task rimasti `Blocked` o `Planned`;
- motivo dell'arresto;
- stato finale di branch e working tree.
