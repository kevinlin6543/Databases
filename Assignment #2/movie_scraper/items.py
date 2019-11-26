# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    consensus = scrapy.Field()
    critic_rating = scrapy.Field()
    critic_count = scrapy.Field()
    user_rating = scrapy.Field()
    audience_count = scrapy.Field()

    rating = scrapy.Field()
    runtime = scrapy.Field()
    studio = scrapy.Field()
    genre = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    air_date = scrapy.Field()
