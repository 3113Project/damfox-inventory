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
