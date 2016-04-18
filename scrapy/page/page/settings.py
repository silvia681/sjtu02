# Scrapy settings for baidu project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'page'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['page.spiders']
NEWSPIDER_MODULE = 'page.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = {'page.FilePipelines.PagePipeline':200}
LOG_ENABLED = False
#LOG_LEVEL = 'ERROR'
CONCURRENT_REQUESTS = 300
COOKIES_ENABLED = False
RETRY_ENABLED = False
REDIRECT_ENABLED = False
DOWNLOAD_HANDLERS = {'s3': None}