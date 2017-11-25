# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Selector
from scrapy.spiders import Spider
from scrapy.conf import settings
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class BaseSpider(Spider):
    def _log(self, message):
        self.logger.warning(f'{self.name}: {message}')

    def parse(self, response):
        self.driver = webdriver.Firefox(executable_path=settings.get('WEB_DRIVER_PATH'))
        self.driver.get(response.url)
        WebDriverWait(self.driver, 5)
        sleep(20)
        return Selector(text=self.driver.page_source)
