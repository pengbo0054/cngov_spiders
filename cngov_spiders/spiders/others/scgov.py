from scrapy.spiders import Spider
from scrapy.selector import Selector

from cngov_spiders.items import Website


class DmozSpider(Spider):
    name = "scgov"
    allowed_domains = ["gov.cn"]
    urls = ["10693", "10694", "10691", "10692", "10695", "12412"]
    start_urls = ["http://www.sc.gov.cn/10462/10464/10684/%s/index.shtml"%(url) for url in urls]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        #sites = sel.xpath('//span')
        sites = sel.xpath('//tr')
        items = []
        for site in sites:
            item = Website()
            item['name'] = site.xpath('.//td[1]/span/a/font/text()').extract()
            if len(site.xpath('.//td[1]/span/a/@href').extract()) > 1:
                continue
            #elif not site.xpath('.//td[1]/span/a/@href').extract().startswith('http'):
            #    item['url'] = 'http://www.sc.gov.cn' + site.xpath('.//td[1]/span/a/@href').extract()
            else:
                item['url'] = site.xpath('.//td[1]/span/a/@href').extract()
            item['timestamp'] = site.xpath('.//td[2]/text()').extract()
            items.append(item)
        return items
