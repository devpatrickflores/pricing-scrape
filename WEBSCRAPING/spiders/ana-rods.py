import scrapy

class FishingRodsSpider(scrapy.Spider):
    name = "ana_rods_listing"
    allowed_domains = ["www.anacondastores.com"]
    start_urls = [
        f"https://www.anacondastores.com/fishing/fishing-rods?q=&page={start}" for start in range(0, 100, 1)
    ]

    def parse(self, response):
        self.logger.info('Extracting: %s', response.url)

        # Extracting titles, links, prices, and club prices
        selectors = response.css('#productListWrapper .card-element')
        for selector in selectors:
            titles = selector.css('.card-link .card-headline::text').get()
            links = selector.css('.card-link::attr(href)').get()
            prices = selector.css('.pricing-wrapper .amount::text').get()
            club_prices = selector.css('.pricing-wrapper .price-now .amount::text').get()

            result = {
                'ANA Description': titles.strip() if titles else '',
                'ANA Link': response.urljoin(links) if links else '', 
                'ANA Price': prices.strip() if prices else '',
                'ANA Club Price': club_prices.strip() if club_prices else ''
            }
            yield result
