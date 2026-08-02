import { Redirect, Route, Switch } from "react-router-dom"
import { AppShell } from "./components/AppShell"
import { Dashboard } from "./pages/Dashboard"
import { PlaceholderPage } from "./pages/PlaceholderPage"
import "./styles.css"

export function App() {
  return (
    <AppShell>
      <Switch>
        <Route exact path="/" component={Dashboard} />
        <Route path="/prodotti">
          <PlaceholderPage title="Prodotti" description="Il catalogo prodotti sarà disponibile nel prossimo aggiornamento." />
        </Route>
        <Route path="/categorie">
          <PlaceholderPage title="Categorie" description="La gestione delle categorie non è ancora disponibile in questa interfaccia." />
        </Route>
        <Route path="/unita-di-misura">
          <PlaceholderPage title="Unità di misura" description="La gestione delle unità di misura non è ancora disponibile in questa interfaccia." />
        </Route>
        <Route path="/impostazioni">
          <PlaceholderPage title="Impostazioni" description="Non ci sono ancora impostazioni configurabili dal browser." />
        </Route>
        <Redirect to="/" />
      </Switch>
    </AppShell>
  )
}
