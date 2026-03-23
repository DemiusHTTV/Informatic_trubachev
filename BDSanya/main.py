import pandas as pd
import sqlite3 
from datetime import datetime

dillers = pd.read_csv('dillers')
dillers.columns = ['ID', 'операции','Дата','ID машины','ID дилера','Количество','Тип операции']
marks = pd.read_csv('marks')
marks.columns = ['ID', 'машины','Категория','Наименование']
availability = pd.read_csv('availability')
availability = ['ID дилера','Адрес','ФИО директора'] 