# -*- coding: utf-8 -*-
import scrapy
import re
from keirin_scraper.items import KeirinScraperItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import numpy as np
import pandas as pd


class KeirinSpider(scrapy.Spider):
    name = "Webspider"
    allowed_domains = ["keirin.kdreams.jp"]
    start_urls = ['https://keirin.kdreams.jp/kaisai/2011/12/22/']
    rules = (
        # データ抽出ルール
        Rule(LinkExtractor(
            unique=True     # おなじリンク先ではデータ抽出しない
        ),
        ),
    )

    def parse(self, response):
        for href in response.css(
                '.kaisai-program_table .result a::attr(href)'):
            full_url = response.urljoin(href.extract())
            if href is not None:
                yield scrapy.Request(full_url, callback=self.parse_race)
            else:
                pass

        follow_link = response.css('.raceinfo-date_nav-next a::attr(href)')
        follow_url = response.urljoin(follow_link.extract_first())
        if follow_url is not None:
            yield scrapy.Request(follow_url, callback=self.parse)

    def parse_race(self, response):
        item = KeirinScraperItem()
        url = response.url
        race_id = re.findall(r'\d{16}', url)[0]
        item['race_id'] = race_id
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
            if player.css('td::text').extract_first() is not None:
                p = re.compile(r"<[^>]*?>")
                datas = [
                    re.split(
                        '[\r\n\t/]',
                        p.sub("", data).strip().replace(" ", "").replace("\u3000", "")
                    )
                    for data
                    in player.css('td').extract()
                ]
                if re.match(r"\d\.\d{3}\.\d{2}", datas[4][0]):
                    gear = re.findall(r"\d\.\d{2}(\d\.\d{2})", datas[4][0])[0]
                else:
                    gear = datas[4][0]
                pdic = {
                    'bike_num': int(datas[0][0]),
                    'name': datas[1][0],
                    'hometown': datas[1][-3],
                    'age': datas[1][-2],
                    'year': int(datas[1][-1]),
                    'rank': datas[2][0],
                    'feet': datas[3][0],
                    'gear': float(gear),
                    'point': float(datas[5][0]),
                    'S': int(datas[6][0]),
                    'B': int(datas[7][0]),
                    'nige': int(datas[8][0]),
                    'makuri': int(datas[9][0]),
                    'sashi': int(datas[10][0]),
                    'mark': int(datas[11][0]),
                    'first': int(datas[12][0]),
                    'second': int(datas[13][0]),
                    'third': int(datas[14][0]),
                    'over_rank': int(datas[15][0]),
                    'win_rate': float(datas[16][0]),
                    'in_second_rate': float(datas[16][1]),
                    'in_third_rate': float(datas[16][2]),
                }
                item['player{}'.format(pdic['bike_num'])] = pdic
                players.append(pdic)
        # 3連単とオッズのイテレータ
        odds_num = response.css('li tr span.num::text').extract()
        odds = response.css('li tr span.odds::text').extract()
        # numpy array 作製
        odds_arr = np.zeros((50, 4))
        for i, num in enumerate(odds_num):
            if re.match(r"\d\-\d\-\d", num) is not None and i <= 49:
                # それぞれ代入
                first, second, third = num.split('-')
                odds_arr[i, 0] = first
                odds_arr[i, 1] = second
                odds_arr[i, 2] = third
                odds_arr[i, 3] = odds[i]

            else:
                break

        odds_table = pd.DataFrame(odds_arr)
        odds_table.columns = ['first', 'second', 'third', 'odds']
        odds_table = odds_table.astype(
            {'first': int, 'second': int, 'third': int}
        )
        item['odds_table'] = odds_table

        # 結果
        order = response.css('.result_table td.num span::text').extract()
        item['order'] = tuple([int(num) for num in order])

        yield item
