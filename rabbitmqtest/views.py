# coding: utf-8
import thread
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from rabbitmqtest.rabbitmq import RabbitMQInfo
from rabbitmqtest.rabbitmq import Message
from rabbitmqtest.forms import SendForm, Consumer
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
        if len(request.POST) == 5:
            c_form = Consumer()
            s_form = SendForm(request.POST)  # form 包含提交的数据

            if s_form.is_valid():  # 如果提交的数据合法
                exchange = s_form.cleaned_data['exchange']
                mode = s_form.cleaned_data['mode']
                route = s_form.cleaned_data['route']
                payload = s_form.cleaned_data['payload']
                Message().send(exchange, route, payload)
        else:
            s_form = SendForm()
            c_form = Consumer(request.POST)
            if c_form.is_valid():
                exchange = c_form.cleaned_data['exchange']
                route = c_form.cleaned_data['route'].strip().strip(',').split(',')

                thread.start_new_thread(Message().add_custome, (exchange, route))

    else:  # 当正常访问时
        c_form = Consumer()
        s_form = SendForm()
    return render_to_response('test.html', locals(),
                              context_instance=RequestContext(request))


def ajax(request):
    value = get_message()
    return HttpResponse(value)
