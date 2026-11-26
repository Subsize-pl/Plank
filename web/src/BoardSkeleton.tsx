import styles from "./Board.module.css"

export default function BoardSkeleton() {
  return(
    <main>
      <div className={styles.columns}>
        {[1,2,3].map((columnId) => (
        <section key={columnId} className={styles.column}>
          <div className={styles.skeletonHeading} />
            <div className={styles.skeletonCard} />
            <div className={styles.skeletonCard} />
        </section>
        ))}
      </div>
    </main>
  )
}
