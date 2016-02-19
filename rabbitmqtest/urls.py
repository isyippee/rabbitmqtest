"""rabbitmqtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'rabbitmqtest.views.index', name='index'),
    url(r'^channels$', 'rabbitmqtest.views.channels', name='channels'),
    url(r'^exchanges', 'rabbitmqtest.views.exchanges', name='exchanges'),
    url(r'^queues', 'rabbitmqtest.views.queues', name='channels'),
    url(r'^test', 'rabbitmqtest.views.test', name='test'),
    url(r'^ajax', 'rabbitmqtest.views.ajax', name='ajax'),
]
