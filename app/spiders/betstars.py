# -*- coding: utf-8 -*-
from scrapy import Selector
from scrapy.conf import settings
from selenium import webdriver

from .baseSpider import BaseSpider


class BetStartspider(BaseSpider):
    name = 'betstars'
    start_urls = ['https://www.betstars.com/#/soccer/outrights']

    def parse(self, response):
        self.driver = webdriver.Firefox(executable_path=settings.get('WEB_DRIVER_PATH'))
        self.driver.get(self.start_urls[0])
        selector = Selector(text=self.driver.page_source)

        data = selector.xpath('//div[@class="price"]')

        result = dict()

        for team_link in data:
            row = Selector(text=team_link.extract())
            name = row.xpath('//a//i/text()').extract_first()
            coeff = row.xpath('//a//em/text()').extract_first()
            if not coeff:
                continue
            name = name.replace("\t", "").replace("\n", "").replace('\xa0', '').replace(' ', '')
            name = name.strip()
            result[name] = coeff.replace("\t", "").replace("\n", "")
        self.driver.quit()
        yield result
