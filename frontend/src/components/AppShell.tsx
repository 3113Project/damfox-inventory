import type { ReactNode } from "react"
import { NavLink } from "react-router-dom"

const navigation = [
  { to: "/", label: "Dashboard", mark: "D", exact: true },
  { to: "/prodotti", label: "Prodotti", mark: "P" },
  { to: "/categorie", label: "Categorie", mark: "C" },
  { to: "/unita-di-misura", label: "Unità", mark: "U" },
  { to: "/impostazioni", label: "Impostazioni", mark: "I" },
]

function Navigation({ mobile = false }: { mobile?: boolean }) {
  return (
    <nav className={mobile ? "mobile-nav" : "side-nav"} aria-label={mobile ? "Navigazione mobile" : "Navigazione principale"}>
      {navigation.map((item) => (
        <NavLink
          key={item.to}
          exact={item.exact}
          to={item.to}
          className="nav-link"
          activeClassName="nav-link--active"
        >
          <span className="nav-mark" aria-hidden="true">{item.mark}</span>
          <span>{item.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">Vai al contenuto</a>
      <header className="topbar">
        <NavLink className="brand" exact to="/" aria-label="DAMFOX Inventory, dashboard">
          <span className="brand-mark" aria-hidden="true">D</span>
          <span>
            <strong>DAMFOX</strong>
            <small>Inventory</small>
          </span>
        </NavLink>
        <span className="environment-label">Ambiente locale</span>
      </header>
      <aside className="sidebar">
        <p className="nav-heading">Workspace</p>
        <Navigation />
        <p className="sidebar-note">Inventario semplice, dati affidabili.</p>
      </aside>
      <main className="content" id="main-content" tabIndex={-1}>
        {children}
      </main>
      <Navigation mobile />
    </div>
  )
}
