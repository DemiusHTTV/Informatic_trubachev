from DB import DataBase


students = [
    {"name": "Ivan", "surname": "Moskvin", "father_name": "Sergeevich", "age": 20, "grade_mean": 16.7, "id_level": 1, "id_group": 1, "id_type_learning": 1},
    {"name": "Dmitriy", "surname": "Trubachev", "father_name": "Alexeevich", "age": 22, "grade_mean": 16.7, "id_level": 2, "id_group": 2, "id_type_learning": 2},
    {"name": "Georgiy", "surname": "Volovikov", "father_name": "Alexandrovich", "age": 21, "grade_mean": 20.1, "id_level": 1, "id_group": 3, "id_type_learning": 1},
    {"name": "Elena", "surname": "Kuznetsova", "father_name": "Dmitrievna", "age": 23, "grade_mean": 12.3, "id_level": 3, "id_group": 4, "id_type_learning": 2},
    {"name": "Sergey", "surname": "Volkov", "father_name": "Petrovich", "age": 20, "grade_mean": 13.5, "id_level": 2, "id_group": 4, "id_type_learning": 1},
]

# Типы обучения
type_of_learning = [
    {"id_type_learning": 1, "type_name": "Очная"},
    {"id_type_learning": 2, "type_name": "Заочная"},
]


groups = [
    {"id_group": 1, "group_name": "14123-ДБ"},
    {"id_group": 2, "group_name": "14121-ДБ"},
    {"id_group": 3, "group_name": "14122-ДБ"},
    {"id_group": 4, "group_name": "14223-ДБ"},
]


levels = [
    {"id_level": 1, "level_name": "Бакалавр"},
    {"id_level": 2, "level_name": "Магистр"},
    {"id_level": 3, "level_name": "Аспирант"},
]

db = DataBase()
db.executemany(
    "INSERT OR REPLACE INTO `types_learning` (`id_type_learning`, `type_name`) VALUES (?, ?)",
    [(t["id_type_learning"], t["type_name"]) for t in type_of_learning],    

)
db.executemany(
    "INSERT OR REPLACE INTO `groups` (`id_group`, `group_name`) VALUES (?, ?)",
    [(g["id_group"], g["group_name"]) for g in groups],
)
db.executemany(
    "INSERT OR REPLACE INTO `levels` (`id_level`, `level_name`) VALUES (?, ?)",
    [(l["id_level"], l["level_name"]) for l in levels],
)
db.executemany(
    "INSERT OR REPLACE INTO `students` (`id_level`, `id_group`, `id_type_learning`, `name`, `surname`, `father_name`, `age`, `grade_mean`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",    
    [(s["id_level"], s["id_group"], s["id_type_learning"], s["name"], s["surname"], s["father_name"], s["age"], s["grade_mean"]) for s in students],
)                    

count_students = db.query('''
SELECT id_student FROM students;
''')
print("Кол-во студентов:", len(count_students))

count_students_by_type = db.query('''
SELECT t.group_name, COUNT(s.id_student) AS student_count
FROM students s
JOIN groups t ON s.id_group = t.id_group
GROUP BY t.group_name;
                                                                                   '''
)

print("Кол-во студентов по группам:")
for group_name, student_count in count_students_by_type:
    print(f"{group_name}: {student_count}")


count_students_by_type =db.query('''
SELECT t.type_name, COUNT(s.id_student) AS student_count
FROM students s
JOIN types_learning t ON s.id_type_learning = t.id_type_learning
                                 GROUP BY t.type_name;''')

print("Кол-во студентов по типу обучения:")
for type_name, student_count in count_students_by_type:
    print(f"{type_name}: {student_count}")  
