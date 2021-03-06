import json

import scrapy

from kingfisher_scrapy.base_spider import CompressedFileSpider
from kingfisher_scrapy.util import components, handle_http_error


class Zambia(CompressedFileSpider):
    """
    Domain
      Zambia Public Procurement Authority
    """
    name = 'zambia'
    data_type = 'record_package'
    ocds_version = '1.0'

    def start_requests(self):
        yield scrapy.Request(
            'https://www.zppa.org.zm/ocds/services/recordpackage/getrecordpackagelist',
            meta={'file_name': 'list.json'},
            callback=self.parse_list
        )

    @handle_http_error
    def parse_list(self, response):
        urls = json.loads(response.text)['packagesPerMonth']

        for url in urls:
            # URL looks like https://www.zppa.org.zm/ocds/services/recordpackage/getrecordpackage/2016/7
            yield self.build_request(url, formatter=components(-2))
