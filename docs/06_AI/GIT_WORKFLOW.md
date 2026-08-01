# Git Workflow

## Scopo

GitHub è la fonte di verità del progetto DAMFOX Inventory. Codex opera sul repository locale collegato tramite SSH e pubblica modifiche soltanto quando il task lo autorizza esplicitamente.

## Ambiente di lavoro

- VS Code sul PC Windows.
- Connessione Remote SSH al server.
- Repository locale: `/srv/docker/damfox-inventory`.
- Codex eseguito localmente nell'estensione VS Code.
- Remote GitHub configurato tramite SSH.
- Repository remoto: `git@github.com:3113Project/damfox-inventory.git`.

## Ruoli

### Maintainer

- Definisce priorità.
- Approva funzionalità.
- Esegue test reali.
- Decide merge e release.

### ChatGPT

- Legge il repository GitHub.
- Analizza architettura e documentazione.
- Prepara task.
- Esegue review.
- Propone modifiche.
- Non opera autonomamente sul filesystem locale.

### Codex

- Legge i task.
- Modifica i file locali autorizzati.
- Esegue test e verifiche.
- Crea commit.
- Esegue push solo quando il task lo autorizza esplicitamente.

## Regole Git obbligatorie

1. Non usare mai `git add .`.
2. Non usare mai `git add -A`.
3. Aggiungere allo staging esclusivamente i file elencati nel task.
4. Non usare mai `git push --force`.
5. Non usare mai `git reset --hard`.
6. Non usare rebase, merge, pull o checkout senza autorizzazione esplicita.
7. Non modificare la cronologia Git.
8. Non includere modifiche non correlate nel commit.
9. Se il working tree contiene modifiche estranee al task, lasciarle intatte.
10. Prima del commit eseguire `git diff --cached`.
11. Dopo il commit verificare i file inclusi con `git show --stat --oneline HEAD`.
12. Il push è permesso solo se nel task è indicato `Push: YES`.
13. Se `Push: NO`, fermarsi dopo il commit.
14. Se il push fallisce, non tentare correzioni invasive: riportare l'errore e fermarsi.

## Branch

Per ora il progetto utilizza `main`. Con la crescita del progetto potranno essere adottati branch secondo queste convenzioni:

- `feature/<nome>`
- `fix/<nome>`
- `docs/<nome>`
- `refactor/<nome>`

Codex non deve creare branch senza istruzione esplicita.

## Commit

Usare Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:` e `chore:`. Ogni commit deve riguardare una sola attività coerente.

## Push

- Usare `git push origin <branch>`.
- Non eseguire mai force push.
- Verificare il remote prima del primo push.
- Fermarsi in caso di errore.
- Riportare branch, commit SHA ed esito.

## Pull request

In futuro le modifiche più importanti dovranno passare da branch e pull request.

## Procedura standard

1. Leggere il task.
2. Controllare `git status`.
3. Modificare solo i file autorizzati.
4. Eseguire test e verifiche.
5. Aggiungere solo i file autorizzati.
6. Controllare `git diff --cached`.
7. Creare il commit.
8. Controllare il commit.
9. Eseguire il push solo se autorizzato.
10. Restituire il report finale.
11. Fermarsi.
