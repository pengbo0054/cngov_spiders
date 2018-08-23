
FROM python:3.5
RUN apt-get update
RUN pip install scrapy bs4 textrank4zh
RUN git clone https://github.com/pengbo0054/cngov_spiders.git
