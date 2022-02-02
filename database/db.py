import sqlite3


class Database:
    
    def __init__(self) -> None:
        self.conn = sqlite3.connect("./database/database.db")

    def check_or_create_user(self, user_id, first_name, last_name):
        with self.conn:
            cursor = self.conn.cursor()
            info = cursor.execute(f'SELECT * FROM users WHERE user_id = {user_id}')
            if info.fetchone() is None:
                cursor.execute(
                    'INSERT INTO users(user_id, first_name, last_name, balance) VALUES (?, ?, ?, ?)',
                    (user_id, first_name, last_name, 0))
            self.conn.commit
            self.conn.close

    def add_customer(self, user_id, first_name, last_name):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                    'INSERT INTO customer(user_id, first_name, last_name) VALUES (?, ?, ?)',
                    (user_id, first_name, last_name))
            self.conn.commit
            self.conn.close

    def check_balance(self, user_id):
        with self.conn:
            cursor = self.conn.cursor()
            data = cursor.execute(f'SELECT balance FROM users WHERE user_id = {user_id}')
            self.conn.close
            return int(data.fetchone()[0])

    def update_balance(self, user_id, money):
        with self.conn:
            cursor = self.conn.cursor()
            balance = cursor.execute(f'SELECT balance FROM users WHERE user_id = {user_id}').fetchone()[0]
            new_balance = int(balance) + int(money)
            cursor.execute(f'UPDATE users SET balance = {new_balance} WHERE user_id = {user_id}')
            self.conn.commit
            self.conn.close

    def get_random_people(self, count):
        cursor = self.conn.cursor()
        random_people = cursor.execute(f'SELECT user_id FROM customer by RANDOM() LIMIT {count}')
        print(random_people.fetchall())
