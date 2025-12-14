# database/engine.py
import aiosqlite

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name

    async def create_tables(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price INTEGER,
                    schedule TEXT
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    student_name TEXT,
                    phone TEXT,
                    course_id INTEGER,
                    status TEXT DEFAULT 'paid'
                )
            """)
            
            await db.execute("INSERT OR IGNORE INTO courses (course_id, name, price, schedule) VALUES (1, 'Цікава інформатика(6-9років)', 100, 'Пн, Ср 19:00')")
            await db.execute("INSERT OR IGNORE INTO courses (course_id, name, price, schedule) VALUES (2, 'Базова інформатика(8-11 років)', 200, 'Вт, Чт 18:30')")
            await db.execute("INSERT OR IGNORE INTO courses (course_id, name, price, schedule) VALUES (3, 'Fround-End розробка(12-16 років)', 175, 'Вт, Чт 18:30')")
            await db.execute("INSERT OR IGNORE INTO courses (course_id, name, price, schedule) VALUES (4, 'Основи програмування Python(12-16 років)', 150, 'Вт, Чт 18:30')")
            await db.execute("INSERT OR IGNORE INTO courses (course_id, name, price, schedule) VALUES (5, '3D моделювання(12-16 років)', 300, 'Вт, Чт 18:30')")
            await db.execute("INSERT OR IGNORE INTO courses (course_id, name, price, schedule) VALUES (6, 'Компютерна грамотність для дорослих(18+)', 250, 'Вт, Чт 18:30')")

            await db.commit()

    async def get_courses(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM courses") as cursor:
                return await cursor.fetchall()

    async def get_course_by_id(self, course_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,)) as cursor:
                return await cursor.fetchone()

    async def add_student(self, user_id: int, name: str, phone: str, course_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                INSERT INTO students (user_id, student_name, phone, course_id, status)
                VALUES (?, ?, ?, ?, 'paid')
            """, (user_id, name, phone, course_id))
            await db.commit()

    async def get_all_students(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT user_id FROM students") as cursor:
                users_list = await cursor.fetchall()
                return [row[0] for row in users_list]
            
db_client = Database("besmart.db")
