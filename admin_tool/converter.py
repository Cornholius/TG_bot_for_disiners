import json
from telethon import TelegramClient
import asyncio

with open('config.json') as conf:
    config = json.load(conf)
    api_id = config['api_id']
    api_hash = config['api_hash']


with open('targets.txt', 'r') as trgs:
    targets = trgs.readlines()
    peoples = [target.strip() for target in targets]

with open('message.txt') as msg:
    message = msg.read()


async def main():
    async with TelegramClient('name', api_id, api_hash) as client:
        for people in peoples:
            try:
                await client.send_message(entity=int(people), message=message)
                print(f'sending to {people} OK')
                peoples.remove(people)
            except:
                print(f'sending to {people} FAILED')
        with open('targets.txt', 'w') as file:
            for people in peoples:
                file.write(f'{people}\n')


asyncio.run(main())
