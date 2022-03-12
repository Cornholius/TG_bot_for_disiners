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

    def add_customer(self, user_id):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f'INSERT INTO customer(user_id) VALUES ({user_id})')

    def check_balance(self, user_id):
        with self.conn:
            cursor = self.conn.cursor()
            data = cursor.execute(f'SELECT balance FROM users WHERE user_id = {user_id}')
            return float(data.fetchone()[0])

    def update_balance(self, user_id, money):
        with self.conn:
            cursor = self.conn.cursor()
            balance = cursor.execute(f'SELECT balance FROM users WHERE user_id = {user_id}').fetchone()[0]
            new_balance = float(balance) + float(money)
            cursor.execute(f'UPDATE users SET balance = {new_balance} WHERE user_id = {user_id}')

    def get_random_people(self, count):
        with self.conn:
            cursor = self.conn.cursor()
            selection = cursor.execute(f'SELECT user_id FROM customer ORDER BY RANDOM() LIMIT {count}').fetchall()
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

    def get_all_tasks(self):
        with self.conn:
            cursor = self.conn.cursor()
            task = cursor.execute(f'SELECT * FROM task').fetchall()
            return task

    def get_current_task(self, task_id):
        with self.conn:
            cursor = self.conn.cursor()
            task = cursor.execute(f'SELECT * FROM task WHERE id = {task_id}').fetchone()
            return task

    def change_status_task(self, task_id, new_status):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f"UPDATE task SET status = '{new_status}' WHERE id = {int(task_id)}")

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute(f'DELETE FROM task WHERE id = {int(task_id)}')
