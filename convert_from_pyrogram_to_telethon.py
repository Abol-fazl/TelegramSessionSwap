import asyncio
import os
from glob import glob
from pathlib import Path

from pyrogram import Client
from telethon import TelegramClient
from telethon.crypto import AuthKey
from telethon.sessions import SQLiteSession

pyro_workdir = "pyro_data"
tele_workdir = "tele_data"

api_id = 6
api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

if not os.path.exists(tele_workdir):
    os.mkdir(tele_workdir)


async def convert(s_name: str):
    pyro_client = Client(
        s_name,
        api_id,
        api_hash,
        workdir=pyro_workdir
    )
    await pyro_client.storage.open()
    await pyro_client.storage.api_id(api_id)
    await pyro_client.storage.close()

    try:
        async with pyro_client:
            me = await pyro_client.get_me()
            session = f"+{me.phone_number}"
            server_address, port = pyro_client.session.connection.address

            sqlite = SQLiteSession(f"{tele_workdir}/{session}.session")
            sqlite.set_dc(pyro_client.session.dc_id, server_address, port)
            sqlite.auth_key = AuthKey(pyro_client.session.auth_key)
            sqlite.save()

            async with TelegramClient(sqlite, api_id, api_hash) as tl:
                tl_me = await tl.get_me()
                print(f"{tl_me.first_name} {tl_me.last_name}, {tl_me.id}")

    except Exception as e:
        return print(e, e.__traceback__.tb_lineno)


async def main():
    tasks = []
    for path in glob(f"{pyro_workdir}/*.session"):
        path = Path(path)
        tasks.append(asyncio.create_task(convert(path.stem)))

    return await asyncio.gather(*tasks)


asyncio.run(main())
