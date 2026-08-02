# Workflow ufficiale di esecuzione dei task

Codex esegue solo attività esplicitamente richieste. Prima di qualsiasi operazione Git deve leggere e rispettare [GIT_WORKFLOW.md](GIT_WORKFLOW.md).

## Comando rapido: eseguire l'ultimo task

Quando il maintainer scrive `Esegui l'ultimo task`, Codex deve:

1. eseguire `git fetch origin main` senza pull, merge, rebase o reset;
2. leggere `docs/06_AI/TASK_INDEX.md`, preferendo `origin/main` se più recente;
3. individuare il task con identificativo numericamente più alto e stato `Planned`;
4. aprire il corrispondente file `docs/06_AI/TASKS/TASK-XXXX.md`, preferendo `origin/main` se più recente;
5. eseguirlo integralmente secondo questo workflow e [GIT_WORKFLOW.md](GIT_WORKFLOW.md);
6. se non esiste alcun task `Planned`, fermarsi e comunicarlo senza eseguire altro.

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

Seguire la sezione Git del task e [GIT_WORKFLOW.md](GIT_WORKFLOW.md). Non creare commit o push se la sezione Git non li autorizza esplicitamente.

## 10. Produrre e archiviare il report

Preparare il report finale nel formato richiesto dal task. Prima di mostrarlo nella chat, salvarne una copia integrale e identica in UTF-8 nella directory:

`/home/casa/codex-responses/`

Il nome del file deve essere:

`YYYY-MM-DD_HH-MM-SS_TASK-XXXX.md`

Se non è associato a un task, usare:

`YYYY-MM-DD_HH-MM-SS_RESPONSE.md`

Creare la directory se non esiste. Il file deve contenere l'intera risposta finale, senza omissioni o riassunti. Il salvataggio del report non autorizza automaticamente commit o push.

Dopo il salvataggio, restituire nella chat lo stesso contenuto e aggiungere in fondo il percorso del file archiviato.

## 11. Fermarsi

Terminare il task e attendere istruzioni successive.
