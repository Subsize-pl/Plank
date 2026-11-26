import type {components} from "./api-schema";
import Card from "./Card.tsx"

type ColumnGet = components['schemas']['ColumnGet']

type ColumnProps = {
  column: ColumnGet
}

export default function Column(props: ColumnProps) {
  return (
    <section>
      <h2>
        {props.column.name}
      </h2>
      {
        props.column.cards.map((cardItem) => (
          <Card key={cardItem.id} card={cardItem} />
          )
        )
      }
    </section>
  )
}
