import { Redirect, Route, Switch } from "react-router-dom"
import { AppShell } from "./components/AppShell"
import { Dashboard } from "./pages/Dashboard"
import { PlaceholderPage } from "./pages/PlaceholderPage"
import { ProductCatalog } from "./pages/ProductCatalog"
import { ProductDetail } from "./pages/ProductDetail"
import { ProductForm } from "./pages/ProductForm"
import "./styles.css"

export function App() {
  return (
    <AppShell>
      <Switch>
        <Route exact path="/" component={Dashboard} />
        <Route exact path="/prodotti" component={ProductCatalog} />
        <Route exact path="/prodotti/nuovo" component={ProductForm} />
        <Route exact path="/prodotti/:productId/modifica" component={ProductForm} />
        <Route exact path="/prodotti/:productId" component={ProductDetail} />
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
