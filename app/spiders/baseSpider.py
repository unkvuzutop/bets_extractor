# -*- coding: utf-8 -*-
from scrapy import Selector
from scrapy.spiders import Spider
from scrapy.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseSpider(Spider):
    def _log(self, message):
        self.logger.warning(f'{self.name}: {message}')

    def parse(self, response):
        self.driver = webdriver.Firefox(executable_path=settings.get('WEB_DRIVER_PATH'))
        self.driver.get(response.request.url)

        if hasattr(self, 'page_loaded_flag'):
            WebDriverWait(self.driver, settings.get('DRIVER_TIMEOUT')).until(
                EC.visibility_of_element_located((By.CLASS_NAME, self.page_loaded_flag)))

        if 'select_form' in self.xpath:
            select_form = self.xpath.get('select_form')

            WebDriverWait(self.driver, settings.get('DRIVER_TIMEOUT')).until(
                EC.presence_of_element_located((By.XPATH, select_form)))
            self.driver.find_element_by_xpath(select_form).click()
        selector = Selector(text=self.driver.page_source)
        if 'block_xpath' in self.xpath:
            block_xpath = self.xpath.get('block_xpath')
            elements_xpath = self.xpath.get('elements_xpath')

            WebDriverWait(self.driver, settings.get('DRIVER_TIMEOUT')).until(
                EC.presence_of_element_located((By.XPATH, block_xpath)))

            team_link = Selector(
                text=selector.xpath(
                    self.xpath.get('block_xpath')).extract_first())

            WebDriverWait(self.driver, settings.get('DRIVER_TIMEOUT')).until(
                EC.presence_of_element_located((By.XPATH, elements_xpath)))
            data = team_link.xpath(self.xpath.get('elements_xpath'))
        else:
            elements_xpath = self.xpath.get('elements_xpath')

            WebDriverWait(self.driver, settings.get('DRIVER_TIMEOUT')).until(
                EC.presence_of_element_located((By.XPATH, elements_xpath)))

            data = selector.xpath(self.xpath.get('elements_xpath'))

        result = dict()
        for team_link in data:
            row = Selector(text=team_link.extract())
            name = row.xpath(self.xpath.get('element_xpath_name')).extract_first()
            coeff = row.xpath(self.xpath.get('element_xpath_rate')).extract_first()
            if not coeff or not name:
                continue
            name = name.strip()

            result[name] = coeff.strip('\n').replace('\t', '').replace('\n', '')
        self.driver.quit()
        yield result
