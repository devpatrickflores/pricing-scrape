import scrapy

class FishingRodsSpider(scrapy.Spider):
    name = "bcf_rods_listing"
    allowed_domains = ["www.bcf.com.au"]
    start_urls = [
        f"https://www.bcf.com.au/fishing/fishing-rods?start={start}&sz=60" for start in range(0, 301, 60)
    ]

    def parse(self, response):
        self.logger.info('Extracting: %s', response.url)

        # Extracting titles, links, prices, and club prices
        selectors = response.css('#search-result-items .grid-tile')
        for selector in selectors:
            titles = selector.css('.name-link::text').get()
            links = selector.css('.name-link::attr(href)').get()
            prices = selector.css('.product-sales-price::text').get()
            club_prices = selector.css('.member-price span:first-child::text').get()
            result = {
                'BCF Description': titles.strip() if titles else '', 
                'BCF Link': response.urljoin(links) if links else '', 
                'BCF Price': prices.strip() if prices else '',  
                'BCF Club Price': club_prices.strip() if club_prices else '' 
            }
            yield result
