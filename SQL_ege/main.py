import pandas as pd
import sqlite3

conn = sqlite3.connect("::memory::")

store = pd.read_csv('SQL_ege/')
store =["ID операции",	'Дата',	'Магазин',	'Артикул'	'Операция',	"Количество упаковок, шт"	'Цена руб/шт']
goods = pd.read_csv('SQL_ege/')
goods=["Артикул",	"Отдел",	"Наименование товара',	'Ед изм	","Количество в упаковке",	"Поставщик"]
trade = pd.read_csv('SQL_ege/')

store, goods, trade,