# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# TODO: these should be shared across spiders, and consider using Django models

class SeekJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    labels = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    country = scrapy.Field()
    sites = scrapy.Field()
    organisation = scrapy.Field()
    organisation_id = scrapy.Field()
    organisation_url = scrapy.Field()


class SeekOrganisationItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    country = scrapy.Field()


class SeekSiteItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
