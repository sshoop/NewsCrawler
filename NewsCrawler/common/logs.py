import logging
import time
import os

"""
公共日志类
"""


class Logger(object):
    def __init__(self, name, level=logging.INFO,):
        self.logger = logging.getLogger(name)
        self.level = level
        # 设置log级别
        self.logger.setLevel(level=self.level)
        # 日志文件路径(绝对路径，scrapy路径问题）
        self.path ='/home/sshoop/NewsCrawler/NewsCrawler/logs/'
        # 初始化
        self.init()

    def init(self,):
        """
        初始化logger
        :return:
        """
        # 设置输出文件, 文件名为当天的时间
        file_name = time.strftime('%Y-%m-%d') + '.txt'
        file_path = self.path + file_name
        # print(file_path)
        if not os.path.exists(file_path):
            # 创建新的文件
            with open(file_path, 'a'):
                pass
        # file handler
        # 解决日志重复输出的问题
        '''
        问题原因：调用logging.getLogger(name)时，name相同则返回的是同一个logger，
                 因此会出现重复添加handler的情况。
        解决办法：
                 1：每次赋不同的name;
                 2：if not len(logger.handlers):
                           add handler;
                 3：logger.handlers.pop()   //每次移除一个
                 4：logger.handlers = []    //直接将其赋空
        这里采用第四种方法，考虑到输出文件名可能会有变化
        '''
        self.logger.handlers = []
        handler = logging.FileHandler(file_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # print(self.logger.handlers)

    # def write_log(self, level, message):
    #     """
    #     向指定的handler输出一条日志
    #     :param level: 日志级别
    #     :param message: 日志信息
    #     :return:
    #     """
    #
    #     if level == logging.DEBUG:
    #         self.logger.debug(message)
    #     elif level == logging.INFO:
    #         self.logger.info(message)
    #     elif level == logging.WARNING:
    #         self.logger.warning(message)
    #     elif level == logging.ERROR:
    #         self.logger.error(message)
    #     else:
    #         self.logger.critical(message)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    # for _ in range(5):
    #     logger = Logger('test')
    #     logger.info('test')

    tags = ['news_tech', 'news_finance',
            'news_game', 'news_military',
            'news_history', 'news_car',
            'news_travel', 'news_baby']
    print(len(tags))



