# coding: utf-8
import commands
import re
import requests  # http请求

import pika  # pika是AMQP协议的Python客户端开发包。

global ALL_MESSAGE
ALL_MESSAGE = ''
global PORT
PORT = ''


class RabbitMQInfo(object):
    """
    获取 rabbitmq server 信息的类
    该类通过调用 rabbigmq server 的 http APi 接口来获取该 server 的信息
    """

    def __init__(self, host='localhost', username='guest', password='guest'):
        host = host
        self.auth = (username, password)
        global PORT
        if not PORT:
            PORT = self._get_port()
        self.port = PORT
        self.url_suff = 'http://%s:%s/api' % (host, self.port)

    def _get_port(self):
        """
        获取 rabbitmq 服务占用的端口，因为 rabbimq server 的端口不固定，有可能是5672、15672、25672
        :return: port
        """
        stat, output = commands.getstatusoutput('netstat -tnlp | grep 5672 | grep 0.0.0.0:*')
        if not stat:
            pattern = re.compile(r':(\d{5})\s')
            ports = pattern.findall(output)
        else:
            raise
        # 这里通过正则获取的port有可能有多个，循环每个port，分别进行请求验证，找出正确的
        for port in ports:
            url = '%s/%s' % ('http://localhost:%s/api' % port, 'overview')
            # 请求该url，如果返回状态码是200,则成功
            try:
                r = requests.get(url, auth=self.auth, timeout=1)
            except requests.exceptions.ReadTimeout:
                continue
            if r.status_code == 200:
                return port

    def overview(self):
        """
        概览，请求url是 /overview
        :return:
        """
        url = '%s/%s' % (self.url_suff, 'overview')
        r = requests.get(url, auth=self.auth)
        return str2list(r.content)

    def channels(self):
        """
        channels列表，请求url是 /channels
        :return:
        """
        url = '%s/%s' % (self.url_suff, 'channels')
        r = requests.get(url, auth=self.auth)
        return str2list(r.content)

    def exchanges(self):
        """
        exchanges列表，请求url是 /exchanges
        :return:
        """
        url = '%s/%s' % (self.url_suff, 'exchanges')
        r = requests.get(url, auth=self.auth)
        return str2list(r.content)

    def queues(self):
        """
        queues列表，请求url是 /queues
        :return:
        """
        url = '%s/%s' % (self.url_suff, 'queues')
        r = requests.get(url, auth=self.auth)
        return str2list(r.content)

    def get_exchanges(self):
        """
        在取exchanges的时候，我们只需要exchanges的name属性，循环获取到的exanges列表中每一个的name，
        组成一个元组(name,name)
        :return:
        """
        exchanges = []
        for exchange in self.exchanges():
            name = exchange.get('name')
            if name:
                exchanges.append((name, name))
        return exchanges


class Message(object):
    """
    操作消息的类
    """

    def __init__(self, host='localhost'):
        """
        初始化一个连接和channel
        :param host:
        """
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host))
        self.channel = self.connection.channel()

    def __del__(self):
        """
        当类销毁时关闭连接
        :return:
        """
        self.connection.close()

    def create_exchange(self, name='hello', type='direct'):
        """
        创建一个exchange
        :param name: exchange的name
        :param type: exchange的类型
        :return:
        """
        self.channel.exchange_declare(exchange=name, type=type)

    def send(self, exchange, route, message):
        """
        发送一条消息到对应的exchange
        :param exchange:
        :param route:
        :param message:
        :return:
        """
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=route,
                                   body=message)

    def add_custome(self, exchange=None, route=None):
        """
        添加一个消费者，消费消息
        :param exchange:
        :param route:
        :return:
        """
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        for r in route:
            self.channel.queue_bind(exchange=exchange,
                                    queue=queue_name,
                                    routing_key=r)
        self.channel.basic_consume(callback,
                                   queue=queue_name,
                                   no_ack=True)
        self.channel.start_consuming()


def callback(ch, method, properties, body):
    """
    回调函数
    在 add_custome()中使用了改回调函数，
    当消费者受到一个消息，就会调用该方法，
    该方法又将消费者受到的消息进行处理然后赋值给全局变量 ALL_MESSAGE
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    body = 'exchange(%s),consumer_tag(%s): <em>%s</em><br/>' % (
        method.exchange, method.consumer_tag, body)
    global ALL_MESSAGE
    ALL_MESSAGE = ALL_MESSAGE + body


def str2list(s):
    """
    通过http请求得到的结果是类似 '["a":"b","c":"d"]'的字符串
    将其中的false、true转换成False、True，python的bool值
    eval()将改字符串转换为python的数据类型，可以直接当作list来使用
    :param s:
    :return:
    """
    return eval(s.replace('false', 'False').replace('true', 'True'))


def get_message():
    global ALL_MESSAGE
    return ALL_MESSAGE
