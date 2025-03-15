from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession
import asyncio

async def main():
    tdataFolder = r"C:\Users\Abolfazl\Downloads\Compressed\Telegram\tdata"
    tdesk = TDesktop(tdataFolder)
    assert tdesk.isLoaded()
    client = await tdesk.ToTelethon(session="telethon.session", flag=UseCurrentSession)
    await client.connect()
    await client.PrintSessions()

asyncio.run(main())