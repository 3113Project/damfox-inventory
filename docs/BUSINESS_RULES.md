# BUSINESS RULES

Versione: 1.0

Questo documento contiene tutte le regole funzionali del progetto DAMFOX Inventory.

Le regole qui presenti rappresentano il comportamento che il software dovrà rispettare.

---

# PRODOTTI

## BR-001 - Identità del prodotto

Ogni prodotto rappresenta un articolo realmente gestito dalla ferramenta.

---

## BR-002 - SKU

Ogni prodotto possiede uno SKU interno univoco.

Lo SKU non cambia mai.

---

## BR-003 - Informazioni prodotto

Un prodotto può avere:

- descrizione
- immagini
- documenti PDF
- uno o più codici a barre

---

## BR-004 - Identificativi

Uno stesso prodotto può possedere:

- SKU interno
- Codice produttore
- Codice fornitore
- Codice EAN / Barcode

---

## BR-005 - Articoli indipendenti

Ogni variante commerciale è un prodotto indipendente.

Esempi:

- Vite TCEI M6x20
- Vite TCEI M6x25
- Vite TCEI M6x30

sono tre prodotti distinti.

Ogni prodotto possiede un proprio:

- SKU
- Barcode
- Magazzino
- Storico prezzi
- Fornitori

## BR-006 - Famiglie prodotto

I prodotti possono appartenere ad una famiglia.

La famiglia serve esclusivamente ad organizzare e facilitare la ricerca.

Non influenza:

- magazzino
- prezzi
- fornitori
- vendite

## BR-007 - Ricerca prodotti

La ricerca deve permettere di trovare rapidamente un prodotto utilizzando qualsiasi informazione significativa.

Ad esempio:

- SKU
- Barcode
- Codice fornitore
- Nome
- Marca
- Modello
- Descrizione
- Famiglia

## BR-008 - Documentazione

Ogni prodotto può avere allegati come:

- immagini
- schede tecniche
- manuali
- certificazioni
- link al sito del produttore

## BR-009 - Informazioni specifiche

Ogni categoria di prodotti può prevedere informazioni dedicate.

Esempi:

Bulloneria

- tipo
- diametro
- lunghezza
- materiale
- finitura

Elettroutensili

- marca
- modello
- tipo utensile
- potenza
- alimentazione

Il sistema deve rimanere semplice e contenere solo le informazioni realmente utili alla gestione del prodotto.

# FORNITORI

## BR-010 - Fornitori multipli

Uno stesso prodotto può essere acquistato da più fornitori.

---

## BR-011 - Informazioni specifiche del fornitore

Per ogni fornitore devono poter essere salvati:

- codice articolo del fornitore
- prezzo di acquisto
- eventuali sconti
- tempi di consegna
- note

---

## BR-012 - Prezzo di acquisto

Il prezzo di acquisto NON appartiene al prodotto.

Il prezzo appartiene al rapporto tra prodotto e fornitore.

---

# PREZZI

## BR-020 - Calcolo del prezzo

Il gestionale deve conoscere:

- prezzo netto
- IVA
- costo effettivo
- ricarico
- prezzo di listino
- eventuale sconto
- prezzo finale

---

## BR-021 - Ricarico

Il ricarico può essere differente per ogni prodotto.

In futuro potrà essere definito anche per categoria.

---

## BR-022 - IVA

L'IVA appartiene al prodotto.

---

## BR-023 - Prezzo manuale

Il prezzo di vendita può essere modificato manualmente.

Il sistema deve comunque mantenere il prezzo calcolato automaticamente.

---

## BR-024 - Visualizzazione prezzi

Il gestionale deve mostrare separatamente:

- prezzo netto
- IVA
- costo effettivo (netto + IVA)
- ricarico
- prezzo di listino
- sconto applicato
- prezzo finale

---

## BR-025 - Margine

Il gestionale deve calcolare automaticamente:

- margine lordo
- margine percentuale

---

# CLIENTI

## BR-030 - Prezzi personalizzati

In futuro il gestionale dovrà supportare:

- clienti privati
- clienti abituali
- aziende
- artigiani

Ogni cliente potrà avere condizioni commerciali differenti.

---

## BR-031 - Sconti

Lo sconto viene applicato al prezzo di listino.

Il gestionale deve mostrare sempre il margine residuo.

---

# STORICO

## BR-040 - Storico prezzi

Lo storico dei prezzi di acquisto non viene mai eliminato.

---

## BR-041 - Storico vendite

Ogni vendita deve poter essere ricostruita anche dopo anni.

---

## BR-042 - Tracciabilità

Ogni variazione di prezzo deve essere registrata.

---

# MAGAZZINO

## BR-050 - Quantità

Ogni prodotto possiede:

- quantità disponibile
- scorta minima

---

## BR-051 - Lista acquisti

Quando la quantità disponibile scende sotto la scorta minima, il prodotto entra automaticamente nella lista acquisti.

---

## BR-052 - Miglior fornitore

La lista acquisti deve suggerire automaticamente il fornitore economicamente più conveniente.

L'utente può comunque scegliere un fornitore differente.

---

## BR-053 - Unità di misura

Ogni prodotto possiede un'unità di misura principale.

Esempi:

- pezzo
- metro
- litro
- chilogrammo
- sacco
- cartuccia

## BR-054 - Unità di riferimento

Il magazzino gestisce sempre una sola unità di riferimento.

Eventuali confezioni sono conversioni dell'unità principale.

## BR-055 - Confezioni

Uno stesso prodotto può essere acquistato o venduto in confezioni differenti.

Esempi:

1 pezzo

1 scatola = 100 pezzi

1 cartone = 1000 pezzi

## BR-056 - Posizione di magazzino

Ogni prodotto può essere associato ad una posizione fisica del magazzino.

Esempio:

A-03-12

(corsia - scaffale - ripiano/cassetto)


# EVOLUZIONE DEL PROGETTO

## BR-100

Il database dovrà supportare senza modifiche strutturali:

- applicazione mobile
- scanner barcode
- importazione listini
- immagini
- documenti PDF
- dashboard
- statistiche
- intelligenza artificiale
- OCR di DDT e fatture