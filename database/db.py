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
            # self.conn.commit
            # self.conn.close

    def add_customer(self, user_id):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f'INSERT INTO customer(user_id) VALUES ({user_id})')

    def check_balance(self, user_id):
        with self.conn:
            cursor = self.conn.cursor()
            data = cursor.execute(f'SELECT balance FROM users WHERE user_id = {user_id}')
            # self.conn.close
            return float(data.fetchone()[0])

    def update_balance(self, user_id, money):
        with self.conn:
            cursor = self.conn.cursor()
            balance = cursor.execute(f'SELECT balance FROM users WHERE user_id = {user_id}').fetchone()[0]
            new_balance = float(balance) + float(money)
            cursor.execute(f'UPDATE users SET balance = {new_balance} WHERE user_id = {user_id}')
            # self.conn.commit
            # self.conn.close

    def get_random_people(self, count):
        with self.conn:
            cursor = self.conn.cursor()
            selection = cursor.execute(f'SELECT user_id FROM users ORDER BY RANDOM() LIMIT {count}').fetchall()
            random_people = []
            for i in selection:
                random_people.append(str(i[0]))
            return random_people

    def create_task(self, author, message, picture, targets):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO task(author, message, picture, targets) VALUES(?, ?, ?, ?)',
                           (author, message, picture, targets)
                           )
