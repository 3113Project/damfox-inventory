# DECISION-0005 — Fondazione frontend

## Stato

Accepted

## Decisione

Il primo frontend operativo di DAMFOX Inventory usa:

- React;
- TypeScript;
- Vite;
- React Router per la navigazione;
- TanStack Query per stato server, cache e richieste API;
- CSS modulare e variabili CSS proprie, senza introdurre inizialmente un framework UI pesante.

Il frontend vive in `frontend/`, viene eseguito come servizio Docker Compose separato e comunica con il backend FastAPI tramite URL configurabile da ambiente.

## Motivazione

La combinazione è diffusa, leggera, adatta a un'applicazione API-first e consente di produrre rapidamente interfacce responsive mantenendo tipizzazione e separazione dal backend. Evitare inizialmente un framework grafico completo riduce lock-in e permette di applicare direttamente `UI_GUIDELINES.md`.

## Vincoli

- TypeScript in modalità strict.
- Nessun accesso diretto al database.
- Nessun dato applicativo duplicato stabilmente nel client.
- Tutte le chiamate passano dalle API FastAPI.
- Configurazione runtime tramite variabili d'ambiente.
- Responsive e accessibilità devono essere considerate fin dal primo componente.
- Il primo verticale non implementa autenticazione, dashboard analitica, fornitori o magazzino.

## Conseguenze

- Docker Compose dovrà includere il servizio `frontend`.
- Il backend dovrà consentire l'origine frontend locale tramite configurazione CORS esplicita.
- Il primo schermo operativo sarà il catalogo prodotti.
- Componenti e stile iniziali dovranno restare semplici e riutilizzabili.