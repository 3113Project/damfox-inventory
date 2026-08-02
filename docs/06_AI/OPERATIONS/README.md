# Operations

Questa cartella contiene attività operative separate dai task applicativi.

## Convenzione

- identificativo: `OPS-XXXX`;
- file operativo: `OPS-XXXX.md`;
- report, quando richiesto: `REPORTS/OPS-XXXX-REPORT.md`;
- indice: `OPS_INDEX.md`.

## Ambito

Le operation possono riguardare:

- rebase e riallineamenti Git;
- risoluzione di conflitti;
- pubblicazione di commit già verificati;
- sincronizzazione repository;
- manutenzione documentale AI;
- release e infrastruttura.

Non devono introdurre funzionalità applicative non previste da un task.

## Stati

- `Planned`
- `In Progress`
- `Completed`
- `Blocked`
- `Cancelled`

## Regola di esecuzione

Codex deve leggere l'operation da `origin/main`, rispettare `AI_CONSTITUTION.md`, `CODEX_WORKFLOW.md` e `GIT_WORKFLOW.md`, modificare soltanto il perimetro autorizzato e produrre il report richiesto.
