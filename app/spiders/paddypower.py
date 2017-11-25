# -*- coding: utf-8 -*-
from .baseSpider import BaseSpider


class PaddypowerSpider(BaseSpider):
    name = 'paddypower'
    start_urls = ['http://www.paddypower.com/football/euro-football/champions-league']

    def parse(self, response):
        selector = super(PaddypowerSpider, self).parse(response)
        team_links = selector.xpath("//div[contains(@class, fb-sub-content)]//div[contains(@class, fb-market-content)]//a[contains(@class, fb-odds-button)]")
        result = dict()
        for team_link in team_links:
            name = team_link.xpath('span[@class="odds-label"]/text()').extract_first()
            coeff = team_link.xpath('span[@class="odds-value"]/text()').extract_first()
            if not name:
                continue
            result[name] = coeff.strip('\n')
        self.driver.quit()
        yield result
