# -*- coding: utf-8 -*-

from telethon import TelegramClient
from telethon.tl.functions import InitConnectionRequest, InvokeWithLayerRequest
from telethon.tl.functions.langpack import GetDifferenceRequest
import config


async def get_langpack(client: TelegramClient, lang_code: str, platform_name: str, from_version: int = 0) -> int:
    """
    Gets langpack diff of full langpack if "from_version" set to 0

    :param client: TelegramClient instance
    :param lang_code: custom language identifier, e.g. "english", "mycustompack"
    :param platform_name: platform name, e.g. "android", "ios"
    :param from_version: Lower version to diff with
    :return: langpack difference
    """
    init_connection_request = InitConnectionRequest(
        api_id=client.api_id,
        lang_pack=platform_name,
        lang_code=lang_code,
        system_lang_code="ru",
        query=GetDifferenceRequest(from_version=from_version, lang_code=lang_code, lang_pack=platform_name),
        **{x: 'whatever' for x in ['device_model', 'system_version', 'app_version']}
    )
    lang_pack_difference = await client(InvokeWithLayerRequest(
        layer=config.current_layer, query=init_connection_request)
    )
    return lang_pack_difference
