# Workflow ufficiale di esecuzione dei task

Codex esegue solo attività esplicitamente richieste. Prima di qualsiasi operazione Git deve leggere e rispettare [GIT_WORKFLOW.md](GIT_WORKFLOW.md).

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

## 10. Produrre il report

Restituire il risultato nel formato richiesto, con modifiche, verifiche, commit e anomalie pertinenti.

## 11. Fermarsi

Terminare il task e attendere istruzioni successive.
