import csv
from pathlib import Path

from Nodes.database_node import Database


def load_from_csv() -> None:
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    db_path = base_dir / "Nodes" / "company.db"

    db = Database(str(db_path))
    db.query(
        """
        CREATE TABLE IF NOT EXISTS job_titles (
            id_job_title INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );
        """
    )
    db.query(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            surname TEXT NOT NULL,
            name TEXT NOT NULL,
            id_job_title INTEGER NOT NULL,
            FOREIGN KEY(id_job_title) REFERENCES job_titles(id_job_title)
        );
        """
    )

    
    db.execute("DELETE FROM employees")
    db.execute("DELETE FROM job_titles")

    job_titles_df = db.read_csv(data_dir / "job_titles.csv")
    job_titles_data = [
        (int(row["id_job_title"]), row["name"])
        for _, row in job_titles_df.iterrows()
    ]

    employees_df = db.read_csv(data_dir / "employees.csv")
    employees_data = [
        (
            int(row["id"]),
            row["surname"],
            row["name"],
            int(row["id_job_title"]),
        )
        for _, row in employees_df.iterrows()
    ]

    db.executemany(
        "INSERT INTO job_titles (id_job_title, name) VALUES (?, ?)",
        job_titles_data,
    )
    db.executemany(
        "INSERT INTO employees (id, surname, name, id_job_title) VALUES (?, ?, ?, ?)",
        employees_data,
    )

    result = db.query(
        """
        SELECT e.surname, e.name, j.name AS job_title
        FROM employees e
        JOIN job_titles j ON e.id_job_title = j.id_job_title
        ORDER BY e.id
        """
    )
    db.close()

    print("Импорт из CSV завершен. Записи:")
    for surname, name, job_title in result:
        print(f"{surname} {name} — {job_title}")


if __name__ == "__main__":
    load_from_csv()
