import sys
import csv
import json
import logging
from datetime import datetime
from time import time

from scrapy.conf import settings
from prettytable import PrettyTable
from scrapy.crawler import CrawlerProcess

from app.spiders.baseSpider import BaseSpider

logger = logging.getLogger()


def load_spiders():
    spiders = []
    data = {}
    try:
        data = json.load(open(settings.get('SPIDERS_CONFIG')))
    except Exception as e:
        logger.exception(e)
        logger.exception('Can\'t load spiders configuration file')

    for spider, spider_data in data.items():
        if not spider_data.get('is_active'):
            logger.info(f'Spider {spider} IS NO ACTIVE')
            continue

        spider_settings = spider_data.get('spider_settings', None)

        if spider_settings:
            spiders.append(type(spider, (BaseSpider,), spider_settings))
    return spiders


class BetsReporter(object):
    def __init__(self, spiders):
        self.spiders = spiders

    def output_to_console(self, matrix):
        p = PrettyTable()
        [p.add_row(row) for row in matrix]
        sys.stdout.write(p.get_string(header=False, border=False)+'\n')
        return None

    def output_to_file(self, matrix):
        with open('matrix.csv', 'w') as matrix_file:
            csv_writer = csv.writer(matrix_file, delimiter=',', quotechar=';')
            csv_writer.writerows(matrix)
            logger.info('Data stored to file')
        return None

    def process_data_files(self):
        logger.warning('producing final file')
        teams = set()
        file_head = [''] + [spider.name for spider in self.spiders]
        matrix_template = {k: [] for k in teams}
        path = settings.get('TMP_FOLDER')
        for i, spider in enumerate(self.spiders, start=1):
            with open(f'{path}/{spider.name}.json', 'r') as file:
                lines = file.readlines()

            for line in lines:
                try:
                    rate_source = json.loads(line)
                except Exception as e:
                    logger.exception(e)
                    continue
                [matrix_template.setdefault(row, ['N/A']*len(self.spiders)) for row in rate_source.keys()]

                for team, rate in rate_source.items():
                    matrix_template[team][i-1] = rate

        matrix = list()
        matrix.append(file_head)

        for team_name, rates in matrix_template.items():
            matrix.append([team_name]+rates)

        self.output_to_console(matrix)
        self.output_to_file(matrix)


def main():
    logger.warning('Start time {0}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    start = time()
    process = CrawlerProcess(settings)
    spiders = load_spiders()
    for spider in spiders:
        process.crawl(spider)
    process.start()
    reporter = BetsReporter(spiders=spiders)
    reporter.process_data_files()
    logger.warning('End')
    logger.warning('Runtime {0}'.format(time()-start))


if __name__ == '__main__':
    main()
