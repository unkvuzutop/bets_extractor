# -*- coding: utf-8 -*-
from .baseSpider import BaseSpider


class WilliamhillSpider(BaseSpider):
    name = 'williamhill'
    start_urls = ['http://sports.williamhill.com/bet/en-gb/betting/e/11195829/UEFA+Champions+League+2017+2018.html']

    def parse(self, response):
        selector = super(WilliamhillSpider, self).parse(response)
        team_links = selector.xpath('//div[@class="marketHolderExpanded"]//td[@scope="col"]')
        result = dict()
        names = team_links.xpath('//div[contains(@class,"eventselection")]/text()').extract()
        coeffs = team_links.xpath('//div/div[@class="eventprice"]/text()').extract()
        for name, coeff in zip(names, coeffs):
            name = name.replace("\t", "").replace("\n", "")
            name = name.strip()
            result[name] = coeff.replace("\t", "").replace("\n", "")
        self.driver.quit()
        yield result
