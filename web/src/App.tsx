import { useQuery } from "@tanstack/react-query"
import type { components } from "./api-schema"
import Column from "./Column.tsx"

type BoardGet = components['schemas']['BoardGet']

const boardId = '01a12d46-799b-7e82-8a0a-af401d97afaa'

async function loadBoard(): Promise<BoardGet> {
  const response = await fetch(`/api/v1/boards/${boardId}`)

  if (!response.ok) {
    throw new Error(`Ошибка API(${response.status})`)
  }

  return response.json()
}

export default function App() {
  const boardQuery = useQuery({
    queryKey: ['board', boardId],
    queryFn: loadBoard,
    retry: false
  })

  if (boardQuery.isPending) {
    return <p>Загружаем доску…</p>
  }

  if (boardQuery.isError){
    return (
      <div>
        <p>Не удалось загрузить доску. {boardQuery.error.message}</p>
        <button type="button" onClick={() => void boardQuery.refetch()}>
          Повторить
        </button>
      </div>
    )
  }

  return (
    <main>
      <h1>{boardQuery.data.name}</h1>
        {
          boardQuery.data.columns.map((columnItem) => (
            <Column key = {columnItem.id} column={columnItem} />
            )
          )
        }

    </main>
  )
}


