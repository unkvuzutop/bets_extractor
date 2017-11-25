# -*- coding: utf-8 -*-
from app.spiders.baseSpider import BaseSpider


class TitanBetSpider(BaseSpider):
    name = "titanbet"
    start_urls = ['http://sports.titanbet.com/en/t/19161/UEFA-Champions-League?mkt_sort=X086']

    def parse(self, response):
        selector = super().parse(response)
        team_buttons = selector.xpath('//div[contains(@class, "pager-page")]//button[contains(@name, "add-to-slip")]')
        result = dict()
        for button in team_buttons:
            name = button.xpath('span/span/span/span[@class="seln-name"]/text()').extract_first()
            if not name:
                continue
            coeff = button.xpath('span/span[contains(@class, "frac")]/text()').extract_first()
            result[name] = coeff
        self.driver.quit()
        yield result
