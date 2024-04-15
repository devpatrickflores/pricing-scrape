import scrapy
import re

class FishingRodsDetailedSpider(scrapy.Spider):
    name = "bcf_rods_detailed"
    allowed_domains = ["www.bcf.com.au"]
    start_urls = [
        f"https://www.bcf.com.au/fishing/fishing-rods?start={start}&sz=60" for start in range(0, 301, 60)
    ]

    def parse(self, response):
        self.logger.info('Extracting data from: %s', response.url)

        # Extracting titles and links
        product_links = response.css('.search-result-content .name-link::attr(href)').getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response):
        current_url = response.url
        product_code = re.search(r'/([A-Z0-9]+)\.html', current_url).group(1)
        headers_exist = response.css('.table-scroll thead th::text').getall()
        rows = response.css('.table-scroll tbody tr')

        # Extract title
        title = response.css(".product-name::text").get()

        if not headers_exist:
            data_rows = []
            for row in rows:
                column1_data_list = row.css('th::text').getall()
                column2_data_list = row.css('td::text').getall()
                
                if column1_data_list:
                    for column1_data, column2_data in zip(column1_data_list, column2_data_list):
                        data_row = {
                            'title': title,
                            'format': 'non-tabular',
                            'bcf_code': product_code,
                            column1_data.strip(): column2_data.strip() if column2_data else None,
                        }
                        data_rows.append(data_row)
            for data_row in data_rows:  # Yield each data_row separately
                yield data_row
        else:
            headers = headers_exist
            for row in rows:
                data = {'title': title}  # Adding title to data
                # Extracting data from each column in the row
                for index, header in enumerate(headers):
                    if index == 0:
                        # For the first column represented by <th>
                        value = row.css('th::text').get().strip()
                    else:
                        # For other columns represented by <td>
                        value = row.css(f'td:nth-child({index + 1})::text').get().strip()
                    data[header.strip()] = value
                data['bcf_code'] = product_code  # Add current_url to the data
                yield data
