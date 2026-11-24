import type {components} from "./api-schema";

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
    </section>
  )
}
