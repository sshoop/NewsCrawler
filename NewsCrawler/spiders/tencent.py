import scrapy
import json
from NewsCrawler.items import NewItem


class ToutiaoSpider(scrapy.Spider):
    name = 'tencent'

    _BASE_URL = 'https://pacaio.match.qq.com/irs/rcd?'
    _MAX_PAGES = 100
    _PARAM = {
        '1': {
            'cid': '146',
            'ext': 'finance',
            'token': '49cbb2154853ef1a74ff4e53723372ce',
        },
        '2': {
            'cid': '135',
            'ext': 'milite_pc',
            'token': 'c232b098ee7611faeffc46409e836360',
        },
        '3': {
            'cid': '146',
            'ext': 'ent',
            'token': '49cbb2154853ef1a74ff4e53723372ce',
        },
        '4': {
            'cid': '146',
            'ext': 'auto',
            'token': '49cbb2154853ef1a74ff4e53723372ce',
        },
        '5': {
            'cid': '146',
            'ext': 'visit',
            'token': '49cbb2154853ef1a74ff4e53723372ce',
        },
        '6': {
            'cid': '146',
            'ext': 'baby',
            'token': '49cbb2154853ef1a74ff4e53723372ce',
        },
        '7': {
            'cid': '146',
            'ext': 'games',
            'token': '49cbb2154853ef1a74ff4e53723372ce',
        },
        '8': {
            'cid': '146',
            'ext': 'history',
            'token': '49cbb2154853ef1a74ff4e53723372ce',
        },
        '9': {
            'cid': '146',
            'ext': 'tech',
            'token': '49cbb2154853ef1a74ff4e53723372ce',
        },
        '10': {
            'cid': '146',
            'ext': 'sports',
            'token': '49cbb2154853ef1a74ff4e53723372ce',
        },
    }
    _INDEX = 0

    def start_requests(self):
        # headers = {
        #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        # }
        while True:
            if self._INDEX == len(self._PARAM):
                self._INDEX = 0
            self._INDEX += 1
            value = self._PARAM[str(self._INDEX)]
            # self.logger.info('\n\n\n\n\n\n\n\n')
            # self.logger.info(value['ext'])
            # for k, v in self._PARAM.items():
            #     print(k, v)
            # break
            for page in range(self._MAX_PAGES):
                yield scrapy.FormRequest(
                    url=self._BASE_URL,
                    formdata={
                        'cid': value['cid'],
                        'token': '49cbb2154853ef1a74ff4e53723372ce',
                        'ext': value['ext'],
                        'page': str(page + 1),
                        # 'expIds': '',
                        # 'callback': '__jp13',
                    },
                    meta={
                        'label': value['ext'],
                    },
                    callback=self.get_urls,
                )

    def get_urls(self, response):
        self.logger.info(response.text)
        try:
            data = json.loads(response.text)
        except:
            data = json.loads(response.text[response.text.find('(') + 1:response.text.rfind(')')])

        data = data['data']

        # self.logger.info(type(data))
        # data 为空表示该类别数据已经爬取完
        if data:
            for new in data:
                # self.logger.info(new)
                # 文字新闻
                if new['article_type'] == 0:
                    # 新闻的元数据
                    # self.logger.info(new)
                    meta = dict()
                    meta['title'] = new['title']
                    meta['source'] = new['source']
                    meta['time'] = new['ts']
                    meta['url'] = new['vurl']
                    meta['label'] = response.meta['label']
                    yield scrapy.Request(url=meta['url'], meta=meta, callback=self.parse)

    def parse(self, response):
        # self.logger.info(response.text)
        results = response.selector.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/p')
        # self.logger.info('\n\n\n\n')
        # self.logger.info(results)
        # self.logger.info(type(results))
        # for result in results:
        #     self.logger.info(result.xpath('./text()').extract())
        texts = [result.xpath('./text()').extract() for result in results]
        content = ''
        for text in texts:
            if text:
                content += text[0]
        # self.logger.info(content)

        item = NewItem()
        item['title'] = response.meta['title']
        item['source'] = response.meta['source']
        item['time'] = response.meta['time']
        item['url'] = response.meta['url']
        item['content'] = content
        item['web'] = 'tencent'
        item['label'] = response.meta['label']

        return item
