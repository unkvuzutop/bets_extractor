# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Selector
from scrapy.conf import settings
from selenium import webdriver

from .baseSpider import BaseSpider


class CoralSpider(BaseSpider):
    name = 'coral'
    start_urls = ['http://sports.coral.co.uk/football/uefa-club-comps/champions-league']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'
    }
    def parse(self, response):
        self.driver = webdriver.Firefox(executable_path=settings.get('WEB_DRIVER_PATH'))
        self.driver.get(response.url)

        sleep(15)
        self.driver.find_element_by_class_name('fb-outrights').click()
        sleep(5)
        selector = Selector(text=self.driver.page_source)

        data = selector.xpath('//div[contains(@class,"outrights-match-")]')

        result = dict()
        for team_link in data:
            row = Selector(text= team_link.extract())
            name = row.xpath('//div[@class="outrights-betting-title"]/text()').extract_first()
            coeff = row.xpath('//span[@class="odds-fractional"]/text()').extract_first()
            if not coeff:
                continue
            result[name] = coeff.strip('\n')
        self.driver.quit()
        yield result
