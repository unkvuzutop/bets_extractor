from .baseSpider import BaseSpider


class SportBetSpider(BaseSpider):
    name = "sportsbet"
    start_urls = ['https://www.sportsbet.com.au/betting/soccer/uefa-competitions/uefa-champions-league/Outright-Winner-2017/18-3373755.html']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'
    }

    def parse(self, response):
        selector = super().parse(response)
        team_links = selector.xpath('//div[@class="accordion-body"]//a[contains(@class, "price")]')
        result = dict()
        for team_link in team_links:
            name = team_link.xpath('span[contains(@class, "team-name")]/text()').extract_first()
            coeff = team_link.xpath('span[contains(@class, "odd-val")]/text()').extract_first()
            result[name] = coeff.strip('\n')
        self.driver.quit()
        yield result
