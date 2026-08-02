1. Read AI_CONTEXT.md

2. Read ROADMAP.md

3. Read DATABASE.md

4. Never change APIs without approval.

5. Never remove existing code.

6. Ask before database migrations.

7. Update CHANGELOG.

8. Follow CODING_STANDARDS.

9. Produce one feature per task.

10. Wait for review.

## Build riproducibile e readiness

Le dipendenze runtime dirette sono fissate a versioni esatte in `backend/requirements.txt`. Per aggiornarle: modificare consapevolmente le versioni, eseguire una build senza cache e ripetere migrazioni e suite prima del commit.

```bash
docker compose build --no-cache backend
docker compose up -d db
docker compose run --rm backend alembic upgrade head
docker compose up -d backend
docker compose exec backend python scripts/wait_for_backend.py --timeout 60
docker compose exec backend python -m unittest discover -s tests -v
```

Lo script termina con codice diverso da zero al timeout. L’immagine backend include inoltre un `HEALTHCHECK` sullo stesso endpoint; PostgreSQL usa `pg_isready` e il backend viene avviato solo dopo il database healthy.

## Frontend locale

Il frontend React/TypeScript è eseguito da Vite nel servizio Compose `frontend`:

```bash
docker compose up --build -d
docker compose ps
```

Aprire `http://localhost:15173`; la pagina interroga il backend configurato con
`VITE_API_BASE_URL` (predefinito Compose: `http://localhost:18000`). Il backend
accetta soltanto le origini elencate in `CORS_ORIGINS`, separate da virgola;
Compose autorizza esplicitamente `http://localhost:15173`.

Quality gate frontend:

```bash
docker compose run --rm --no-deps frontend npm run lint
docker compose run --rm --no-deps frontend npm test
docker compose run --rm --no-deps frontend npm run build
```

Il `HEALTHCHECK` frontend verifica Vite sulla porta 5173; le dipendenze sono fissate in `frontend/package-lock.json`.
