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

## 10. Preparare il report integrale

Preparare la risposta finale completa prima di mostrarla al maintainer. Il report deve includere integralmente tutto ciò che Codex intende restituire nella risposta finale, senza riassunti o omissioni.

## 11. Archiviare automaticamente la risposta

Ogni risposta finale relativa a un task deve essere salvata nel repository in:

`docs/06_AI/RESPONSES/`

Usare un file Markdown distinto per ogni risposta con questo formato:

`TASK-XXXX_YYYY-MM-DD_HHMMSS.md`

Se la risposta non riguarda un task numerato, usare:

`GENERAL_YYYY-MM-DD_HHMMSS.md`

Il file deve contenere:

- identificativo e titolo del task, quando disponibili;
- data e ora;
- commit HEAD osservato all'inizio;
- testo integrale della risposta finale;
- eventuali errori o condizioni di arresto.

L'archiviazione del report è un'operazione amministrativa obbligatoria e separata dall'implementazione del task. È consentita anche quando il task indica `Push: NO`, purché:

1. venga aggiunto allo staging esclusivamente il file della risposta;
2. non vengano incluse modifiche applicative o documentali non autorizzate;
3. venga usato il commit `docs: archive Codex response for TASK-XXXX` oppure `docs: archive Codex response`;
4. venga eseguito il push su `origin/main` solo se il branch locale può avanzare in fast-forward senza pull, merge, rebase o reset;
5. in caso di cronologie divergenti o push rifiutato, il file resti locale e l'errore venga riportato integralmente.

Prima del commit del report eseguire:

- `git diff --cached --check`;
- `git diff --cached --stat`;

Dopo il commit eseguire:

- `git show --stat --oneline HEAD`.

## 12. Mostrare il report

Mostrare al maintainer esattamente lo stesso contenuto archiviato nel file Markdown, aggiungendo in fondo:

- percorso del file della risposta;
- commit SHA dell'archivio, se creato;
- esito del push dell'archivio.

## 13. Fermarsi

Terminare il task e attendere istruzioni successive.
