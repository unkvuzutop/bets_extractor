# -*- coding: utf-8 -*-
from scrapy import Selector
from selenium import webdriver
from scrapy.conf import settings
from .baseSpider import BaseSpider
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Bet365spider(BaseSpider):
    name = 'bet365'
    start_urls = ['https://mobile.bet365.com/#type=Coupon;key=1-172-1-33380644-2-0-0-0-2-0-0-0-0-0-1-0-0-0-0-0-0;ip=0;lng=1;anim=1']

    def parse(self, response):
        self.driver = webdriver.Firefox(executable_path=settings.get('WEB_DRIVER_PATH'))
        self.driver.get(self.start_urls[0])
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "eventWrapper"))
        )
        selector = Selector(text=self.driver.page_source)

        data = Selector(
            text=selector.xpath('//div[@class="eventWrapper"]').extract_first()).xpath('//span[@class="opp"]')

        result = dict()

        for team_link in data:
            row = Selector(text= team_link.extract())
            name = row.xpath('//span[@class="opp"]/text()').extract_first()
            coeff = row.xpath('//span[@class="odds"]/text()').extract_first()
            if not coeff:
                continue
            name = name.replace("\t", "").replace("\n", "").replace('\xa0', '').replace(' ', '')
            name = name.strip()
            result[name] = coeff.replace("\t", "").replace("\n", "")
        self.driver.quit()
        yield result
