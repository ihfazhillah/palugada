import re
from dataclasses import dataclass, asdict
from typing import List, TypedDict

import feedparser
import requests
from django.conf import settings

from config.celery_app import app as celery_app
from sembada.feeds.models import FeedItem, FeedTag, FeedUrl


@dataclass
class Item:
    title: str
    guid: str
    url: str
    description: str
    tags: List[str]


class ItemDict(TypedDict):
    title: str
    guid: str
    url: str
    description: str
    tags: List[str]


def fcm_sender(input: ItemDict):
    devices = FCMDevice.objects.all()
    title = input["title"]
    description = input["description"]

    devices.send_message(title=title, description=description[:100], data={"type": "feed", "data": input})



def telegram_bot_sender(input: ItemDict):
    url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"

    link = input["url"]
    title = input["title"]
    description = input["description"]

    to_excaped = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

    for exc in to_excaped:
        if exc in link:
            link = link.replace(exc, f"\\{exc}")

    for exc in to_excaped:
        if exc in title:
            title = title.replace(exc, f"\\{exc}")

    for exc in to_excaped:
        if exc in description:
            description = description.replace(exc, f"\\{exc}")

    text = f"*{title}*\n{description[:200]}\\.\\.\\.\n[Read More]({link})"
    data = dict(
        chat_id=settings.TG_BOT_ADMIN,
        text=text,
        parse_mode="MarkdownV2"
    )
    response = requests.post(url, json=data)
    print(response.json())

class OnNewFeedItem:
    receivers = [telegram_bot_sender, fcm_sender]
    def dispatch(self, data: dict):
        for receiver in self.receivers:
            receiver(data)

on_new_feed_item = OnNewFeedItem()

def parse_one_feed(label, url):
    doc = feedparser.parse(url)
    entries = [entry for entry in doc.entries]
    entries.reverse()
    for entry in entries:
        item, created = FeedItem.objects.get_or_create(
            guid=entry["id"],
            defaults=dict(
                title=entry.title,
                url=entry.link,
                description=entry.description
            )
        )

        if not created:
            tag, _ = FeedTag.objects.get_or_create(name=label)
            if not item.tags.filter(name=tag.name).exists():
                item.tags.add(tag)

        if created:
            item_dict = asdict(
                Item(
                    item.title,
                    item.guid,
                    item.url,
                    item.description,
                    [tag.name for tag in item.tags.all()]
                )
            )

            on_new_feed_item.dispatch(item_dict)


@celery_app.task
def feed_parser_task():
    for feed_url in FeedUrl.objects.all():
        parse_one_feed(feed_url.name, feed_url.url)
