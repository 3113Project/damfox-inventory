# Workflow ufficiale di esecuzione dei task

Codex esegue solo attività esplicitamente richieste. Le istruzioni di bootstrap nella root del repository, contenute in [`AGENTS.md`](../../AGENTS.md), sono obbligatorie.

## Regola preliminare obbligatoria — bootstrap e contesto remoto

Prima di interpretare o eseguire qualsiasi comando del maintainer, Codex deve:

```bash
git fetch origin main
```

Se il fetch fallisce, deve fermarsi e riportare l'errore.

Dopo il fetch deve leggere da `origin/main`, mediante `git show`:

```bash
git show origin/main:AGENTS.md
git show origin/main:docs/06_AI/AI_STATE.md
git show origin/main:docs/06_AI/CODEX_WORKFLOW.md
git show origin/main:docs/06_AI/GIT_WORKFLOW.md
```

Per un task numerato deve leggere anche:

```bash
git show origin/main:docs/06_AI/TASKS/TASK-XXXX.md
```

Deve inoltre leggere da `origin/main` le decisioni, review e gli altri documenti sotto `docs/06_AI/` indicati dal task.

La versione ufficiale della memoria operativa AI è sempre quella presente in `origin/main`. Il fetch e la lettura tramite `git show` sono obbligatori anche quando il branch locale contiene modifiche non committate o risulta indietro rispetto al remoto.

Per aggiornare il contesto non deve usare automaticamente:

- `git pull`;
- merge;
- rebase;
- reset;
- stash;
- checkout o restore massivi;
- force push.

## Comandi sintetici del maintainer

### `Esegui TASK-XXXX`

1. Applicare il bootstrap di `AGENTS.md`.
2. Leggere `AI_STATE.md` da `origin/main`.
3. Leggere `TASKS/TASK-XXXX.md` da `origin/main`.
4. Verificare stato e prerequisiti in `TASK_INDEX.md` e `AI_STATE.md`.
5. Eseguire integralmente il task secondo questo workflow.

### `Esegui l'ultimo task`

1. Applicare il bootstrap di `AGENTS.md`.
2. Leggere `AI_STATE.md` da `origin/main`.
3. Usare il valore `current_task` come candidato.
4. Verificare che il candidato risulti `Planned` anche in `TASK_INDEX.md`.
5. Leggere il relativo file in `TASKS/` da `origin/main`.
6. Eseguirlo integralmente.
7. In caso di incoerenza tra `AI_STATE.md` e `TASK_INDEX.md`, fermarsi e segnalarla.

## 1. Leggere il contesto

Leggere documenti, istruzioni, vincoli e decisioni indicati nel task.

I documenti sotto `docs/06_AI/` devono essere letti dalla versione `origin/main` dopo il fetch obbligatorio.

La documentazione nelle cartelle `00_Project`–`05_Project_Management` deve essere letta soltanto quando richiesta dal task o strettamente necessaria per comprenderne il perimetro.

## 2. Leggere il task

Identificare obiettivo, file autorizzati, operazioni, criteri di completamento, condizioni di arresto e istruzioni Git.

## 3. Verificare il perimetro

Confermare che l'intervento riguardi solo file e sistemi autorizzati. Non introdurre miglioramenti non richiesti e non correggere file fuori dal perimetro.

## 4. Controllare lo stato Git

Eseguire `git status` prima di qualsiasi modifica o ulteriore operazione Git. Le modifiche preesistenti e non correlate devono rimanere intatte e non essere incluse in staging, commit o push.

## 5. Analizzare i file coinvolti

Esaminare solo i file necessari per comprendere lo stato iniziale e l'impatto delle modifiche.

## 6. Eseguire solo le modifiche richieste

Applicare esclusivamente le modifiche autorizzate. Se una richiesta è ambigua o richiede autorizzazioni mancanti, fermarsi e chiedere chiarimenti.

## 7. Fare autoverifica

Controllare i criteri di completamento e le verifiche esplicitamente richieste.

## 8. Eseguire test

Eseguire i test e i comandi indicati dal task; non sostituirli con attività non autorizzate.

## 9. Applicare le istruzioni Git del task

Seguire la sezione Git del task e [GIT_WORKFLOW.md](GIT_WORKFLOW.md). Non creare commit o push relativi all'implementazione se la sezione Git non li autorizza esplicitamente.

Prima di qualsiasi push, eseguire un nuovo:

```bash
git fetch origin main
```

Verificare che la pubblicazione sia fast-forward. Il fetch non autorizza pull, merge o rebase.

## 10. Preparare la Engineering Review

Ogni task deve produrre una review tecnica completa in `REVIEWS/`.

Il file deve chiamarsi:

`REVIEW-XXXX.md`

Il numero deve corrispondere al task. Usare [REVIEWS/REVIEW_TEMPLATE.md](REVIEWS/REVIEW_TEMPLATE.md) come struttura di riferimento.

La review deve contenere, quando pertinenti:

- metadati del task;
- verdetto: `APPROVATO`, `APPROVATO CON RISERVE`, `NON APPROVATO` oppure `NON APPLICABILE`;
- livello di rischio;
- sintesi esecutiva;
- conteggio dei problemi per priorità;
- problemi con ID stabile;
- milestone o task previsto per la risoluzione;
- riferimenti a regole, standard e documentazione violati;
- review per file;
- review end-to-end;
- regressioni potenziali;
- checklist;
- piano di consolidamento;
- decisioni richieste al maintainer;
- conferma finale delle operazioni eseguite.

La risposta mostrata al maintainer deve essere coerente con la review archiviata.

## 11. Aggiornare lo stato operativo

Quando un task cambia stato, Codex deve aggiornare, se autorizzato dal task:

- `TASK_INDEX.md`;
- `AI_STATE.md`.

`AI_STATE.md` deve riflettere almeno:

- task corrente;
- ultimo task completato;
- ultima review;
- prossimi task;
- task bloccati;
- decisioni attive pertinenti.

Non aggiornare lo stato in modo speculativo: deve corrispondere a risultati effettivamente verificati.

## 12. Archiviare e pubblicare la review

La creazione della review è un'operazione amministrativa obbligatoria e separata dall'implementazione.

È consentita anche quando il task indica `Push: NO`, purché:

1. venga aggiunto allo staging esclusivamente il file `REVIEWS/REVIEW-XXXX.md`;
2. non vengano incluse modifiche non autorizzate;
3. venga usato il commit `docs: archive engineering review for TASK-XXXX`;
4. il push sia fast-forward;
5. in caso di cronologie divergenti o push rifiutato, il file resti locale e l'errore venga riportato integralmente.

Prima del commit eseguire:

- `git diff --cached --check`;
- `git diff --cached --stat`.

Dopo il commit eseguire:

- `git show --stat --oneline HEAD`.

## 13. Mostrare il report

Mostrare al maintainer il riepilogo finale previsto dal task e indicare:

- percorso della review;
- verdetto;
- commit SHA della review, se creato;
- esito del push.

## 14. Fermarsi

Terminare il task e attendere istruzioni successive.
