# coding: utf-8
# 视图层（即业务逻辑层）
import thread

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from rabbitmqtest.forms import SendForm, Consumer
from rabbitmqtest.rabbitmq import Message
from rabbitmqtest.rabbitmq import RabbitMQInfo
from rabbitmqtest.rabbitmq import get_message


def index(request):
    value = RabbitMQInfo().overview()
    return render_to_response('index.html', locals())


def channels(request):
    value = RabbitMQInfo().channels()
    return render_to_response('channels.html', locals())


def exchanges(request):
    value = RabbitMQInfo().exchanges()
    return render_to_response('exchanges.html', locals())


def queues(request):
    value = RabbitMQInfo().queues()
    return render_to_response('queues.html', locals())


def test(request):
    if request.method == 'POST':  # 当提交表单时
        # 判断post的数据都多少，如果是5个，就说明是在发送消息，否则是在定义消费者
        if len(request.POST) == 5:
            c_form = Consumer()
            s_form = SendForm(request.POST)  # form 包含提交的数据

            if s_form.is_valid():  # 如果提交的数据合法
                exchange = s_form.cleaned_data['exchange']
                mode = s_form.cleaned_data['mode']
                route = s_form.cleaned_data['route']
                payload = s_form.cleaned_data['payload']
                # post的数据合法性进行验证，然后调用 Message 类的方法发送消息
                Message().send(exchange, route, payload)
        else:
            # 定义消费者
            s_form = SendForm()
            c_form = Consumer(request.POST)
            if c_form.is_valid():
                exchange = c_form.cleaned_data['exchange']
                route = c_form.cleaned_data['route'].strip().strip(',').split(',')
                # 另开一个线程来启动一个消费者来监听自己的频道
                # 以免阻塞当前的主线程，导致页面一直请求的状态
                thread.start_new_thread(Message().add_custome, (exchange, route))

    else:  # 当正常访问时，即打开test页面，并未post任何数据
        c_form = Consumer()
        s_form = SendForm()
    return render_to_response('test.html', locals(),
                              context_instance=RequestContext(request))


def ajax(request):
    """
    在 test.html 中使用了 ajax 请求，当在 test 页面加载或者点击一次都会来调用这个方法，
    并将这里获取到的 message 都显示在页面上，
    做到消息框中内容会变的效果。
    :param request:
    :return:
    """
    value = get_message()
    return HttpResponse(value)
