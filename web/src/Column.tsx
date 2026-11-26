import type { components } from "./api-schema"
import Card from "./Card.tsx"

type ColumnGet = components["schemas"]["ColumnGet"]
import styles from "./Board.module.css"

type ColumnProps = {
  column: ColumnGet
}

export default function Column(props: ColumnProps) {
  return (
    <section className={styles.column}>
      <header className={styles.columnHeader}>
        <h2>{props.column.name}</h2>
        <span>{props.column.cards.length}</span>
      </header>
      {props.column.cards.length === 0 ? (
        <p>Нет карточек</p>
      ) : (
        // oxfmt-ignore
        props.column.cards.map((cardItem) =>
          <Card key={cardItem.id} card={cardItem} />)
      )}
    </section>
  )
}
