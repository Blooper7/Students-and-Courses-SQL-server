import os
import sqlite3

class DataAccess:
    primary_keys={"Students":"studentId","Courses":"courseId"}
    
    def __init__(self):
        self.db_path='./StudentSQL'
    
    def db_exists(self):
        return os.path.exists(self.db_path)
    
    def get_table_names(self):
        sql_command = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql_command)
            #print(cur.fetchall())
            return [row["name"] for row in cursor.fetchall()]
    
    def get_table_columns(self, table_name:str)->list[str]:
        sql_command = f"PRAGMA table_info('{table_name}')"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cur = conn.execute(sql_command)
            return [row["name"] for row in cur.fetchall()]
    
    
    # Handle Students
    def create_student(self, first, last):
        sql_command = f"INSERT INTO Students(firstName, lastName) VALUES ('{first}', '{last}');"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cur=conn.execute(sql_command)
    
    def delete_student(self, first, last):
        sql_command = f"DELETE FROM Students WHERE firstName='{first}' AND lastName='{last}';"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cur=conn.execute(sql_command)
    
    def get_all_student_data(self):
        sql_command = "SELECT * FROM Students;"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cursor=conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(sql_command)
        return [[row["studentId"], row["firstName"], row["lastName"]] for row in cursor.fetchall()]
    
    #Handle Courses
    def create_course(self, courseCode, courseName):
        sql_command = f"INSERT INTO Courses(courseCode, courseName) VALUES ('{courseCode}', '{courseName}');"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cur=conn.execute(sql_command)
    
    def delete_course(self, courseCode, courseName):
        sql_command = f"DELETE FROM Courses WHERE courseCode='{courseCode}' AND courseName='{courseName}';"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cur=conn.execute(sql_command)

    def get_all_course_data(self):
        sql_command = "SELECT * FROM Courses;"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cursor=conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(sql_command)
        return [[row["courseId"], row["courseCode"], row["courseName"]] for row in cursor.fetchall()]
    
    #Handle Schedules
    def create_schedule_item(self, studentId, courseId):
        sql_command = f"INSERT INTO Schedules(studentId, courseId) VALUES ({studentId}, {courseId});"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cur=conn.execute(sql_command)
    
    def delete_schedule_item(self, studentId, courseId):
        sql_command = f"DELETE FROM Schedules WHERE studentId={studentId} AND courseId={courseId};"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cur=conn.execute(sql_command)
    
    def get_all_schedules(self):
        sql_command = "SELECT * FROM Schedules;"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cursor=conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(sql_command)
        return [[row["studentId"], row["courseId"]] for row in cursor.fetchall()]
    
    def lookup_by_id(self, table, item_id):
        sql_command = f"SELECT * FROM {table} WHERE {self.primary_keys[table]}={item_id};"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cursor=conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(sql_command)
        return cursor.fetchone()
    
    def make_schedule_references(self, schedule_data):
        data=[[] for i in range(len(schedule_data))]
        for i in range(len(schedule_data)):
            data[i].append(' '.join(self.lookup_by_id("Students",schedule_data[i][0])[1:]))
            data[i].append(self.lookup_by_id("Courses",schedule_data[i][1])[1])
        return data
    
    def get_student_schedule(self, studentId):
        sql_command=f"SELECT * FROM Schedules WHERE studentId={studentId};"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory=sqlite3.Row
            cursor=conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(sql_command)
        data=cursor.fetchall()
        return self.make_schedule_references(data)
    
if __name__ == "__main__":
    da=DataAccess()
    #print(da.db_exists())
    tables=da.get_table_names()
    print(tables)
    for t in tables:
        print(f"Table: {t}")
        for c in da.get_table_columns(t):
            print(f"\t{c}")
    #da.create_student("Joe", "Mama")
    #da.create_student("Tom", "Smith")
    #da.delete_student("first=Bob", "last=Ross")
    #print(da.get_all_student_data())
    
    #da.create_schedule_item(2, 2)
    print(da.get_all_schedules())
    print(da.lookup_by_id("Students", 2)[1])
    print(da.get_student_schedule(2))
    