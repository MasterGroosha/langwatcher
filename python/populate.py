# -*- coding: utf-8 -*-

"""
This script should be run when you want to create a database from the scratch!
"""

import asyncio
from telethon import TelegramClient
import config
import api_calls
import utils
import dbworker

LANG = "en"  # Choose what language you want to track

async def main():
    # Initiating connection to Telegram
    client = TelegramClient(config.session_name, config.api_id, config.api_hash)
    await client.connect()

    for platform in ["Android", "iOS", "TDesktop", "Android_X"]:  # macOS missing, add manually if you need
        # Getting full langpack and parsing it
        # TODO: Add checks!
        full_langpack = await api_calls.get_langpack(client, LANG, str.lower(platform))
        langpack_as_dict = await utils.prepare_dict(full_langpack)

        await dbworker.insert_many(platform, langpack_as_dict)
        await dbworker.set_version(platform, full_langpack.version)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
