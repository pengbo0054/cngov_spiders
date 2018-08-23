from scrapy.spiders import Spider
from scrapy.selector import Selector

from cngov_spiders.items import Website


class GovSpider(Spider):
    name = "cngov_frame"
    allowed_domains = ["gov.cn"]
    start_urls = ["http://www.gov.cn/2016public/bottom.htm"]

    def parse(self, response):

        sel = Selector(response)
        sites = sel.xpath('/html/body/div/div/div[1]/div')
        items = []
        for site in sites:            
            for i in site.xpath('.//ul/li'):
                if len(i.xpath('.//a/text()').extract()) > 1:
                    for j in i.xpath('.//a'):
                        item = Website()
                        item['belong'] = site.xpath('.//p/text()').extract()
                        item['name'] = j.xpath('text()').extract()
                        if not j.xpath('@href').extract()[0].startswith('http'):
                            item['url'] = ['http://www.gov.cn' + j.xpath('@href').extract()[0]]
                        else:
                            item['url'] = j.xpath('@href').extract()
                        items.append(item)
                else:
                    item = Website()
                    item['belong'] = site.xpath('.//p/text()').extract()
                    item['classes'] = ['frame']
                    item['name'] = i.xpath('.//a/text()').extract()
                    if not i.xpath('.//a/@href').extract()[0].startswith('http'):
                        item['url'] = ['http://www.gov.cn' + i.xpath('.//a/@href').extract()[0]]
                    else:
                        item['url'] = i.xpath('.//a/@href').extract()
                    items.append(item)

        return items
