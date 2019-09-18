# -*- coding: utf-8 -*-

import feedparser
import telebot
from vedis import Vedis
from time import mktime, sleep
from urllib.parse import quote_plus

msg_template = """<b>{title}</b>

<a href="{link_iv}">Instant View</a>

<a href="{link_regular}">View on Web</a>
"""

last_sync_time = 0
with Vedis("storage.vdb") as db:
    try:
        last_sync_time = db["last_sync"].decode()
    except KeyError:
        pass  # Already 0

FEED_URL = "https://username.github.io/langwatcher/posts/index.xml"
bot = telebot.TeleBot("1234567890:AaBbCcDdXxYyZz")

feed = feedparser.parse(FEED_URL)
entries = feed["entries"]
entries.reverse()  # Retain chronological order

for entry in entries:
    if int(mktime(entry["published_parsed"])) > int(last_sync_time):
        iv = "https://t.me/iv?url={}&rhash=yourivhash".format(quote_plus(entry["link"]))
        bot.send_message(1234567, # Whatever chat_id you'd like
                        parse_mode="html",
                        text=msg_template.format(title=entry["title"], link_iv=iv, link_regular=entry["link"]))
        sleep(1)

# Update last_sync_time
with Vedis("storage.vdb") as db:
    db["last_sync"] = int(mktime(entries[-1]["published_parsed"]))
