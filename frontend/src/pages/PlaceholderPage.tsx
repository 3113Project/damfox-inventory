import { EmptyState, PageHeader } from "../components/ui"

export function PlaceholderPage({ title, description }: { title: string; description: string }) {
  return (
    <>
      <PageHeader
        title={title}
        description="Questa sezione è già raggiungibile e sarà completata in modo incrementale."
      />
      <EmptyState title="Sezione in preparazione" description={description} />
    </>
  )
}
