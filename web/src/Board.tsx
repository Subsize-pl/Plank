import type { components } from "./api-schema"
import Column from "./Column.tsx";

type BoardGet = components["schemas"]["BoardGet"]

type BoardProps = {
  board: BoardGet
}

export default function Board(props: BoardProps) {
  return (
    <main>
      <h1>{props.board.name}</h1>
      {props.board.columns.length === 0 ? (
        <p>Нет колонок</p>
      ) : (
        props.board.columns.map((columnItem) => (
          <Column key={columnItem.id} column={columnItem} />
        ))
      )}
    </main>
  )
}

