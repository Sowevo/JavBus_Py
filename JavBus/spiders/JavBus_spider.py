import scrapy
import time

from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from JavBus.items import MainItem, StarItem


class JavBusSpider(RedisCrawlSpider):
    # 网站的主页
    domain = 'www.javbus.com'
    name = 'JavBus'
    allowed_domains = [domain]
    start_urls = [
        'https://'+domain+'/actresses'
    ]
    rules = (
        # 演员详情页
        Rule(LinkExtractor(allow=(r'https://'+domain+'/(uncensored/)?star/\w+$'),deny=(r'/en/?|/ko/?|/ja/?|/uncensored|/genre|/actresses')), callback="parse_star", follow=True),

        # 电影详情页
        Rule(LinkExtractor(allow=(r'https://'+domain+'/[\w-]+$'),deny=(r'/en/?|/ko/?|/ja/?|/uncensored|/genre|/actresses')), callback="parse_main", follow=True),

        # 其他页面 r"https://www.javbus.com/actresses|https://www.javbus.com/uncensored/actresses"
        Rule(LinkExtractor(allow=(r'^((?!/en/|/ko/|/ja/).)*$'))),
    )
    redis_key = 'JavBus:start_urls'

    def parse_star(self, r):
        # print('演员详情页' + r.url)
        name = birthday = height = cup = bust = waist = hips = hometown = hobby = avatar = None
        name = r.css('.avatar-box img::attr(title)').extract_first()
        avatar = r.css('.avatar-box img::attr(src)').extract_first()
        code = r.url.split('/')[-1]
        for info in r.css('.photo-info p'):
            line = info.xpath('string(.)').extract_first()
            key = line.split(':')[0].strip()
            value = line.split(':')[-1].strip()
            if key == '生日':
                birthday = value
            elif key == '年齡':
                pass
            elif key == '身高':
                height = value
            elif key == '罩杯':
                cup = value
            elif key == '胸圍':
                bust = value
            elif key == '腰圍':
                waist = value
            elif key == '臀圍':
                hips = value
            elif key == '出生地':
                hometown = value
            elif key == '愛好':
                hobby = value
            else:
                print('未知字段!!!!!!!!!!')
        item = StarItem()
        item['code'] = code
        item['name'] = name
        item['birthday'] = birthday
        item['height'] = height
        item['cup'] = cup
        item['bust'] = bust
        item['waist'] = waist
        item['hips'] = hips
        item['hometown'] = hometown
        item['hobby'] = hobby
        item['avatar'] = avatar
        yield item

    def parse_main(self, r):
        # print('电影详情页' + r.url)
        title = cover = censored = censored = code = release_date = duration = director = maker =\
            publisher = series = tags = stars = previews = gid = uc = None
        title = r.css('.col-md-9.screencap  img::attr(title)').extract_first()
        cover = r.css('.col-md-9.screencap  img::attr(src)').extract_first()
        censored = r.css('li.active > a::text').extract_first()
        tags = r.css('.genre  a[href*="genre"]::text').extract()
        stars = []
        # stars = r.css('span[onmouseover] a::text').extract()
        for x in r.css('span[onmouseover] a'):
            star = {}
            star['name'] = x.xpath('string(.)').extract_first()
            star['code'] = x.xpath('.//@href').extract_first().split('/')[-1]
            stars.append(star)
        previews = r.css('a.sample-box::attr(href)').extract()
        script = r.xpath('//script')[8].extract()
        for line in script.split('\n'):
            if 'gid' in line:
                gid = line.split('=')[-1].strip()[:-1]
            elif 'uc' in line:
                uc = line.split('=')[-1].strip()[:-1]
        magnets_url = 'https://'+self.domain+'/ajax/uncledatoolsbyajax.php?gid='+gid+'&uc='+uc+'&lang=en'
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

    def parse_magnets(self, r):
        item = r.meta['item']
        magnets = []
        for line in r.css('tr'):
            magnet = {}
            infos = line.css('a')
            if len(infos) == 5:
                magnet['magnet_url'] = infos[0].css('::attr(href)').extract_first().strip()[:60]
                magnet['magnet_name'] = infos[0].xpath('string(.)').extract_first().strip()
                magnet['HD'] = infos[1].xpath('string(.)').extract_first().strip() == 'HD'
                magnet['SUB'] = infos[2].xpath('string(.)').extract_first().strip() == 'SUB'
                magnet['magnet_size'] = infos[3].xpath('string(.)').extract_first().strip()
                magnet['magnet_date'] = infos[4].xpath('string(.)').extract_first().strip()
            elif len(infos) == 4:
                # 过滤magnet_url多余的后缀
                magnet['magnet_url'] = infos[0].css('::attr(href)').extract_first().strip()[:60]
                magnet['magnet_name'] = infos[0].xpath('string(.)').extract_first().strip()
                magnet['HD'] = infos[1].xpath('string(.)').extract_first().strip() == 'HD'
                magnet['SUB'] = infos[1].xpath('string(.)').extract_first().strip() == 'SUB'
                magnet['magnet_size'] = infos[2].xpath('string(.)').extract_first().strip()
                magnet['magnet_date'] = infos[3].xpath('string(.)').extract_first().strip()
            elif len(infos) == 3:
                # 过滤magnet_url多余的后缀
                magnet['magnet_url'] = infos[0].css('::attr(href)').extract_first().strip()[:60]
                magnet['magnet_name'] = infos[0].xpath('string(.)').extract_first().strip()
                magnet['HD'] = False
                magnet['SUB'] = False
                magnet['magnet_size'] = infos[1].xpath('string(.)').extract_first().strip()
                magnet['magnet_date'] = infos[2].xpath('string(.)').extract_first().strip()
            magnets.append(magnet)
        item['magnets'] = magnets
        yield item



