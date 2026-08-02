import type {
  ButtonHTMLAttributes,
  InputHTMLAttributes,
  ReactNode,
  SelectHTMLAttributes,
} from "react"

export function PageHeader({ title, description, actions }: { title: string; description?: string; actions?: ReactNode }) {
  return (
    <header className="page-header">
      <div>
        <p className="eyebrow">DAMFOX Inventory</p>
        <h1>{title}</h1>
        {description && <p className="page-description">{description}</p>}
      </div>
      {actions && <div className="page-actions">{actions}</div>}
    </header>
  )
}

export function Button({ className = "", ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button className={`button ${className}`.trim()} {...props} />
}

export function Input({ label, hint, id, ...props }: InputHTMLAttributes<HTMLInputElement> & { label: string; hint?: string }) {
  const inputId = id ?? `input-${label.toLowerCase().replace(/\s+/g, "-")}`
  const hintId = hint ? `${inputId}-hint` : undefined
  return (
    <label className="field" htmlFor={inputId}>
      <span className="field-label">{label}</span>
      <input className="input" id={inputId} aria-describedby={hintId} {...props} />
      {hint && <span className="field-hint" id={hintId}>{hint}</span>}
    </label>
  )
}

export function Select({
  label,
  options,
  id,
  ...props
}: SelectHTMLAttributes<HTMLSelectElement> & {
  label: string
  options: Array<{ value: string; label: string }>
}) {
  const selectId = id ?? `select-${label.toLowerCase().replace(/\s+/g, "-")}`
  return (
    <label className="field" htmlFor={selectId}>
      <span className="field-label">{label}</span>
      <select className="select" id={selectId} {...props}>
        {options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
      </select>
    </label>
  )
}

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <section className={`card ${className}`.trim()}>{children}</section>
}

export function Badge({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "success" | "danger" }) {
  return <span className={`badge badge--${tone}`}>{children}</span>
}

export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <Card className="state-panel">
      <span className="state-icon" aria-hidden="true">◇</span>
      <h2>{title}</h2>
      <p>{description}</p>
    </Card>
  )
}

export function LoadingState({ label = "Caricamento…" }: { label?: string }) {
  return (
    <div className="inline-state" role="status">
      <span className="spinner" aria-hidden="true" />
      <span>{label}</span>
    </div>
  )
}

export function ErrorState({ title = "Si è verificato un problema", description }: { title?: string; description: string }) {
  return (
    <div className="error-state" role="alert">
      <strong>{title}</strong>
      <span>{description}</span>
    </div>
  )
}
