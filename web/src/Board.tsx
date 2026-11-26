import type { components } from "./api-schema"
import Column from "./Column.tsx"
import styles from "./Board.module.css"

type BoardGet = components["schemas"]["BoardGet"]

type BoardProps = {
  board: BoardGet
}

export default function Board(props: BoardProps) {
  return (
    <main>
      <h1>{props.board.name}</h1>
      <div className={styles.columns}>
        {props.board.columns.map((columnItem) => (
          <Column key={columnItem.id} column={columnItem} />
        ))}
      </div>
    </main>
  )
}
