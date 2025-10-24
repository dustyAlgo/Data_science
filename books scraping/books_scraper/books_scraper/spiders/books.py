import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    '''def parse(self, response):
        links_href = []
        for links in response.css("a"):
            #print("link -->", links.attrib["href"])
            links_href.append(links.attrib["href"])
        return{"links_colums":links_href}
        '''
    '''def parse(self, response):
        # Loop through each <a> tag
        for link in response.css("a::attr(href)").getall():
            # Yield each link as a separate row
            yield {"links": link}'''
    def parse(self, response):
        # Loop through all book links on the current page
        for book_link in response.css("ol.row article.product_pod a"):
            yield response.follow(book_link.attrib["href"], callback=self.extract_book)

        # Follow the next page link to crawl all pages
        for next_page_link in response.css("ul.pager li.next a"):
            yield response.follow(next_page_link.attrib["href"], callback=self.parse)

    def extract_book(self, response):
        # Extract book details from the product page
        title = response.css("div.product_main h1::text").get()
        price = response.css("div.product_main p.price_color::text").get()
        description = response.css("#product_description + p::text").get()

        # Extract the product information table
        table_info = response.css("table.table").get()
        book_info = pd.read_html(table_info)[0].set_index(0).to_dict()[1]

        # Add other fields to the book info
        book_info["title"] = title
        book_info["price"] = price
        book_info["description"] = description

        return book_info