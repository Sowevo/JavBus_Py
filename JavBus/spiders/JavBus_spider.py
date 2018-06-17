import scrapy
import time

from scrapy_redis.spiders import RedisSpider

from JavBus.items import MainItem


class JavBusMainSpider(RedisSpider):
    base_url = 'https://www.javbus.com'
    name = 'JavBusMain'
    allowed_domains = ["www.javbus.com"]
    start_urls = [
        "https://www.javbus.com/"
    ]
    redis_key = 'JavBusMain:start_urls'

    def parse(self, r):
        if len(r.css('.bigImage img')) > 0:
            title = cover = censored = censored = code = release_date = duration = director = maker =\
                publisher = series = tags = stars = previews = gid = uc = None
            title = r.css('.col-md-9.screencap  img::attr(title)').extract_first()
            cover = r.css('.col-md-9.screencap  img::attr(src)').extract_first()
            censored = r.css('li.active > a::text').extract_first()
            tags = r.css('.genre  a[href*="genre"]::text').extract()
            stars = r.css('span[onmouseover] a::text').extract()
            previews = r.css('a.sample-box::attr(href)').extract()
            script = r.xpath('//script')[8].extract()
            for line in script.split('\n'):
                if 'gid' in line:
                    gid = line.split('=')[-1].strip()[:-1]
                elif 'uc' in line:
                    uc = line.split('=')[-1].strip()[:-1]
            magnets_url = 'https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid='+gid+'&uc='+uc+'&lang=en'
            for info in r.css('.info p'):
                header = info.css('.header::text').extract_first()
                if header:
                    data = info.xpath('string(.)').extract_first().replace(header, "").strip()

                if header == '識別碼:':
                    code = data
                elif header == '發行日期:':
                    release_date = data
                elif header == '長度:':
                    duration = data
                elif header == '導演:':
                    director = data
                elif header == '製作商:':
                    maker = data
                elif header == '發行商:':
                    publisher = data
                elif header == '系列:':
                    series = data
                elif header == '類別:' or header == '演員':
                    pass
                elif header is None:
                    pass
                else:
                    print("存在未知字段!!!"+header)
            item = MainItem()
            item['code'] = code
            item['title'] = title
            item['censored'] = censored
            item['stars'] = stars
            item['release_date'] = release_date
            item['duration'] = duration
            item['director'] = director
            item['maker'] = maker
            item['publisher'] = publisher
            item['tags'] = tags
            item['cover'] = cover
            item['previews'] = previews
            item['series'] = series
            item['magnets'] = None
            item['release_date'] = release_date
            item['update_time'] = time.time()
            # 将参数代入到第二个解析方法中
            yield scrapy.Request(magnets_url, meta={'item': item}, callback=self.parse_magnets)
        for url in r.xpath('//a/@href').extract():
            if '/en' not in url and '/ja' not in url and '/ko' not in url and 'http' in url:
                yield scrapy.Request(url, callback=self.parse)
                pass

    def parse_magnets(self, r):
        item = r.meta['item']
        magnets = []
        for line in r.css('tr'):
            magnet = {}
            infos = line.css('a')
            if len(infos) == 4:
                magnet['magnet_url'] = infos[0].css('::attr(href)').extract_first().strip()
                magnet['magnet_name'] = infos[0].xpath('string(.)').extract_first().strip()
                magnet['is_HD'] = infos[1].xpath('string(.)').extract_first().strip()
                magnet['magnet_size'] = infos[2].xpath('string(.)').extract_first().strip()
                magnet['magnet_date'] = infos[3].xpath('string(.)').extract_first().strip()
            elif len(infos) == 3:
                magnet['magnet_url'] = infos[0].css('::attr(href)').extract_first().strip()
                magnet['magnet_name'] = infos[0].xpath('string(.)').extract_first().strip()
                magnet['is_HD'] = 'NO_HD'
                magnet['magnet_size'] = infos[1].xpath('string(.)').extract_first().strip()
                magnet['magnet_date'] = infos[2].xpath('string(.)').extract_first().strip()
            magnets.append(magnet)
        item['magnets'] = magnets
        yield item



