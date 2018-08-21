import os
import time
import concurrent.futures

spider_dir = '/home/pengbo/project/cngov_spiders/cngov_spiders/spiders'
scripts = os.listdir(spider_dir)
files = [file for file in scripts if file.endswith('.py') and file.startswith('cngov')]
spiders = [spider.split('.')[0] for spider in files]


def foo(strings):
    os.system('scrapy crawl %s' % (strings))

start = time.time()
with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(foo, spiders)

end = time.time()
print('Took %.3f seconds.' % (end - start))
