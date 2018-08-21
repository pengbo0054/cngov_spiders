# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    timestamp = Field()
    url = Field()
    body = Field()
    belong = Field()
    sub_belong = Field()
    keyword = Field()
    keyphase = Field()
    keysentence = Field()
    classes = Field()
