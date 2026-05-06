import sqlite3


class Database:

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)

    def execute(self, sql: str, params: tuple = ()) -> None:
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def executemany(self, sql: str, seq_of_params: list[tuple]) -> None:
        try:
            cur = self.conn.cursor()
            cur.executemany(sql, seq_of_params)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def query(self, sql: str, params: tuple = ()) -> list[tuple]:
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()
        except Exception:
            raise

    def query_one(self, sql: str, params: tuple = ()) -> tuple | None:
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params)
            return cur.fetchone()
        except Exception:
            raise

    def close(self) -> None:
        self.conn.close()
