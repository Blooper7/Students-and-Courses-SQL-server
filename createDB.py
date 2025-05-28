import sqlite3
import os

class CreateDB:
    db_name="StudentSQL"
    
    @classmethod
    def init_db(cls):
        sql_commands =[
            "CREATE TABLE IF NOT EXISTS Students("
            "studentId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            "firstName TEXT NOT NULL, "
            "lastName TEXT NOT NULL"
            ") STRICT;",
            "CREATE TABLE IF NOT EXISTS Courses("
            "courseId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            "courseCode TEXT NOT NULL, "
            "courseName TEXT NOT NULL"
            ") STRICT;",
            "CREATE TABLE IF NOT EXISTS Schedules("
            "studentId INTEGER NOT NULL, "
            "courseId INTEGER NOT NULL, "
            "PRIMARY KEY (studentId, courseId), "
            "FOREIGN KEY (studentId) REFERENCES Students(studentId) ON UPDATE CASCADE ON DELETE CASCADE, "
            "FOREIGN KEY (courseId) REFERENCES Courses(courseId) ON UPDATE CASCADE ON DELETE CASCADE"
            ") STRICT;"
        ]
        
        with sqlite3.connect(cls.db_name) as conn:
            cursor=conn.cursor()
            for sql_command in sql_commands:
                cursor.execute(sql_command)
            conn.commit()
            

if __name__ == "__main__":
    
    db_path="./"+CreateDB.db_name
    if os.path.exists(db_path):
        print(f"File '{db_path}' exists.")
    else:
        print(f"File '{db_path}' does not exist.")
        try:
            print(f"Creating database at {db_path}")
            CreateDB.init_db()
        except Exception as ex:
            print("Unable to create database!")
            raise ex
            