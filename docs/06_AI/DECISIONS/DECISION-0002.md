# DECISION-0002 — Fondamenta prima delle funzionalità

## Stato

Accepted

## Contesto

L'audit tecnico ha rilevato debito su metadata SQLAlchemy, migrazioni, configurazione, transazioni, validazioni e test. Aggiungere nuovi moduli prima di consolidare questi aspetti aumenterebbe il costo di manutenzione.

## Decisione del maintainer

Fino alla milestone 1.0, la qualità delle fondamenta ha priorità assoluta rispetto all'aggiunta di nuove funzionalità.

Quando emerge un problema architetturale o infrastrutturale che compromette affidabilità, coerenza o testabilità, tale problema deve essere risolto prima di ampliare il dominio applicativo.

## Conseguenze

- Le nuove funzionalità possono essere bloccate da task di consolidamento.
- Nessun modulo è completo senza migrazione, validazioni, gestione errori, test e documentazione pertinenti.
- Categories sarà implementato solo dopo il consolidamento della baseline e del modulo VAT.
- Le review devono dichiarare esplicitamente se le fondamenta sono sufficienti per procedere.

## Collegamenti

- REVIEW-0010
- TASK-0014
- TASK-0015
- TASK-0016
- PROJECT_CONSTITUTION.md
