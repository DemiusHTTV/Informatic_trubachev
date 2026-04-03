import sqlite3

class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('students.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students
                            (id_student INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_level INTEGER FOREIGN KEY NOT NULL,
                            id_group INtEGER FOREIGN KEY NOT NULL,
                            id_type_learning INTEGER FOREIGN KEY NOT NULL,
                            name TEXT NOT NULL,
                            surname TEXT NOT NULL,
                            father_name TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            grade_mean TEXT NOT NULL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS levels
                            (id_level INTEGER PRIMARY KEY AUTOINCREMENT,
                            level_name TEXT NOT NULL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS groups
                            (id_group INTEGER PRIMARY KEY AUTOINCREMENT,
                            group_name TEXT NOT NULL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS types_learning
                            (id_type_learning INTEGER PRIMARY KEY AUTOINCREMENT,
                            type_name TEXT NOT NULL)''')
        self.connection.commit()

    def query(self,sql,params =None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql,params)
        self.connection.commit()
        return self.cursor.fetchall()