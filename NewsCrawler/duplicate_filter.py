from scrapy.dupefilter import RFPDupeFilter

"""
弃用！！！！！！ url转换过于麻烦，不如直接在mongodb中查询是否重复
定义去重类
虽然scrapy默认基于sha1(method + url + body + header)进行去重，
但我们每次请求的url都不同(signature），因此自定义一个去重
https://m.toutiao.com/i6618154263824581133/info/?_signature=KdRV3BAYcgqDk.2J4JL58CnUVc&i=66618154263824581133
"""


class SeenURLFilter(RFPDupeFilter):
    def __init__(self, path=None):
        self.urls_seen = set()
        RFPDupeFilter.__init__(self, path)

    def request_seen(self, request):
        # 用于获取新闻json串的url(即转换后的url)
        down_url = request.url
        # 转换为初始url
        # url =
        if request.url in self.urls_seen:
            return True
        else:
            self.urls_seen.add(request.url)
