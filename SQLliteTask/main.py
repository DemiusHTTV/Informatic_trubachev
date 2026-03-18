from Nodes.database_node import Database

job_titles_data = [
    (1, "Менеджер"),
    (2, "Разработчик"),
    (3, "Аналитик"),
    (4, "Дизайнер")
]

employees_data = [
    (1, "Иванов", "Иван", 2),
    (2, "Петров", "Петр", 1),
    (3, "Сидорова", "Мария", 3),
    (4, "Козлов", "Алексей", 2),
    (5, "Васильева", "Ольга", 4)
]

db = Database("SQLliteTask/Nodes/company.db")

# Создание таблиц
db.query("""
CREATE TABLE IF NOT EXISTS job_titles (
    id_job_title INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
""")

db.query("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    id_job_title INTEGER NOT NULL,
    FOREIGN KEY(id_job_title) REFERENCES job_titles(id_job_title)
);
""")

# Вставка данных (перезаписываем, если скрипт запускается повторно)
db.executemany(
    "INSERT OR REPLACE INTO `job_titles` (`id_job_title`, `name`) VALUES (?, ?)",
    job_titles_data,
)
db.executemany(
    "INSERT OR REPLACE INTO `employees` (`id`, `surname`, `name`, `id_job_title`) VALUES (?, ?, ?, ?)",
    employees_data,
)

# Получение данных
employees_with_job_titles = db.query("""
SELECT e.surname, e.name, j.name as job_title
FROM employees e
JOIN job_titles j ON e.id_job_title = j.id_job_title
""")
## Легкие запросы, дэфолтные 

employee_count =db.query("""
SELECT COUNT(*) AS total_employees FROM employees;



""")
employee_max_id = db.query("""
                    SELECT MAX(id) AS max_employee_id FROM employees;
""")
employee_middle_name = db.query("""
                                SELECT name From employees WHERE id = {{employee_max_id[0][0]//2}};)""")

employee_sum_job_ids = db.query("""
                                    SELECT SUM(id_job_title) AS sum_job_ids FROM employees;
""")

employee_unique_job_count = db.query("""
SELECT COUNT(DISTINCT id_job_title) AS unique_job_count FROM employees;
""")

db.close()
print("---Легкие запросы---")
print(f"Общее количество сотрудников: {employee_count[0][0]}")
print(f"Максимальный ID сотрудника: {employee_max_id[0][0]}")
print(f"Имя сотрудника посередине: {employee_middle_name[0][0]}")
print(f"Сумма ID должностей сотрудников: {employee_sum_job_ids[0][0]}")
print(f"Количество уникальных должностей: {employee_unique_job_count[0][0]}")

# Вывод
print("Сотрудники с их должностями:")
for employee in employees_with_job_titles:
    print(f"{employee[0]} {employee[1]} - {employee[2]}")
