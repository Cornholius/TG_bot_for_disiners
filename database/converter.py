import sqlite3

from telethon import TelegramClient, events, functions
import asyncio
api_id = 13293247
api_hash = 'aed5f6a7274a6952078152081c197a64'

# with open('100.txt', 'r') as file:
#     nicknames = file.readlines()

async def main(users):
    ppl = [362594800, 1121467380, 5038372944, 1695990268]
    async with TelegramClient('name', api_id, api_hash) as client:
        # full = await client(functions.users.GetFullUserRequest(users))
        # print(full)
        for i in ppl:
            try:
                await client.send_message(entity=i, message='это тестовое сообщение. не обращайте на него внимания')
                print(f'sending to {i} OK')
            except:
                print(f'sending to {i} FAILED')
        # count = 0
        # with open('temp.txt', 'a') as temp:
        #     for i in nicknames:
        #         count += 1
        #         try:
        #             full = await client(functions.users.GetFullUserRequest(i))
        #             # print(nicknames.pop(nicknames.index(i)))
        #             temp.write(f'{full.user.username} {full.user.id} {full.user.first_name} {full.user.last_name}\n')
        #             # print(count, full.user.id, full.user.first_name, full.user.last_name)
        #             nicknames.remove(i)
        #
        #         except:
        #             print(count, '!!!')
        # with open('100.txt', 'w') as file:
        #     for i in nicknames:
        #         file.write(i)

asyncio.run(main(5038372944))

# from telethon.sync import TelegramClient
# from telethon import functions, types
#
# with TelegramClient('name', api_id, api_hash) as client:
#     result = client(functions.users.GetFullUserRequest('@zondishe'))
#     print(result.stringify())
#