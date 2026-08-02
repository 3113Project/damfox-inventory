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

## Navigazione

L'app shell offre Dashboard, Prodotti, Categorie, Unità di misura e Impostazioni.
Su desktop usa una sidebar; sotto 760 px usa una barra di navigazione inferiore.
Le sezioni non ancora operative mostrano un empty state esplicito.

I componenti base sono in `src/components/ui.tsx`; colori, spaziatura, superfici,
stati e focus sono definiti come variabili in `src/styles.css`. La dashboard
mostra solo lo stato reale del backend e scorciatoie alle rotte disponibili.

## Catalogo prodotti

La rotta `/prodotti` usa esclusivamente le API reali. Ricerca, filtro famiglia e
filtro unità di misura sono inviati al backend come parametri query. Tabella,
empty state, dettaglio e form sono responsive.

Creazione e modifica caricano categorie, famiglie, aliquote IVA e unità di misura
dalle rispettive API. Lo SKU è richiesto in creazione e sola lettura in modifica;
l'unità di misura è sempre obbligatoria. Gli errori HTTP 404, 409 e 422 sono
tradotti in messaggi comprensibili.
