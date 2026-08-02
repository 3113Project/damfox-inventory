# REVIEW-0010 — Audit tecnico delle modifiche backend locali

## Metadati

- **Task:** TASK-0010
- **Verdetto:** NON APPROVATO
- **Rischio:** Alto
- **Pronto per pubblicazione:** NO

## Indicatori

- Modifiche locali rilevate: 12
- File modificati: 3
- File non tracciati: 9
- Blocking issues: 9
- Test automatici presenti: 0

## 1. Sintesi esecutiva

Le modifiche locali non sono pronte per la pubblicazione.

Il modulo Categories è incompleto e non avviabile: model e schema importano moduli inesistenti, service e router sono vuoti, il router non è registrato, il modello non entra nella metadata e manca la migrazione Alembic. Non sono implementate le validazioni gerarchiche richieste.

Il modulo VAT è integrato end-to-end, ma presenta rischi di integrità ed error handling: assenza di rollback, gestione dei duplicati non controllata e aggiornamenti che consentono valori null incompatibili con il database.

Sono state rilevate 12 modifiche locali:

- 3 file modificati;
- 9 file non tracciati;
- nessuna divergenza tra main e origin/main;
- nessun merge o rebase in corso.

## 2. Problemi bloccanti

### BUG-001 — Import Category model inesistente

`backend/app/models/category.py` importa `app.models.base`, che non esiste. Il modulo corretto presente nel repository è `app.models.base_model`.

### BUG-002 — Import Category schema inesistente

`backend/app/schemas/category.py` importa `app.schemas.base`, che non esiste.

### BUG-003 — Service Categories assente

`backend/app/services/category_service.py` è vuoto.

### BUG-004 — Router Categories assente

`backend/app/api/v1/categories.py` è vuoto.

### BUG-005 — Router Categories non registrato

Il router Categories non è esportato da `backend/app/api/v1/__init__.py` né registrato in `backend/app/main.py`.

### BUG-006 — Category non registrato nella metadata

Category non è esportato da `backend/app/models/__init__.py`; di conseguenza Alembic non lo carica tramite `import app.models`.

### BUG-007 — Migrazione Categories assente

Non esiste una migrazione Alembic per `categories`.

### BUG-008 — Naming convention SQLAlchemy non valida

`backend/app/database/base.py` usa `{...}` come `naming_convention`: è un set contenente `Ellipsis`, non una mapping valida per SQLAlchemy. La costruzione della metadata e dei vincoli non è affidabile.

### BUG-009 — Creazione implicita dello schema

L’avvio esegue `Base.metadata.create_all()` durante l’importazione di `main.py`, in conflitto con Alembic come fonte di verità e con rischio di modifiche implicite allo schema.

Le verifiche runtime degli import non sono state completabili nell’ambiente host perché FastAPI, SQLAlchemy e Pydantic non sono installati. Docker Compose è sintatticamente valido.

## 3. Problemi per priorità

### Alta priorità

- Il vincolo `UNIQUE(parent_id, name)` non impedisce categorie radice duplicate in PostgreSQL, perché più valori `NULL` sono ammessi.
- Non esistono controlli contro auto-parenting.
- Non esistono controlli contro cicli diretti o indiretti.
- Non è definito il comportamento di eliminazione di una categoria con figli.
- La relazione gerarchica non specifica una politica `ondelete` o una gestione applicativa esplicita.
- Non viene verificata l’esistenza della categoria padre.
- Il service VAT non esegue rollback in caso di errore durante `commit()` o `refresh()`.
- Duplicati VAT e altre violazioni dei vincoli producono verosimilmente errori database non tradotti in risposte HTTP coerenti.
- `VATRateUpdate` permette `None` per colonne database non nullable. `exclude_unset=True` gestisce correttamente i campi omessi, ma non impedisce l’invio esplicito di `null`.
- Modelli e migrazioni VAT non sono coerenti: `VATRate` eredita `created_at` e `updated_at`, assenti nella migrazione.
- La revisione utenti è vuota, mentre `main.py` importa User e demanda la creazione effettiva a `create_all()`.

### Media priorità

- Gli schemi Category non impongono il limite di 100 caratteri previsto dal modello.
- Gli schemi VAT non impongono limiti coerenti con `String(50)` e `Numeric(5,2)`, né validano l’intervallo dell’aliquota.
- `CategoryUpdate` distingue correttamente campo omesso e campo impostato a `null` solo se il service userà `exclude_unset=True`; il service attuale è vuoto.
- Il router VAT usa `PUT` per aggiornamenti parziali; il comportamento è semanticamente più vicino a `PATCH`.
- Le funzioni pubbliche di router e service VAT non hanno docstring.
- Mancano annotazioni precise dei tipi restituiti nei service.
- Esistono due implementazioni di `get_db`, in `database/session.py` e `dependencies/db.py`.
- `main.py` importa direttamente i modelli per popolare la metadata, mentre Alembic usa `app.models`: la strategia di registrazione non è uniforme.
- L’URL Alembic è configurato separatamente da `DATABASE_URL`, creando due fonti di configurazione.
- `docker-compose.yml` contiene spazi finali nella riga aggiunta.
- Non esistono test automatici.

### Bassa priorità

- Diversi file non rispettano l’header descrittivo richiesto dagli standard.
- Mancano newline finali nei file locali aggiunti o modificati.
- L’ordine degli import non è uniforme.
- `backend/app/models/vat_rate.py` contiene righe vuote superflue.
- I commenti separatori nel model Category aggiungono rumore senza spiegare motivazioni.
- I placeholder `auth.py`, `pagination.py`, `exceptions.py`, `logging.py` e `security.py` sono vuoti; non bloccano Categories, ma rappresentano debito tecnico dichiarato.

## 4. Review per file

| File | Stato | Problemi e conformità | Intervento consigliato |
| --- | --- | --- | --- |
| `backend/app/api/v1/__init__.py` | Modificato | Esporta VAT, non Categories; manca newline finale. | Esportare il router Categories dopo la sua implementazione. |
| `backend/app/api/v1/categories.py` | Non tracciato, vuoto | Modulo HTTP assente. | Implementare router sottile con CRUD, codici HTTP e traduzione degli errori service. |
| `backend/app/api/v1/vat_rates.py` | Non tracciato | Separazione router/service sostanzialmente corretta; errori database non gestiti; update parziale esposto come PUT; manca newline finale. | Uniformare error handling, semantica update e stile. |
| `backend/app/main.py` | Modificato | Registra VAT correttamente; non registra Categories; usa `create_all()`; import dei modelli manuale e incompleto. | Registrare Categories e rimuovere `create_all()` quando la baseline Alembic è consolidata. |
| `backend/app/models/category.py` | Non tracciato | Import bloccante; struttura ORM gerarchica iniziale presente; timestamps ereditati; vincolo radici insufficiente; assenti politiche di eliminazione e validazioni. | Correggere import e definire vincoli, indici e relazioni coerenti con la politica gerarchica approvata. |
| `backend/app/models/__init__.py` | Tracciato, invariato | Non esporta Category; metadata Alembic incompleta. | Esportare Category. |
| `backend/app/models/base_model.py` | Tracciato, invariato | Fornisce correttamente ID e timestamp; `updated_at` dipende dall’ORM per l’aggiornamento. | Allineare tutte le migrazioni ai campi ereditati. |
| `backend/app/models/vat_rate.py` | Tracciato, invariato | Modello coerente nel dominio, ma non con la migrazione sui timestamp. | Allineare migrazione e modello. |
| `backend/app/models/user.py` | Tracciato, invariato | Modello presente, migrazione vuota; stile non uniforme. | Consolidare la baseline utenti in un task dedicato. |
| `backend/app/schemas/__init__.py` | Non tracciato | Esporta soltanto gli schemi VAT. | Esportare gli schemi Category dopo la correzione degli import. |
| `backend/app/schemas/category.py` | Non tracciato | Import bloccante; separazione Create/Update/Response presente; aggiornamento parziale modellato; validazioni insufficienti. | Usare una base schema esistente o introdurla esplicitamente; aggiungere vincoli di input. |
| `backend/app/schemas/vat_rate.py` | Non tracciato | Create/Update/Response separati; mancano validazioni; Update accetta null incompatibili. | Aggiungere vincoli e distinguere campo omesso da valore nullo non ammesso. |
| `backend/app/services/category_service.py` | Non tracciato, vuoto | Mancano CRUD e tutte le regole gerarchiche. | Implementare query, validazioni, transazioni ed errori applicativi. |
| `backend/app/services/vat_rate_service.py` | Non tracciato | CRUD presente e update usa correttamente `exclude_unset`; nessun rollback o traduzione delle violazioni. | Introdurre gestione transazionale coerente e tipi di ritorno. |
| `backend/app/database/base.py` | Tracciato, invariato | `naming_convention` non è una mapping valida. | Definire una naming convention SQLAlchemy completa e verificata. |
| `backend/app/database/session.py` | Tracciato, invariato | Configurazione engine valida strutturalmente; duplica `get_db`. | Conservare una sola dipendenza di sessione. |
| `backend/app/dependencies/db.py` | Tracciato, invariato | Dipendenza funzionante in struttura, ma duplicata. | Delegare o importare l’unica implementazione scelta. |
| `backend/app/core/config.py` | Tracciato, invariato | Legge `DATABASE_URL` e `SQL_ECHO` da ambiente; conforme alla configurazione esterna. | Usare la stessa configurazione anche per Alembic. |
| `backend/app/core/exceptions.py` | Tracciato, vuoto | Placeholder. | Definire eccezioni applicative quando richiesto dal consolidamento. |
| `backend/app/core/logging.py` | Tracciato, vuoto | Placeholder. | Nessun intervento necessario per Categories salvo logging richiesto. |
| `backend/app/core/security.py` | Tracciato, vuoto | Placeholder non pertinente a Categories. | Lasciare a un task dedicato. |
| `backend/app/dependencies/auth.py` | Tracciato, vuoto | Placeholder non pertinente a Categories. | Lasciare a un task dedicato. |
| `backend/app/dependencies/pagination.py` | Tracciato, vuoto | Placeholder; l’elenco Categories non ha ancora una strategia di paginazione. | Decidere nel task API se necessaria. |
| `backend/alembic/env.py` | Tracciato, invariato | Usa `Base.metadata`, ma importa solo i modelli esportati da `app.models`; Category esclusa. URL non derivato dalle settings applicative. | Registrare Category e unificare la configurazione URL. |
| `backend/alembic/versions/655402dd511f_create_vat_rates_table.py` | Tracciato, invariato | Manca `created_at` e `updated_at`. | Creare una migrazione correttiva verificabile. |
| `backend/alembic/versions/d09503f074f6_create_users_table.py` | Tracciato, invariato | Upgrade e downgrade vuoti. | Consolidare la migrazione utenti separatamente. |
| `backend/alembic/` | Nessuna nuova revisione | Migrazione Categories assente. | Aggiungere una revisione solo dopo approvazione del modello definitivo. |
| `docker-compose.yml` | Modificato | `env_file` è coerente; Compose valida; spazi finali; configurazione DB duplicata rispetto ad Alembic. | Rimuovere whitespace e mantenere una fonte esterna coerente per la connessione. |
| `backend/.env` | Ignorato da Git | Variabili richieste presenti; URL PostgreSQL usa correttamente l’host Compose `db`; nessun valore esposto. | Nessun intervento richiesto nell’audit. |

## 5. Review end-to-end Categories

**Model:** struttura iniziale corretta per una gerarchia adjacency-list, con `parent_id`, relazione bidirezionale, indice e timestamp ereditati. Non importabile, non registrato e privo delle garanzie necessarie su radici duplicate, cicli ed eliminazione.

**Schema:** Create, Update e Response sono distinti. L’import è inesistente; mancano limiti e normalizzazione. L’update può rappresentare correttamente “campo omesso” e “rimuovi padre”, purché il service usi `exclude_unset=True`.

**Service:** completamente assente.

**Router:** completamente assente.

**Registrazione:** assente sia nell’API sia nella metadata.

**Migrazione:** assente.

**Validazioni gerarchiche:** assenti per padre inesistente, auto-parenting, cicli, duplicati tra fratelli, duplicati radice ed eliminazione con figli.

**Test mancanti:** CRUD completo; 404; duplicati tra fratelli e radici; stesso nome sotto genitori diversi; auto-parenting; ciclo diretto e indiretto; cambio e rimozione padre; eliminazione con figli; update parziale; valori nulli; limiti di lunghezza; rollback dopo violazioni; coerenza migrazione/modello; registrazione OpenAPI.

## 6. Eventuali regressioni VAT

- La registrazione del router VAT in `main.py` rende disponibile il CRUD e corregge l’import errato precedente di engine.
- La nuova dipendenza da `app.schemas` e `app.services` richiede che tutti i file non tracciati VAT siano pubblicati insieme; in caso contrario l’applicazione non parte.
- Gli update espliciti a `null` possono violare i vincoli non nullable.
- Duplicati e altri errori di integrità non sono convertiti in risposte controllate e non provocano rollback.
- La migrazione VAT resta incompatibile con i timestamp ereditati.
- `create_all()` può mascherare l’incompletezza delle migrazioni e produrre schemi diversi tra installazioni.

## 7. Checklist

- [ ] Import Category corretti
- [ ] Category registrata nella metadata
- [ ] Schemi Category validati
- [ ] Service Categories implementato
- [ ] Router Categories implementato
- [ ] Router registrato in FastAPI
- [ ] Migrazione Categories creata
- [ ] Duplicati radice gestiti
- [ ] Auto-parenting impedito
- [ ] Cicli diretti e indiretti impediti
- [ ] Politica di eliminazione con figli approvata
- [ ] Rollback e integrità VAT consolidati
- [ ] Migrazioni VAT e User corrette
- [ ] `create_all()` rimosso dopo consolidamento Alembic
- [ ] Test automatici presenti
- [ ] OpenAPI verificata

## 8. Piano di consolidamento numerato

1. Correggere la configurazione di `Base.metadata` e definire la strategia unica di registrazione dei modelli.
2. Approvare le decisioni aperte sulla gerarchia Categories.
3. Correggere gli import Category e registrare modello e schemi nei rispettivi package.
4. Consolidare il model Category con vincoli, indici e comportamento delle relazioni approvati.
5. Completare e validare gli schemi Create, Update e Response.
6. Implementare il service Categories con validazioni gerarchiche, commit, refresh, rollback ed errori applicativi.
7. Implementare il router Categories e registrarlo nell’API.
8. Creare e revisionare la migrazione Categories, includendo ID, timestamp, vincoli, indice e foreign key.
9. Correggere la coerenza delle migrazioni esistenti per User e VAT.
10. Rimuovere `Base.metadata.create_all()` quando la baseline Alembic è affidabile.
11. Consolidare error handling e validazioni del modulo VAT.
12. Eliminare la duplicazione di `get_db` e unificare `DATABASE_URL` tra applicazione e Alembic.
13. Aggiungere test automatici per Categories, VAT, metadata e migrazioni.
14. Eseguire test di import, API e migrazione in un ambiente con le dipendenze installate.

## 9. Decisioni richieste al maintainer

1. Se l’eliminazione di una categoria con figli debba essere vietata, trasformata in disattivazione oppure gestita con un’altra politica esplicita.
2. Se i nomi categoria debbano essere univoci tra fratelli senza distinzione tra maiuscole/minuscole e spazi.
3. Se siano ammessi nomi uguali sotto genitori differenti.
4. Se la profondità della gerarchia debba essere illimitata o avere un limite.
5. Se l’aggiornamento parziale debba essere esposto con PATCH oppure mantenuto su PUT.
6. Quale strategia approvare per la baseline Alembic esistente, considerando la migrazione utenti vuota, i timestamp VAT mancanti e gli schemi eventualmente già creati da `create_all()`.

## 10. Conferma finale

Nessun file è stato modificato, creato, eliminato o rinominato durante l’audit. Nessuna migrazione è stata generata o applicata. Nessun container è stato avviato. Nessuna operazione di staging, commit o push è stata eseguita.
