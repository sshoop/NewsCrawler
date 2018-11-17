import execjs
import json
import re
"""
公共工具包
"""


def get_token():
    """
    获取头条url中的各种token
    :return: as, cp, _signature
    """
    with open(r"/Users/song/Projects/TextClassification/NewsCrawler/NewsCrawler/common/generate_signature.js", "r") as js_file:
        lines = js_file.readlines()
        js_code = ""
        for line in lines:
            js_code += line
        context = execjs.compile(js_code)
        # the type of token is a str of json
        token = context.call('get_as_cp_signature')
        # print(token)
        # str to dict
        token_dict = json.loads(token)

        return token_dict['as'], token_dict['cp'], token_dict['_signature']


def exchange_url(url):
    """
    转换头条url, 将普通url转换为能直接返回文章信息json串的特殊url
    eg：
    http://toutiao.com/group/6618154263824581133/
    https://m.toutiao.com/i6618154263824581133/info/?_signature=KdRV3BAYcgqDk.2J4JL58CnUVc&i=66618154263824581133
    :param url:
    :return:
    """
    # 判断是否为头条问答
    item_list = re.split(r'[/|.]', url)
    if 'wukong' in item_list:
        return None
    item_list = url.split('/')
    i = item_list[4]
    AS, CP, _signature = get_token()
    url = 'https://m.toutiao.com/i' + i + '/info/?_signature=' + _signature + '&i=' + i
    return url


if __name__ == '__main__':
    # pass
    url = 'http://toutiao.com/group/6618154263824581133/'
    print(exchange_url(url))
    f = open(r'generate_signature.js', 'r')
    print(f.readline())


