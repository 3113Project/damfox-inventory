# Sincronizzazione Git sicura

## Scopo e limiti

`damfox-git-safe-sync` mantiene aggiornati i riferimenti remoti e può applicare esclusivamente un fast-forward quando il working tree locale è completamente pulito. Non sostituisce la review, non effettua push e non risolve divergenze.

Il push resta un'operazione autorizzata dal singolo task secondo [GIT_WORKFLOW.md](../06_AI/GIT_WORKFLOW.md). Non sono previsti hook `post-commit` né push automatici generici.

## Comportamento

Ad ogni esecuzione lo script esegue `git fetch --prune origin main`.

- Con working tree sporco, aggiorna solo i riferimenti `origin/*`; i file locali non cambiano e il fast-forward è saltato.
- Con working tree pulito e locale dietro al remoto, esegue solo `git merge --ff-only origin/main`.
- Con locale avanti, non esegue push.
- Con storie divergenti, registra un errore e non modifica il repository.

Un task remoto può essere letto senza applicarlo localmente:

```bash
git fetch origin main
git show origin/main:docs/06_AI/TASKS/TASK-XXXX.md
```

## Installazione

Dopo aver verificato i file versionati e se è disponibile sudo non interattivo:

```bash
sudo install -o root -g root -m 0755 scripts/git-safe-sync.sh /usr/local/bin/damfox-git-safe-sync
sudo install -o root -g root -m 0644 deploy/systemd/damfox-git-sync.service /etc/systemd/system/damfox-git-sync.service
sudo install -o root -g root -m 0644 deploy/systemd/damfox-git-sync.timer /etc/systemd/system/damfox-git-sync.timer
sudo systemctl daemon-reload
sudo systemctl enable --now damfox-git-sync.timer
sudo systemctl start damfox-git-sync.service
```

## Verifica e log

```bash
bash -n scripts/git-safe-sync.sh
scripts/git-safe-sync.sh --dry-run
systemd-analyze verify deploy/systemd/damfox-git-sync.service deploy/systemd/damfox-git-sync.timer
systemctl status damfox-git-sync.timer --no-pager
systemctl status damfox-git-sync.service --no-pager
systemctl list-timers damfox-git-sync.timer --no-pager
journalctl -u damfox-git-sync.service -n 50 --no-pager
```

## Disattivazione e rimozione

```bash
sudo systemctl disable --now damfox-git-sync.timer
sudo rm /etc/systemd/system/damfox-git-sync.service /etc/systemd/system/damfox-git-sync.timer
sudo rm /usr/local/bin/damfox-git-safe-sync
sudo systemctl daemon-reload
```

La rimozione delle unità non modifica i commit né le modifiche locali del repository.

## Comportamento in caso di divergenza

Lo script termina con errore e non tenta merge non fast-forward, rebase, reset, stash, clean o push. La divergenza richiede un intervento esplicito del maintainer.

## Documenti correlati

- [Workflow Git](../06_AI/GIT_WORKFLOW.md)
- [Workflow Codex](../06_AI/CODEX_WORKFLOW.md)
- [Task template](../06_AI/TASK_TEMPLATE.md)
