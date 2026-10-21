import scrapy

from w3lib.url import add_or_replace_parameter
from Books.items import BookItem


class OpenLibrarySpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["openlibrary.org"]
    start_urls = ["https://openlibrary.org/trending/now"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, callback=self.parse, errback=self.log_error
            )

    def parse(self, response):
        """
        @url https://openlibrary.org/trending/now
        @returns items 20 20
        @returns request 1 50
        @scrapes url title price
        """
        books = response.css("div.sri__main")

        for book in books:
            href = book.css("h3.booktitle a.results::attr(href)").get()
            if not href:
                continue
            work_key = href.split("/works/")[1].split("/")[0]
            cover = book.css("img[itemprop=image]::attr(src)").get()
            details = book.css("span.resultDetails")

            item = BookItem()
            item["url"] = f"https://openlibrary.org/works/{work_key}"
            item["title"] = (book.css("h3.booktitle a.results::text").get() or "").strip()
            item["authors"] = book.css("span.bookauthor a::text").getall()
            item["first_published"] = details.css("span::text").re_first(r"First published in (\d{4})")
            item["editions"] = int(details.css("a::text").re_first(r"(\d+)\s+edition") or 0)
            item["ebooks"] = int(details.css("a::text").re_first(r"(\d+)\s+ebook") or 0)
            item["cover"] = response.urljoin(cover) if cover else None
            yield item
        
        
        pagination = response.css("ol-pagination")

        if pagination:
            current_page = int(pagination.attrib.get("current-page", "1"))
            total_pages = int(pagination.attrib.get("total-pages", "1"))

            if current_page < total_pages:
                next_page = current_page + 1
                next_page_url = add_or_replace_parameter(
                    response.url, "page", str(next_page)
                )

                self.logger.info(
                    f"Navigating to page {next_page}/{total_pages}: "
                    f"{next_page_url}"
                )

                yield scrapy.Request(
                    url=next_page_url,
                    callback=self.parse,
                    errback=self.log_error,
                )

    def log_error(self, failure):
        self.logger.error(repr(failure))
