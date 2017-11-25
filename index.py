import sys
import csv
import json
import logging
from datetime import datetime
from time import time

from scrapy.conf import settings
from prettytable import PrettyTable
from scrapy.crawler import CrawlerProcess

from app.spiders.bet365 import Bet365spider
from app.spiders.paddypower import PaddypowerSpider
from app.spiders.williamhill import WilliamhillSpider
from app.spiders.bet21 import Bet21Spider
from app.spiders.spread import SpreadSpider
from app.spiders.sportsbet import SportBetSpider
from app.spiders.coral import CoralSpider
from app.spiders.titanbet import TitanBetSpider
from app.spiders.betstars import BetStartspider


spiders = [
    WilliamhillSpider,
    PaddypowerSpider,
    Bet21Spider,
    SpreadSpider,
    SportBetSpider,
    CoralSpider,
    TitanBetSpider,
    Bet365spider,
    BetStartspider,
    ]
logger = logging.getLogger()


class BetsReporter(object):
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
        file_head = [''] + [spider.name for spider in spiders]
        matrix_template = {k: [] for k in teams}
        path = settings.get('TMP_FOLDER')
        for i, spider in enumerate(spiders, start=1):
            with open(f'{path}/{spider.name}.json', 'r') as file:
                lines = file.readlines()

            for line in lines:
                try:
                    rate_source = json.loads(line)
                except Exception as e:
                    logger.exception(e)
                    continue
                [matrix_template.setdefault(row, ['N/A']*len(spiders)) for row in rate_source.keys()]

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
    for spider in spiders:
        process.crawl(spider)
    process.start()
    reporter = BetsReporter()
    reporter.process_data_files()
    logger.warning('End')
    logger.warning('Runtime {0}'.format(time()-start))


if __name__ == '__main__':
    main()
