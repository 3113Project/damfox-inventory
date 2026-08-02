# DECISION-0004 — Intervallo valido per le aliquote IVA

## Stato

Accepted

## Data

2026-08-02

## Contesto

TASK-0015 richiede una regola applicativa esplicita per validare il campo `rate` delle aliquote IVA. La documentazione precedente non definiva l'intervallo consentito e Codex ha arrestato correttamente il task senza inventare una regola.

## Decisione del maintainer

Il campo `rate` deve accettare valori decimali compresi tra:

- minimo: `0.00`;
- massimo: `100.00`;
- estremi inclusi;
- massimo due cifre decimali.

Sono quindi validi, a titolo di esempio:

- `0.00`;
- `4.00`;
- `5.00`;
- `10.00`;
- `22.00`;
- `100.00`.

Sono invece non validi:

- valori negativi;
- valori maggiori di `100.00`;
- valori con più di due cifre decimali;
- `null` nei campi obbligatori.

## Motivazione

L'intervallo rappresenta una percentuale applicativa. `0.00` resta ammesso per aliquote a zero; la descrizione e il nome dell'aliquota devono distinguere i diversi significati fiscali o commerciali. Il limite superiore `100.00` mantiene il dominio coerente e impedisce valori tecnicamente memorizzabili ma semanticamente non validi.

## Conseguenze

- Lo schema Pydantic deve validare `rate` nell'intervallo inclusivo `0.00–100.00`.
- Il database deve applicare un vincolo `CHECK` equivalente.
- Create e PATCH devono rifiutare valori fuori intervallo.
- Gli errori di validazione devono essere deterministici.
- I test devono coprire minimo, massimo, valori fuori intervallo e precisione eccessiva.

## Task e review collegati

- `TASK-0015`
- `REVIEW-0010`
- `REVIEW-0014`
