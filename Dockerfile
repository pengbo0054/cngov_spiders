
FROM python:3.5
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN pip install scrapy bs4 textrank4zh scrapyelasticsearch
RUN git clone https://github.com/pengbo0054/cngov_spiders.git
#RUN cd /cngov_spiders/cngov_spiders/scripts && python multi-scrapy.py