# -*- coding: utf-8 -*-
from scrapy import Selector
from .baseSpider import BaseSpider


class Bet21Spider(BaseSpider):
    name = 'bet21'
    start_urls = ['https://www.21bet.co.uk/sportsbook/SOCCER/EU_CL/']

    def parse(self, response):
        selector = super(Bet21Spider, self).parse(response)
        team_link = Selector(
            text=selector.xpath(
                '//section[@class="app app--market"]//div[@class="app--outrights__container"]').extract_first())
        data = team_link.xpath('//li')
        result = dict()
        for team_link in data:
            row = Selector(text= team_link.extract())
            name = row.xpath('//span[@class="app--market__entry__name"]/text()').extract_first()
            coeff = row.xpath('//span[@class="app--market__entry__value"]/text()').extract_first()
            if not coeff:
                continue
            result[name] = coeff.strip('\n')
        self.driver.quit()
        yield result
