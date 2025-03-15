import asyncio
import os
from glob import glob
from pathlib import Path

from pyrogram import Client
from telethon import TelegramClient

pyro_workdir = "pyro_data"
tele_workdir = "tele_data"

api_id = 6
api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

if not os.path.exists(pyro_workdir):
    os.mkdir(pyro_workdir)


async def convert(s_name: Path):
    tele_client = TelegramClient(s_name, api_id, api_hash)
    try:
        await tele_client.connect()
        me = await tele_client.get_me()
        user_id = me.id
        is_bot = me.bot
        auth_key = tele_client.session.auth_key.key
        dc_id = tele_client.session.dc_id
        s_name = Path(s_name).stem
        await tele_client.disconnect()

        pyro_client = Client(s_name, api_id, api_hash,
                                workdir=pyro_workdir)

        storage = pyro_client.storage

        await storage.open()
        await storage.auth_key(auth_key)
        await storage.date(0)
        await storage.dc_id(dc_id)
        await storage.user_id(user_id)
        await storage.is_bot(is_bot)
        await storage.test_mode(False)
        await storage.api_id(api_id)
        await storage.save()
        await storage.close()

        await pyro_client.connect()
        me = await pyro_client.get_me()
        print(me.first_name, me.last_name, me.id)
        await pyro_client.disconnect()

    except Exception as e:
        return print(e, e.__traceback__.tb_lineno)


async def main():
    tasks = []
    for path in glob(f"{tele_workdir}/*.session"):

        tasks.append(asyncio.create_task(convert(path)))

    return await asyncio.gather(*tasks)


asyncio.run(main())
