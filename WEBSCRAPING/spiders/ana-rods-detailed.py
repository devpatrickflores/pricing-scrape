import scrapy

class AnacondaSpider(scrapy.Spider):
    name = "ana_rods_detailed"
    allowed_domains = ["www.anacondastores.com"]
    start_urls = [
        f"https://www.anacondastores.com/fishing/fishing-rods?q=&page={start}" for start in range(0, 100, 1)
    ]

    def parse(self, response):
        self.logger.info('Extracting data from: %s', response.url)

        # Extract data from card elements
        product_links = response.css('.flexible-cards .card-element-wrapper .card-link::attr(href)').getall()
        for link in product_links:
            absolute_link = link  
            yield response.follow(absolute_link, callback=self.parse_product)

    def parse_product(self, response):
        # Parse product details
        item = dict()

        item["title"] = response.css(
            "#productContentWrapper > div::attr(data-product-name)"
        ).get()
        item["price"] = response.css(
            "#productContentWrapper .price-standard .amount::text"
        ).get()
        item["sale_price"] = response.css(
            "#productContentWrapper .price-vip .amount::text"
        ).get()
        item["size"] = response.css(
            "#productContentWrapper > div::attr(data-product-dimension13)"
        ).get()

        # Extract product details
        product_details = response.css('dl.product-details-list')
        for dt_dd_pair in product_details.css('dt, dd'):
            if dt_dd_pair.css('dt::text').get(): 
                key = dt_dd_pair.css('dt::text').get().strip()
                value = dt_dd_pair.xpath('normalize-space(following-sibling::dd[1]/text())').get()
                item[key] = value

        # yield the item with product details
        yield item

        # Now parse the colors
        color_urls = response.css(".js-variant-style-picker::attr(data-url)").getall()
        for url in color_urls:
            yield response.follow(url)

        # get all the sizes and scrape them
        size_codes = response.css(
            ".size-variant a::attr(data-variant-size-code)"
        ).getall()

        for code in size_codes:
            url = response.urljoin(code)
            yield scrapy.Request(url, callback=self.parse_size)

    def parse_size(self, response):
        item = dict()

        item["title"] = response.css(
            "#productContentWrapper > div::attr(data-product-name)"
        ).get()
        item["price"] = response.css(
            "#productContentWrapper .price-standard .amount::text"
        ).get()
        item["sale_price"] = response.css(
            "#productContentWrapper .price-vip .amount::text"
        ).get()
        item["size"] = response.css(
            "#productContentWrapper > div::attr(data-product-dimension13)"
        ).get()

        # Extract product details
        product_details = response.css('dl.product-details-list')
        for dt_dd_pair in product_details.css('dt, dd'):
            if dt_dd_pair.css('dt::text').get(): 
                key = dt_dd_pair.css('dt::text').get().strip()
                value = dt_dd_pair.xpath('normalize-space(following-sibling::dd[1]/text())').get()
                item[key] = value

        yield item
