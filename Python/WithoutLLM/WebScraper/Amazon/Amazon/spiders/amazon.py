import scrapy

from Amazon.items import AmazonItem


class Amazonpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["www.amazon.com.au"]
    start_urls = ["www.amazon.com.au/amz-books/store?node=4851626051&ref_=apb_psf&ie=UTF8&ref_=nav_cs_books&ccs_id=79ba0706-427a-4cd1-b31b-7c9c01d737a9"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, callback=self.parse, errback=self.log_error
            )

    def parse(self, response):
        """
        @url https://www.amazon.com.au
        @returns items 20 20
        @returns request 1 50
        @scrapes url title price
        """
        for book in response.css("div[data-testid^='book']"):
            face = book.css("bds-unified-book-faceout")
            asin = face.attrib.get("data-csa-c-item-id")
            if not asin:
                continue
            item = AmazonItem()
            item["_id"] = asin
            item["url"] = f"https://www.amazon.com.au/dp/{asin}"
            item["binding"] = face.attrib.get("data-csa-c-binding")
            item["rank"] = book.attrib.get("data-index")
        yield item
        
        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(
                f"Navigating to next page with URL {next_page_url}."
            )
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                errback=self.log_error,
            )
    def log_error(self, failure):
        self.logger.error(repr(failure))
