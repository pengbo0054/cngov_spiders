from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from cngov_spiders.items import Website
from urllib import request
from bs4 import BeautifulSoup
from textrank4zh import TextRank4Keyword, TextRank4Sentence

import re


class GovSpider(Spider):
    name = "cngov_policy_filelib"
    allowed_domains = ["gov.cn"]

    url = "http://new.sousuo.gov.cn/list.htm?sort=pubtime&advance=true&t=paper&n=100"
    bs = BeautifulSoup(request.urlopen(url), features="lxml")
    page = int(re.sub('\D', ' ', bs.find_all('span', attrs={'class': ['jilu']})[0].text).split()[0])

    start_urls = ["http://sousuo.gov.cn/list.htm?q=&n=100&p=%s&t=paper&sort=pubtime&childtype=&subchildtype=&pcodeJiguan=&pcodeYear=&pcodeNum=&location=&searchfield=&title=&content=&pcode=&puborg=&timetype=timeqb&mintime=&maxtime="%(i) for i in range(page)]
    #start_urls = ["http://sousuo.gov.cn/list.htm?q=&n=10&p=0&t=paper&sort=pubtime&childtype=&subchildtype=&pcodeJiguan=&pcodeYear=&pcodeNum=&location=&searchfield=&title=&content=&pcode=&puborg=&timetype=timeqb&mintime=&maxtime="]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('/html/body/div[2]/table//tr')
        print('sites length: ', len(sites))
        for site in sites[1:]:
            item = Website()
            item['name'] = site.xpath('.//td[2]/a/text()').extract()
            item['url'] = site.xpath('.//td[2]/a/@href')[0].extract()
            if len(site.xpath('.//td[4]/text()').extract()) > 0:
                item['timestamp'] = '.'.join(re.sub('\D', ' ', site.xpath('.//td[4]/text()').extract()[0]).split())
            else:
                continue
            item['belong'] = ['政策']
            item['sub_belong'] = ['文件库']
            item['classes'] = site.xpath('.//td[2]/ul/li[3]/text()').extract()

            yield Request(url=item['url'], meta={'item': item}, callback=self.parse_body, dont_filter=True)

    def parse_body(self, response):
        item = response.meta['item']
        contents = response.xpath('//*[@id="UCAP-CONTENT"]/p/text()').extract()

        item['body'] = contents

        def nlp(contents):
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=''.join(i for i in contents), lower=True, window=2)

            tr4s = TextRank4Sentence()
            tr4s.analyze(text=''.join(i for i in contents), lower=True, source='all_filters')

            keyword = [item for item in tr4w.get_keywords(20, word_min_len=1)]
            keyphase = [item for item in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2)]
            keysentence = [item for item in tr4s.get_key_sentences(num=3)]
            return keyword, keyphase, keysentence

        item['keyword'], item['keyphase'], item['keysentence'] = nlp(item['body'])

        yield item
