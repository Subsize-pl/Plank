import type { components } from "./api-schema"

type CardGet = components["schemas"]["CardGet"]

type CardProps = {
  card: CardGet
}

export default function Card(props: CardProps) {
  return (
    <section>
      <h3>{props.card.title}</h3>
    </section>
  )
}
