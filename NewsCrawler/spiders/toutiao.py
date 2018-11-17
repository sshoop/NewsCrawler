import scrapy
import json
import re
import time
from NewsCrawler.common.tools import exchange_url
from NewsCrawler.items import NewItem


class ToutiaoSpider(scrapy.Spider):
    name = "toutiao"
    allowed_domains = ["toutiao.com", 'snssdk.com']
    tags = ['news_tech', 'news_finance',
            'news_game', 'news_military',
            'news_history', 'news_car',
            'news_travel', 'news_baby']
    last_time = '0'
    now_time = '0'
    tag_index = 0
    num = 0
    _MAX_NUM = 1000

    def start_requests(self):
        """
        生成单个文章的url
        :return:
        """

        while True:
            # 确保每一个子标签循环_MAX_NUM次
            if self.num == self._MAX_NUM:
                self.num = 0
                self.tag_index += 1
            else:
                self.num += 1
            if self.tag_index == len(self.tags):
                self.tag_index = 0

            # 构造初始url
            self.now_time = str(int(time.time()))
            url = 'http://is.snssdk.com/api/news/feed/v51/?category=' + self.tags[
                self.tag_index] + '&refer=1&count=20&min_behot_time=' \
                + self.now_time + '&last_refresh_sub_entrance_interval=' + self.last_time + '&loc_mode=&loc_time=1491981000&latitude=&longitude=&city=&tt_from=pull&lac=&cid=&cp=&iid=0123456789&device_id=12345678952&ac=wifi&channel=&aid=&app_name=&version_code=&version_name=&device_platform=&ab_version=&ab_client=&ab_group=&ab_feature=&abflag=3&ssmix=a&device_type=&device_brand=&language=zh&os_api=&os_version=&openudid=1b8d5bf69dc4a561&manifest_version_code=&resolution=&dpi=&update_version_code=&_rticket='
            self.last_time = self.now_time

            yield scrapy.Request(url, callback=self.get_urls)

    def get_urls(self, response):
        """
        获取每一个新闻的url
        :param response:
        :return:
        """
        # self.logger.debug(response.text)
        try:
            json_dict = json.loads(response.text)
        except Exception as e:
            print(e)
        article_list = json_dict['data']
        for article in article_list:
            # str
            content = article['content']
            content_dict = json.loads(content)
            try:
                # 文章的原始url
                display_url = content_dict['display_url']
                # 转化后的url
                down_url = exchange_url(display_url)
                '''
                虽然向API接口传递了tag，但忍让返回多种类别的新闻
                手动获取文章的label, 并传递给parse
                '''
                label = content_dict['tag']
                # self.logger.critical(down_url)
                yield scrapy.Request(down_url, meta={'label': label}, callback=self.parse)
            except Exception as e:
                print(e)

    def parse(self, response):
        """
        解析response， 获取item
        :param response:
        :return:
        """
        # self.logger.debug(response)
        item = NewItem()
        # self.logger.info("response %s", response.text)
        try:
            json_dict = json.loads(response.text)
        except Exception as e:
            yield item
        # dict
        data = json_dict['data']

        # 提取数据
        item['title'] = data['title']
        item['source'] = data['source']
        item['time'] = data['publish_time']
        item['url'] = data['url']
        # 去除文章内容中的html标签
        content = data['content']
        content = re.sub('(<.*?>)', '', content)
        item['content'] = content
        item['web'] = 'toutiao'
        # 去除tag，直接按照label插入mongodb
        # item['tag'] = self.tags[self.tag_index]
        item['label'] = response.meta['label']
        # self.logger.info("title %s", item['title'])
        yield item
