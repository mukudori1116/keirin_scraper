# -*- coding: utf-8 -*-
import scrapy
import re
from keirin_scraper.items import KeirinScraperItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class KeirinSpider(scrapy.Spider):
    name = "Webspider"
    allowed_domains = ["keirin.kdreams.jp"]
    start_urls = ['https://keirin.kdreams.jp/kaisai/2017/01/01/']
    rules = (
        # データ抽出ルール
        Rule(LinkExtractor(
            unique=True # おなじリンク先ではデータ抽出しない
            ),
        ),
    )

    def parse(self, response):
        for href in response.css('.kaisai-program_table .result a::attr(href)'):
            full_url = response.urljoin(href.extract())
            urls.append(full_url)
            race_id = re.findall(r'\d{16}', full_url)[0]
            race_ids.append(race_id)
        yield scrapy.Request(full_url, callback=self.parse_race)

        # follow_link = response.css('.raceinfo-date_nav-next a::attr(href)')
        # follow_url = response.urljoin(follow_link.extract_first())
        # yield scrapy.Request(follow_url, callback=self.parse)
        
    def parse_race(self, response):
        players = []
        # 1 出走表 2 前回出走成績 3 今場所成績
        players1, players2, players3 = response.css('table.racecard_table')
        # 出走表より選手ごとの各種データ
        for player in players1.css('tr'):
            datas = player.css('td')
            players.append(datas[-19:])     # 車番データ~
        tmp = players[2:-1]             # カラム名と誘導員データを削除
        players = []
        for player in tmp:
            p = re.compile(r"<[^>]*?>")
            datas = [re.split('[\r\n\t/]', p.sub("", data).strip()) for data in player.css('td').extract()]
            pdic = {
                'bike_num': datas[0][0],
                'name': datas[1][0],
                'hometown': datas[1][-3],
                'age': datas[1][-2],
                'year': datas[1][-1],
                'rank': datas[2][0],
                'feet': datas[3][0],
                'gear': datas[4][0],
                'point': datas[5][0],
                'S': datas[6][0],
                'B': datas[7][0],
                'nige': datas[8][0],
                'makuri': datas[9][0],
                'sashi': datas[10][0],
                'mark': datas[11][0],
                'first': datas[12][0],
                'second': datas[13][0],
                'third': datas[14][0],
                'over_rank': datas[15][0],
                'win_rate': datas[16][0],
                'in_second_rate': datas[16][0],
                'in_third_rate': datas[16][0],
            }
            players.append(pdic)