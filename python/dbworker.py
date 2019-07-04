# -*- coding: utf-8 -*-

import sqlite3
from typing import Optional
from config import db_name


async def insert_many(platform: str, items: dict) -> bool:
    statement = "INSERT into {0} (key, value) VALUES (?, ?)".format(platform)
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        for key in items:
            cursor.execute(statement, (key, items[key]))
    return True


async def insert_or_replace(platform: str, key: str, value: str) -> bool:
    statement = "INSERT OR REPLACE into {0} (key, value) VALUES (?, ?)".format(platform)
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute(statement, (key, value))
    return True


async def get(platform: str, key: str) -> Optional[str]:
    statement = "SELECT value FROM {0} WHERE key = ?".format(platform)
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        result = cursor.execute(statement, (key,)).fetchone()
        if result:
            return result[0]
        else:
            return None


async def set_version(platform: str, version: int) -> bool:
    statement = "INSERT OR REPLACE INTO versions (platform, version) VALUES (?, ?)"
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute(statement, (platform, version))
    return True


async def get_version(platform: str) -> Optional[int]:
    statement = "SELECT version FROM versions WHERE platform = ?"
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        version = cursor.execute(statement, (platform,)).fetchone()
        if version:
            return version[0]
        else:
            return None
