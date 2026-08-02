# Workflow ufficiale di esecuzione dei task

Codex esegue solo attività esplicitamente richieste. Prima di qualsiasi operazione Git deve leggere e rispettare [GIT_WORKFLOW.md](GIT_WORKFLOW.md).

## Comandi sintetici del maintainer

### `Esegui TASK-XXXX`

Aprire `TASKS/TASK-XXXX.md` ed eseguirlo integralmente secondo questo workflow.

### `Esegui l'ultimo task`

1. Leggere `TASK_INDEX.md` dalla versione più recente disponibile.
2. Individuare il task con stato `Planned` avente il numero progressivo più alto.
3. Aprire il relativo file in `TASKS/`.
4. Eseguirlo integralmente secondo questo workflow.
5. Se non esistono task `Planned`, fermarsi e comunicarlo.

## 1. Leggere il contesto

Leggere documenti, istruzioni, vincoli e decisioni indicati nel task.

## 2. Leggere il task

Identificare obiettivo, file autorizzati, operazioni, criteri di completamento, condizioni di arresto e istruzioni Git.

## 3. Verificare il perimetro

Confermare che l'intervento riguardi solo file e sistemi autorizzati. Non introdurre miglioramenti non richiesti e non correggere file fuori dal perimetro.

## 4. Controllare lo stato Git

Eseguire `git status` prima di qualsiasi operazione Git. Le modifiche preesistenti e non correlate devono rimanere intatte e non essere incluse in staging, commit o push.

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
- problemi con ID stabile `BUG-XXXX`;
- milestone o task previsto per la risoluzione;
- riferimenti a regole, standard e documentazione violati;
- review per file;
- review end-to-end;
- regressioni potenziali;
- checklist;
- piano di consolidamento;
- decisioni richieste al maintainer;
- conferma finale delle operazioni eseguite.

La risposta mostrata al maintainer deve essere coerente con la review archiviata. La review non è una semplice trascrizione della conversazione, ma il documento tecnico ufficiale prodotto dal task.

## 11. Archiviare e pubblicare la review

La creazione della review è un'operazione amministrativa obbligatoria e separata dall'implementazione.

È consentita anche quando il task indica `Push: NO`, purché:

1. venga aggiunto allo staging esclusivamente il file `REVIEWS/REVIEW-XXXX.md`;
2. non vengano incluse modifiche applicative o documentali non autorizzate;
3. venga usato il commit `docs: archive engineering review for TASK-XXXX`;
4. venga eseguito il push su `origin/main` solo se il branch locale può avanzare senza pull, merge, rebase, reset o force push;
5. in caso di cronologie divergenti o push rifiutato, il file resti locale e l'errore venga riportato integralmente.

Prima del commit eseguire:

- `git diff --cached --check`;
- `git diff --cached --stat`.

Dopo il commit eseguire:

- `git show --stat --oneline HEAD`.

## 12. Mostrare il report

Mostrare al maintainer il riepilogo finale previsto dal task e indicare:

- percorso della review;
- verdetto;
- commit SHA della review, se creato;
- esito del push.

## 13. Fermarsi

Terminare il task e attendere istruzioni successive.
