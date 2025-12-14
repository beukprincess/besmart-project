import aiosqlite

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name

    async def create_table(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    balance INTEGER DEFAULT 0,
                    username TEXT
                )
            """)
            await db.commit()

    async def add_user(self, user_id: int, username: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("INSERT INTO users (user_id, balance, username) VALUES (?, 500, ?) ON CONFLICT(user_id) DO UPDATE SET username = excluded.username", (user_id, username))
            await db.commit()
            
    async def get_all_users(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT user_id FROM users") as cursor:
                users_list = await cursor.fetchall()
                return [row[0] for row in users_list]

db_client = Database("besmart.db")