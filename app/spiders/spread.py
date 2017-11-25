# -*- coding: utf-8 -*-
from scrapy import Selector
from scrapy.conf import settings
from selenium import webdriver

from .baseSpider import BaseSpider


class SpreadSpider(BaseSpider):
    name = 'spreadex'
    start_urls = ['https://www.spreadex.com/sports/en-GB/spread-betting/Football-European/UEFA-Champions-League/Long-Term-Markets/p644607']

    def parse(self, response):
        self.driver = webdriver.Firefox(executable_path=settings.get('WEB_DRIVER_PATH'))
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        table = Selector(text=selector.xpath('//div[contains(@class, pricing-panel)]').extract_first())
        data = table.xpath('//td')
        result = dict()
        for team_link in data:
            row = Selector(text=team_link.extract())
            name = row.xpath('//div[@class="name"]/text()').extract_first()
            coeff = row.xpath('//span[@class="oddsFractional"]/text()').extract_first()
            if not coeff:
                continue
            result[name] = coeff.strip('\n')
        self.driver.quit()
        yield result
