# coding: utf8
# 定义表单
from django import forms

from rabbitmqtest.rabbitmq import RabbitMQInfo


class SendForm(forms.Form):
    exchange = forms.ChoiceField(
        choices=RabbitMQInfo().get_exchanges(),
        label='Exchange')
    mode = forms.ChoiceField(
        choices=[('persistent', 'persistent'),
                 ('non-persistent', 'non-persistent')],
        label='Delivery mode')
    route = forms.CharField(label='Routing key', required=False)
    payload = forms.CharField(widget=forms.Textarea, label='Payload')


class Consumer(forms.Form):
    exchange = forms.ChoiceField(
        choices=RabbitMQInfo().get_exchanges(),
        label='Exchange')
    route = forms.CharField(label='Routing key', required=False)
