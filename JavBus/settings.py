# -*- coding: utf-8 -*-

# Scrapy settings for JavBus project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#     中文的 https://www.jianshu.com/p/df9c0d1e9087

# Scrapy项目的名字,这将用来构造默认 User-Agent,同时也用来log,
# 当您使用 startproject 命令创建项目时其也被自动赋值。
BOT_NAME = 'JavBus'
# Scrapy搜索spider的模块列表 默认: [xxx.spiders]
SPIDER_MODULES = ['JavBus.spiders']
# 使用 genspider 命令创建新spider的模块。默认: 'xxx.spiders'
NEWSPIDER_MODULE = 'JavBus.spiders'


# 爬取的默认User-Agent，除非被覆盖
# USER_AGENT = 'demo1 (+http://www.yourdomain.com)'


# Scrapy downloader 并发请求(concurrent requests)的最大值,默认: 16
# CONCURRENT_REQUESTS = 32

# 为同一网站的请求配置延迟（默认值：0）
# 下载器在下载同一个网站下一个页面前需要等待的时间,
# 该选项可以用来限制爬取速度,减轻服务器压力。同时也支持小数:0.25 以秒为单位
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3


# 下载延迟设置只有一个有效
# 对单个网站进行并发请求的最大值。
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 对单个IP进行并发请求的最大值。如果非0,则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定,
# 使用该设定。也就是说,并发限制将针对IP,而不是网站。该设定也影响 DOWNLOAD_DELAY:
# 如果 CONCURRENT_REQUESTS_PER_IP 非0,下载延迟应用在IP而不是网站上。
# CONCURRENT_REQUESTS_PER_IP = 16

# 禁用Cookie（默认情况下启用）
# COOKIES_ENABLED = False

# 禁用Telnet控制台（默认启用）
# TELNETCONSOLE_ENABLED = False

# 覆盖默认请求标头：
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# 启用或禁用蜘蛛中间件
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'demo1.middlewares.Demo1SpiderMiddleware': 543,
# }


# 启用或禁用扩展程序
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }


# 启用和配置AutoThrottle扩展（默认情况下禁用）
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True

# 初始下载延迟
# AUTOTHROTTLE_START_DELAY = 5


# 在高延迟的情况下设置的最大下载延迟
# AUTOTHROTTLE_MAX_DELAY = 60


# Scrapy请求的平均数量应该并行发送每个远程服务器
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0


# 启用显示所收到的每个响应的调节统计信息：
# AUTOTHROTTLE_DEBUG = False

# 启用和配置HTTP缓存（默认情况下禁用）
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# ############基础设置############

# 如果启用,Scrapy将会采用 robots.txt策略
ROBOTSTXT_OBEY = False
# 下载器中间件
DOWNLOADER_MIDDLEWARES = {
    # 'JavBus.middlewares.JavbusDownloaderMiddleware': 543,
    # 调用的随机Agent中间件
    'JavBus.middlewares.UserAgentmiddleware': 400
}
# 数据输出管道
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'JavBus.pipelines.JsonPipeline': 300
    # 将清除的项目在redis进行处理
    'JavBus.pipelines.MysqlPipeline': 300
    # 'JavBus.pipelines.MongoPipeline': 300
}


# ############日志设置############
# 日志是否启动
LOG_ENABLED = True
# 用于记录的编码。
LOG_ENCODING = 'utf-8'
# 用于记录输出的文件名。如果None，将使用标准误差。
LOG_FILE = None
# 用于格式化日志消息的字符串。
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# 用于格式化日期/时间的字符串
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
# 记录的最低级别。可用级别为：CRITICAL，ERROR，WARNING，INFO，DEBUG。
LOG_LEVEL = 'DEBUG'
# 如果True，您的进程的所有标准输出（和错误）将被重定向到日志
LOG_STDOUT = False
# 如果True，日志将仅包含根路径。如果设置为，False 则它显示负责日志输出的组件
LOG_SHORT_NAMES = False


# ###########ScrapyRedis设置############
# 不清除Redis队列、这样可以暂停/恢复 爬取
# SCHEDULER_PERSIST = False
# 启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = 'redis://127.0.0.1:6379'
# REDIS_HOST = '127.0.0.1'  # 也可以根据情况改成 localhost
# REDIS_PORT = 6379


# ############数据导出设置############
# 数据保存到MONGODB
# 主机IP
FEED_EXPORT_ENCODING = 'utf-8'
MONGO_HOST = "10.0.0.4"
# 端口号
MONGO_PORT = 27017
# 库名
MONGO_DB = "JavBus"
# collection名
MONGO_COLL_MOVIE = "movie"
MONGO_COLL_STAR = "star"
MONGO_COLL_MAGNET = "magnet"
MONGO_COLL_PREVIEW = "preview"
MONGO_COLL_MOVIE_STAR = "movie_star"
MONGO_COLL_STUDIO = "studio"
MONGO_COLL_LABEL = "label"
MONGO_COLL_DIRECTOR = "director"
MONGO_COLL_SERIES = "series"
MONGO_COLL_MOVIE_STUDIO = "movie_studio"
MONGO_COLL_MOVIE_LABEL = "movie_label"
MONGO_COLL_MOVIE_DIRECTOR = "movie_director"
MONGO_COLL_MOVIE_SERIES = "movie_series"
MONGO_COLL_TAG = "tag"
MONGO_COLL_MOVIE_TAG = "movie_tag"
# MONGO_USER = "zhangsan"
# MONGO_PSW = "123456"


# MYSQL 配置
MYSQL_HOST = "10.0.0.4"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_PORT = 3306
MYSQL_DB = "javbus"

# ############数据导出设置############
