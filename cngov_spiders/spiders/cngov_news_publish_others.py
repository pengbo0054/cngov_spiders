from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from cngov_spiders.items import Website
from cngov_spiders.settings import MODE
from urllib import request
from bs4 import BeautifulSoup
from textrank4zh import TextRank4Keyword, TextRank4Sentence
from datetime import datetime

import re


class GovSpider(Spider):
    name = "cngov_news_publish_others"
    allowed_domains = ["gov.cn"]

    url = "http://sousuo.gov.cn/column/30619/0.htm"
    bs = BeautifulSoup(request.urlopen(url), features="lxml")
    page = int(re.sub('\D', '', bs.find_all('form', id='toPage')[0].li.text))
    if MODE == 'latest':
        start_urls = ["http://sousuo.gov.cn/column/30474/%s.htm"% (i) for i in range(2)]
    else:
        start_urls = ["http://sousuo.gov.cn/column/30619/%s.htm"% (i) for i in range(page)]

    def parse(self, response):
        sel = Selector(response)
        # sites = sel.xpath('/html/body/div/div/div[1]/div')
        sites = sel.xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li')
        for site in sites:
            item = Website()
            item['title'] = site.xpath('.//h4/a/text()').extract()
            item['url'] = site.xpath('.//h4/a/@href')[0].extract()
            item['author'] = [datetime.strptime(site.xpath('.//h4/span/text()').extract()[0][:-1], '%Y.%m.%d')]
            item['belong'] = ['新闻']
            item['sub_belong'] = ['新闻发布']
            item['classes'] = ['其他']

            yield Request(url=item['url'], meta={'item': item}, callback=self.parse_body, dont_filter=True)

    def parse_body(self, response):
        item = response.meta['item']
        contents = response.xpath('//*[@id="UCAP-CONTENT"]/p/text()').extract()

        item['text'] = contents

        def nlp(contents):
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=''.join(i for i in contents), lower=True, window=2)

            tr4s = TextRank4Sentence()
            tr4s.analyze(text=''.join(i for i in contents), lower=True, source='all_filters')

            keyword = [item for item in tr4w.get_keywords(20, word_min_len=1)]
            keyphase = [item for item in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2)]
            keysentence = [item for item in tr4s.get_key_sentences(num=3)]
            return keyword, keyphase, keysentence

        item['keyword'], item['keyphase'], item['keysentence'] = nlp(item['text'])

        yield item
