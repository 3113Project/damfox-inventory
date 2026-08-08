# REVIEW-XXXX

## Modalità

Usare una delle due modalità:

- `COMPACT` per task intermedi di una tranche autonoma;
- `FULL` per quality gate, task standalone ad alto rischio, regressioni significative o verdetti con riserve/non approvati.

## Template COMPACT

### Metadati

- **Task:** TASK-XXXX
- **Titolo:**
- **Commit analizzato:**
- **Verdetto:** APPROVATO | APPROVATO CON RISERVE | NON APPROVATO | NON APPLICABILE
- **Rischio:** Basso | Medio | Alto | Critico

### Sintesi

### Verifiche mirate eseguite

### Problemi o rischi residui

### Perimetro

Confermare che non siano state introdotte modifiche fuori task.

### Task successivo

- **Autorizzato:** SÌ | NO
- **Task:** TASK-XXXX | nessuno
- **Motivo:**

## Template FULL

### Metadati

- **Task:** TASK-XXXX
- **Titolo:**
- **Data:**
- **Commit analizzato:**
- **Verdetto:** APPROVATO | APPROVATO CON RISERVE | NON APPROVATO | NON APPLICABILE
- **Rischio:** Basso | Medio | Alto | Critico

### Sintesi esecutiva

### Indicatori

- Blocking issues:
- Alta priorità:
- Media priorità:
- Bassa priorità:
- Pronto per sviluppo o merge: SÌ | NO

### Problemi identificati

Ogni problema deve avere un ID stabile.

### Review per file

### Review end-to-end

### Regressioni potenziali

### Checklist pertinente

Non includere voci non pertinenti solo per riempire il template.

### Piano di consolidamento

### Decisioni richieste al maintainer

### Task successivo o chiusura tranche

### Conferma finale

## Regola

La review deve registrare ciò che è stato realmente verificato. Non duplicare integralmente requisiti già presenti nel task e non espandere sezioni prive di informazione utile.