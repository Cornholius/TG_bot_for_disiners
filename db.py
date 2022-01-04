import sqlite3


class Database():
    
    def __init__(self) -> None:
        self.conn = sqlite3.connect("database.db")

    def check_or_create_user(self, user_id):
        with self.conn:
            cursor = self.conn.cursor()
            info = cursor.execute(f'SELECT * FROM users WHERE user_id = {user_id}')
            if info.fetchone() is None:
                cursor.execute(f'INSERT INTO users(user_id, balance) VALUES ({user_id}, 0)')
            self.conn.commit
            self.conn.close

    def check_balance(self, user_id):
        with self.conn:
            cursor = self.conn.cursor()
            data = cursor.execute(f'SELECT balance FROM users WHERE user_id = {user_id}')
            self.conn.close
            return data.fetchone()[0]

    def update_balance(self, new_balance, user_id):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f'UPDATE users SET balance = {new_balance} WHERE user_id = {user_id}')
            self.conn.commit
            self.conn.close
            
