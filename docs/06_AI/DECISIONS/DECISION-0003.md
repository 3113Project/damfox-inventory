# DECISION-0003 — Regole gerarchiche Categories

## Stato

Accepted

## Decisione del maintainer

1. L'eliminazione di una categoria con figli è vietata e restituisce `409 Conflict`.
2. I nomi sono univoci tra categorie sorelle, ignorando maiuscole/minuscole e spazi iniziali o finali.
3. Lo stesso nome è consentito sotto genitori differenti.
4. La profondità della gerarchia non ha un limite fisso.
5. Auto-parenting e cicli diretti o indiretti sono sempre vietati.
6. Gli aggiornamenti parziali devono essere esposti tramite `PATCH`; `PUT` non deve essere usato per modifiche parziali.

## Conseguenze tecniche

- Il nome deve essere normalizzato prima delle verifiche di unicità.
- I duplicati tra categorie radice devono essere gestiti esplicitamente, senza affidarsi soltanto a `UNIQUE(parent_id, name)`.
- Il service deve verificare esistenza del padre, auto-parenting e cicli.
- La cancellazione deve controllare la presenza di figli prima di eliminare.
- API, test e documentazione devono riflettere queste regole.

## Collegamenti

- REVIEW-0010
- TASK-0016
- BUSINESS_RULES.md
