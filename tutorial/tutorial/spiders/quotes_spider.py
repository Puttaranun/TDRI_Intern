import scrapy

# To save everything in a file

class QuoteSpider(scrapy.Spider):
    name = "quotes"

    ## Manually request the urls
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]

    #     for url in urls:
    #         yield scrapy.Request(url=url, callback = self.parse)

    # Using default implementation of start_requests()
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    # parse() methods is the Scrapy's default callback method
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


# To extract quote by various request methods

class QuoteSpider2(scrapy.Spider):
    name = "quotes2"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        ## To scrape some selected data
        for quote in response.css('div.quote'):
            yield {
                'text' : quote.css('span.text::text').get(),
                'author' : quote.css('small.author::text').get(),
                'tags' : quote.css('div.tags a.tag::text').getall(),
            }

        
        ## Full written with if
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     ## Full written next page request
        #     # next_page = response.urljoin(next_page)
        #     # yield scrapy.Request(next_page, callback=self.parse)
        #     yield response.follow(next_page, call_back=self.parse)

        ## Shortcut by request tag <href> in for loop
        # for href in response.css('ul.pager a::attr(href)'):
        #     yield response.follow(href, call_back=self.parse)

        ## Shortcut by request tag <a>
        # for a in response.css('ul.pager a'):
        #     yield response.follow(a, call_back=self.parse)

        ## Multiple requests
        # anchors = response.css('ul.pager a')
        # yield from response.follow_all(anchors, callback=self.parse)

        yield from response.follow_all(css='ul.pager a', callback=self.parse)


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate' : extract_with_css('.author-born-date::text'),
            'bio' : extract_with_css('.author-description::text'),
        }
