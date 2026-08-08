# Lean Autonomous Execution

## Scopo

Ridurre il consumo di contesto e token di Codex durante le tranche autonome senza ridurre le garanzie di sicurezza, tracciabilità o qualità finale.

Questo workflow si applica quando il maintainer usa `Controlla ed esegui tutti i nuovi task` e la coda contiene più task appartenenti alla stessa tranche.

## Principio

Una tranche autonoma è una singola sessione di lavoro con:

- un bootstrap completo iniziale;
- contesto incrementale tra i task;
- test mirati sui task intermedi;
- review intermedie compatte;
- un quality gate finale completo.

Codex non deve ripetere analisi già concluse nella stessa tranche salvo che un file rilevante sia cambiato o emerga un'incoerenza.

## Bootstrap completo — una sola volta

All'avvio della tranche:

1. `git fetch origin main`;
2. applicare l'eventuale fast-forward sicuro autorizzato dalla coda;
3. leggere una volta:
   - `AGENTS.md`;
   - `AI_CONSTITUTION.md`;
   - `AI_STATE.md`;
   - `CODEX_WORKFLOW.md`;
   - `GIT_WORKFLOW.md`;
   - `AUTONOMOUS_TASK_QUEUE.md`;
   - questo file;
   - `TASK_INDEX.md`;
   - tutti i task della tranche;
   - le sole decisioni e fonti tecniche esplicitamente richieste dai task.

Non leggere intere cartelle di documentazione per ricostruire informazioni già fornite nei task.

## Passaggio tra task

Dopo la pubblicazione di un task intermedio:

1. eseguire fetch e, se necessario e sicuro, fast-forward;
2. rileggere soltanto:
   - `AI_STATE.md`;
   - `TASK_INDEX.md`;
   - la review appena prodotta;
   - il task successivo;
   - eventuali file AI realmente modificati dopo il bootstrap;
3. non rileggere Costituzione, AGENTS, GIT_WORKFLOW o documenti tecnici invariati;
4. rileggere una fonte tecnica soltanto se il task successivo la richiede o se è cambiata durante la tranche.

Se un hash o un diff mostra che un documento operativo è cambiato, rileggere solo quel documento.

## Test intermedi

Per i task che non sono quality gate:

- eseguire i test direttamente pertinenti ai file o moduli modificati;
- eseguire lint, type-check, build o test di integrazione soltanto quando il task li richiede o sono necessari a dimostrare il criterio di completamento;
- non ricreare il database da zero, non eseguire l'intera suite backend e non fare rebuild Docker senza cache a ogni task, salvo necessità tecnica specifica;
- eseguire un controllo di regressione minimo sulle aree direttamente dipendenti.

Il task finale di quality gate esegue invece tutte le verifiche complete previste per la tranche.

## Review intermedie compatte

Le review dei task intermedi devono essere concise e contenere soltanto:

- metadati e commit;
- verdetto;
- sintesi delle modifiche;
- test mirati realmente eseguiti;
- problemi o rischi residui;
- conferma del perimetro;
- autorizzazione o blocco del task successivo.

Non ripetere una review file-per-file dettagliata se non esistono problemi specifici. Non ricopiare requisiti già presenti nel task.

## Review del quality gate

La review del quality gate resta completa e deve includere:

- verifica end-to-end;
- regressioni;
- migrazioni e database quando pertinenti;
- build e runtime;
- suite completa prevista;
- problemi classificati;
- stato finale della tranche.

## Uso del contesto

Codex deve preferire:

- `git diff --name-only` e `git diff --stat` prima di aprire file completi;
- ricerca mirata (`grep`, `rg`) prima di leggere documenti lunghi;
- intervalli di righe pertinenti anziché file completi quando possibile;
- output sintetici dei test, espandendo i log solo in caso di errore;
- riuso del contesto già letto nella sessione corrente.

Non stampare nel terminale interi file lunghi già letti solo per confermarne il contenuto.

## Git

Le regole Git restano invariate. L'ottimizzazione del contesto non autorizza operazioni aggiuntive e non riduce i controlli su working tree, staging, commit e fast-forward.

## Arresto

Le condizioni di arresto di `AUTONOMOUS_TASK_QUEUE.md` restano tutte valide.

Se per risparmiare contesto sarebbe necessario saltare una verifica indispensabile alla sicurezza o al criterio di completamento, eseguire la verifica: la qualità prevale sull'ottimizzazione.

## Obiettivo operativo

Codex deve usare la maggior parte del proprio budget per implementazione, debug e test del codice; coordinamento, architettura e definizione dei requisiti devono provenire dai task e dalle decisioni già preparati dal Tech Lead.