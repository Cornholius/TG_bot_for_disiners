import sqlite3

from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
import asyncio
# from database.db import Database
api_id = 13293247
api_hash = 'aed5f6a7274a6952078152081c197a64'
# db = Database()
#
# async def get_user_id_from_username():
#     with open('123.txt', 'r') as file:
#         nicknames = file.readlines()
#     count = 0
#
#     for username in nicknames:
#         count += 1
#         async with TelegramClient('Little helper', api_id, api_hash) as client:
#             user = await client(GetFullUserRequest(username))
#         print(count, user.user.id)
#         await asyncio.sleep(1)
#
#
# asyncio.run(get_user_id_from_username())

with open('123.txt', 'r') as file:
    nicknames = file.readlines()


async def main(users):
    count = 1
    async with TelegramClient('name', api_id, api_hash) as client:
        for username in users:
            user = await client(GetFullUserRequest(username))
            count += 1
            conn = sqlite3.connect("database.db")
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO customer(user_id, first_name, last_name) VALUES (?, ?, ?)',
                    (user.user.id, user.user.first_name, user.user.last_name))
                conn.commit
                conn.close
                # db.add_customer(user.user.id, user.user.first_name, user.user.last_name)
            print(count, user.user.id, user.user.first_name, user.user.last_name)

    await client.run_until_disconnected()

asyncio.run(main(nicknames))