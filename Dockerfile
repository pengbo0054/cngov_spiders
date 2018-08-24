
FROM python:3.5
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN pip install scrapy bs4 textrank4zh scrapyelasticsearch
RUN git clone https://github.com/pengbo0054/cngov_spiders.git
# docker run -it ab8f8870c3e0 sh -c "cd /cngov_spiders/cngov_spiders/scripts && python multi-scrapy.py"