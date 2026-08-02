# DAMFOX Inventory frontend

Frontend React/TypeScript basato su Vite, React Router e TanStack Query.

## Configurazione

`VITE_API_BASE_URL` indica l'URL pubblico del backend visto dal browser. In Docker Compose il valore predefinito è `http://localhost:18000`; il frontend è pubblicato su `http://localhost:15173`.

## Verifiche

```bash
npm ci
npm run lint
npm test
npm run build
```
