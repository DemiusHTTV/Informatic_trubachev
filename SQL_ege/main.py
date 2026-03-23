import pandas as pd
import sqlite3

conn = sqlite3.connect(":memory:")

store = pd.read_csv('SQL_ege/BD/store.csv', sep=';')
store.columns = ['ID магазина', 'Район']

goods = pd.read_csv('SQL_ege/BD/goods.csv', sep=';')
goods.columns = [
    "Артикул",
    "Отдел",
    "Наименование товара",
    "Ед изм",
    "Количество в упаковке",
    "Поставщик"
]

trade = pd.read_csv('SQL_ege/BD/trade.csv', sep=';')
trade.columns = [
    "ID операции",
    "Дата",
    "Магазин",
    "Артикул",
    "Операция",
    "Количество упаковок, шт",
    "Цена руб/шт"
]

store.to_sql('store', conn, index=False)
goods.to_sql('goods', conn, index=False)
trade.to_sql('trade', conn, index=False)

query = """
WITH coffee_sales AS (
    SELECT
        t."Магазин" AS store_id,
        SUM(t."Количество упаковок, шт" * t."Цена руб/шт") AS revenue
    FROM trade t
    JOIN goods g ON t."Артикул" = g."Артикул"
    WHERE g."Наименование товара" LIKE 'Кофе в зернах%'
      AND t."Операция" = 'Продажа'
    GROUP BY t."Магазин"
)
SELECT COUNT(*) AS store_count
FROM coffee_sales
WHERE revenue > 200000;
"""

result = pd.read_sql_query(query, conn)
print(result)