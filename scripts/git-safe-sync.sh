#!/usr/bin/env bash
set -Eeuo pipefail

readonly REPOSITORY_DIR="/srv/docker/damfox-inventory"
readonly REMOTE="origin"
readonly BRANCH="main"
readonly LOCK_FILE="${REPOSITORY_DIR}/.git/damfox-git-safe-sync.lock"

DRY_RUN=false

log() {
    printf '%s [damfox-git-safe-sync] %s\n' "$(date --iso-8601=seconds)" "$*"
}

on_error() {
    local exit_code=$?
    log "ERROR: command failed with exit code ${exit_code}."
    exit "${exit_code}"
}

trap on_error ERR

usage() {
    printf 'Usage: %s [--dry-run]\n' "${0##*/}"
}

if [[ $# -gt 1 ]] || [[ ${1:-} == "--help" ]]; then
    usage
    exit 0
fi

if [[ ${1:-} == "--dry-run" ]]; then
    DRY_RUN=true
elif [[ $# -eq 1 ]]; then
    usage >&2
    exit 2
fi

if [[ ! -d "${REPOSITORY_DIR}" ]] || ! git -C "${REPOSITORY_DIR}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    log "ERROR: ${REPOSITORY_DIR} is not a Git repository."
    exit 1
fi

exec 9>"${LOCK_FILE}"
if ! flock -n 9; then
    log "Another synchronization is already running; skipping."
    exit 0
fi

log "Fetching ${REMOTE}/${BRANCH}${DRY_RUN:+ in dry-run mode}."
git -C "${REPOSITORY_DIR}" fetch --prune "${REMOTE}" "${BRANCH}"

if ! git -C "${REPOSITORY_DIR}" diff --quiet \
    || ! git -C "${REPOSITORY_DIR}" diff --cached --quiet \
    || [[ -n "$(git -C "${REPOSITORY_DIR}" ls-files --others --exclude-standard)" ]]; then
    log "Fetch completed; working tree is not clean, fast-forward skipped."
    exit 0
fi

readonly LOCAL_HEAD="$(git -C "${REPOSITORY_DIR}" rev-parse HEAD)"
readonly REMOTE_HEAD="$(git -C "${REPOSITORY_DIR}" rev-parse "${REMOTE}/${BRANCH}")"

if [[ "${LOCAL_HEAD}" == "${REMOTE_HEAD}" ]]; then
    log "Local branch is already synchronized with ${REMOTE}/${BRANCH}."
    exit 0
fi

if git -C "${REPOSITORY_DIR}" merge-base --is-ancestor "${LOCAL_HEAD}" "${REMOTE_HEAD}"; then
    if "${DRY_RUN}"; then
        log "Dry-run: local branch is behind; fast-forward would be applied."
        exit 0
    fi

    log "Local branch is behind; applying fast-forward only."
    git -C "${REPOSITORY_DIR}" merge --ff-only "${REMOTE}/${BRANCH}"
    log "Fast-forward completed."
    exit 0
fi

if git -C "${REPOSITORY_DIR}" merge-base --is-ancestor "${REMOTE_HEAD}" "${LOCAL_HEAD}"; then
    log "Local branch is ahead of ${REMOTE}/${BRANCH}; automatic push is disabled."
    exit 0
fi

log "ERROR: local and remote histories have diverged; no changes were applied."
exit 1
