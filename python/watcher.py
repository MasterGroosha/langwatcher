# -*- coding: utf-8 -*-

import asyncio
from telethon import TelegramClient
import config
import dbworker
import api_calls
import utils


async def main():
    # Initiating connection to Telegram
    client = TelegramClient(config.session_name, config.api_id, config.api_hash)
    await client.connect()

    changes = {}
    has_changes = False

    for platform in ["Android", "iOS", "Android_X", "TDesktop"]:
        local_version = await dbworker.get_version(platform)
        if not local_version:
            local_version = 0

        # Note: Telegram expects platform name in lowercase, that's why we're using str.lower()
        # and keeping original names for readability later
        cloud_langpack = await api_calls.get_langpack(client, config.language, str.lower(platform), local_version)

        if cloud_langpack.version > local_version:
            changes[platform] = {"new": [], "changed": []}
            has_changes = True
            # There are some changes!
            changeset = await utils.prepare_dict(cloud_langpack)
            for key in changeset:
                existing = await dbworker.get(platform, key)
                if not existing:
                    changes[platform]["new"].append((key, changeset[key]))
                    await dbworker.insert_or_replace(platform, key, changeset[key])
                else:
                    changes[platform]["changed"].append((key, existing, changeset[key]))
                    await dbworker.insert_or_replace(platform, key, changeset[key])

            await dbworker.set_version(platform, cloud_langpack.version)
        else:
            continue  # No changes, skipping

    if has_changes:
        await utils.generate_post(changes)

    await client.disconnect()
    exit(0)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
