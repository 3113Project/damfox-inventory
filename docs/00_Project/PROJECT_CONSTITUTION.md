# DAMFOX Inventory — Project Constitution

## Scopo

Questo documento definisce i principi non negoziabili del progetto DAMFOX Inventory. Ogni decisione tecnica, funzionale, documentale o di interfaccia deve rispettarli.

## 1. Il software è progettato per persone non tecniche

L'utente finale può essere un addetto di ferramenta, un magazziniere, un impiegato o un tecnico senza competenze informatiche avanzate.

L'interfaccia deve essere comprensibile senza conoscere database, API o terminologia da sviluppatore.

Se una funzione richiede spiegazioni complesse per essere usata, va semplificata.

## 2. Semplicità prima della complessità

DAMFOX Inventory deve mostrare solo ciò che è utile nel contesto corrente.

Le opzioni avanzate devono essere introdotte solo quando servono e non devono ostacolare le operazioni comuni.

La complessità tecnica interna non deve essere trasferita all'utente.

## 3. I dati esistenti devono essere protetti

Nessuna modifica deve compromettere dati già presenti.

Ogni variazione strutturale del database deve passare attraverso una migrazione Alembic verificabile e reversibile quando ragionevole.

Campi, tabelle e relazioni non devono essere rinominati o rimossi senza una decisione documentata e una strategia di migrazione.

## 4. GitHub è la fonte di verità

Il repository GitHub ufficiale rappresenta lo stato condiviso e revisionabile del progetto.

Codice, documentazione, task, decisioni e roadmap devono restare coerenti con il contenuto pubblicato nel repository.

Le modifiche locali non pubblicate non devono essere presentate come funzionalità disponibili.

## 5. Codice e documentazione evolvono insieme

Una funzionalità non è completa finché non sono aggiornati, quando pertinenti:

- codice;
- migrazioni;
- test;
- documentazione API;
- modello dati;
- regole di business;
- roadmap;
- changelog;
- decisioni progettuali.

## 6. Il dominio guida l'architettura

Le regole funzionali definite in `BUSINESS_RULES.md` prevalgono sulle scorciatoie implementative.

Il software deve rappresentare correttamente il lavoro reale della ferramenta e del magazzino.

In caso di ambiguità, non si inventano regole: si inserisce `TODO: verificare con il maintainer`.

## 7. Separazione delle responsabilità

I router gestiscono HTTP e dipendenze.

I service contengono query, validazioni e logica applicativa.

Gli schema Pydantic validano input e definiscono output.

I modelli SQLAlchemy rappresentano i dati persistenti.

La logica di business non deve essere dispersa tra router, modelli e interfaccia.

## 8. Migrazioni controllate come unica strategia di schema

Alembic deve diventare l'unica fonte di verità per la creazione e l'evoluzione dello schema database.

Meccanismi automatici come `Base.metadata.create_all()` possono essere tollerati solo temporaneamente durante la fase iniziale e devono essere rimossi quando la baseline delle migrazioni è affidabile.

## 9. API stabili e prevedibili

Le API devono essere versionate, coerenti e documentate.

Una modifica incompatibile richiede approvazione esplicita, documentazione e strategia di transizione.

Gli errori devono essere chiari, consistenti e utili all'utente o al client.

## 10. Sicurezza e segreti

Nessun segreto deve essere inserito nel codice o nella documentazione pubblica.

Password, token e URL sensibili devono essere forniti tramite configurazione esterna.

Le password utente non devono mai essere archiviate in chiaro.

## 11. Qualità verificabile

Ogni modulo deve essere verificabile tramite test appropriati.

Le funzionalità critiche devono avere test automatici prima di essere considerate stabili.

I controlli manuali restano importanti, ma non sostituiscono una suite di test ripetibile.

## 12. Open source come obiettivo strutturale

Il progetto deve restare leggibile, installabile e comprensibile da collaboratori esterni.

Le convenzioni devono essere documentate e il codice non deve dipendere da conoscenze private non presenti nel repository.

La licenza definitiva deve essere approvata dal maintainer e aggiunta prima della pubblicazione ufficiale.

## 13. Accessibilità e usabilità

Il frontend futuro deve essere responsivo, accessibile e utilizzabile con tastiera, dispositivi mobili e lettori di codici a barre.

Il colore non deve essere l'unico mezzo per comunicare uno stato.

Le azioni distruttive devono essere chiaramente riconoscibili e confermate.

## 14. Crescita incrementale

Il progetto deve crescere per moduli verticali completi.

Ogni nuovo modulo dovrebbe includere, quando applicabile:

1. modello;
2. migrazione;
3. schema;
4. service;
5. router;
6. test;
7. documentazione;
8. frontend.

È preferibile completare un modulo coerente prima di iniziarne molti incompleti.

## 15. Ruoli nel workflow assistito da AI

Il maintainer decide direzione, priorità e approvazioni finali.

ChatGPT analizza GitHub, prepara task, revisiona architettura e documentazione e propone modifiche.

Codex opera sul repository locale, esegue task autorizzati, test, commit e push quando consentito.

Nessun agente deve ampliare autonomamente il perimetro di un task.

## Modifica della Costituzione

Questo documento può essere modificato solo con una decisione esplicita del maintainer.

Ogni modifica deve:

- essere motivata;
- essere registrata in `DECISIONS.md`;
- aggiornare i documenti correlati;
- non essere introdotta incidentalmente durante un task applicativo.

## Documenti correlati

- [Contesto AI](AI_CONTEXT.md)
- [Architettura](ARCHITECTURE.md)
- [Funzionalità](FEATURES.md)
- [Roadmap](ROADMAP.md)
- [Regole di business](../03_Business/BUSINESS_RULES.md)
- [Standard di sviluppo](../01_Development/CODING_STANDARDS.md)
- [Workflow Git](../06_AI/GIT_WORKFLOW.md)
