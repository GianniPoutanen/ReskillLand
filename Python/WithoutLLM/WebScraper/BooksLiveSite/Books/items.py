# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name: str | None = None
    
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    first_published = scrapy.Field()
    editions = scrapy.Field()
    ebooks = scrapy.Field()
    cover = scrapy.Field()

    pass
