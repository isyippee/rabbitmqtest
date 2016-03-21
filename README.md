# rabbitmq test

参考：[http://www.rabbitmq.com/getstarted.html](http://www.rabbitmq.com/getstarted.html)

## install

```
sudo apt-get install rabbitmq-server
sudo apt-get install python-django
sudo pip install pika
sudo pip install requests
```

打开 web 管理和 http api
```
sudo rabbitmq-plugins enable rabbitmq_management
```
或者
```
/usr/lib/rabbitmq/bin/rabbitmq-plugins enable rabbitmq_management
```

重启 rabbitmq
```
/etc/init.d/rabbitmq-server restart
```

可登陆 web 管理页面：http://127.0.0.1:15672/, guest/guest   
对应 http api 的 url：http://127.0.0.1:15672/api/

## django

1. 进入项目目录，启动 django
```
python manager.py runserver :8000
```

2. 浏览器访问 `http://127.0.0.1:8000`即可

## typical

几种典型场景，均在 Test 页面操作。

### Routing

1. 在 Define consumer 定义一个 Exchange 为 amq.direct，Routing key 为 a,b 的 consumer;
2. 在 Define consumer 定义一个 Exchange 为 amq.direct，Routing key 为 c 的 consumer;
3. 在 Publish Message 发布一个 Exchange 为 amq.direct，Routing key 为 a，Payload 为 aaaaaaaaaa 的消息;
4. 在 Publish Message 发布一个 Exchange 为 amq.direct，Routing key 为 b，Payload 为 bbbbbbbbbb 的消息;
5. 在 Publish Message 发布一个 Exchange 为 amq.direct，Routing key 为 c，Payload 为 cccccccccc 的消息;

最后可以看到输出框
```
exchange(amq.direct),consumer_tag(ctag1.f283177585bb451eb2cadd28905d20b6): aaaaaaaaaa
exchange(amq.direct),consumer_tag(ctag1.f283177585bb451eb2cadd28905d20b6): bbbbbbbbbb
exchange(amq.direct),consumer_tag(ctag1.fb2d515bb10241d3bc6ae10adb4b704b): cccccccccc
```

### Publish/Subscribe

1. 在 Define consumer 定义一个 Exchange 为 amq.fanout，Routing key 为空的 consumer;
2. 在 Publish Message 发布一个 Exchange 为 amq.fanout，Routing key 为空，Payload 为 test 的消息;

最后可以看到输出框
```
exchange(amq.fanout),consumer_tag(ctag1.8467e2ee370e4c03b4a3479c47aef458): test
```

### Topics

`＊` 可以匹配一个标识符。
`＃` 可以匹配0个或多个标识符。

1. 在 Define consumer 定义一个 Exchange 为 amq.topic，Routing key 为 *.a 的 consumer;
2. 在 Define consumer 定义一个 Exchange 为 amq.topic，Routing key 为 #.a 的 consumer;
3. 在 Publish Message 发布一个 Exchange 为 amq.topic，Routing key 为 b.a，Payload 为 topics test 的消息;
4. 在 Publish Message 发布一个 Exchange 为 amq.topic，Routing key 为 b.c.a，Payload 为 topics test 的消息;
5. 在 Publish Message 发布一个 Exchange 为 amq.topic，Routing key 为 .a，Payload 为 topics test 的消息;

最后可以看到输出框
```
exchange(amq.topic),consumer_tag(ctag1.2c23ee753bad4d1cb57b8eab7492ec04): topics test
exchange(amq.topic),consumer_tag(ctag1.471b00b196a64293afe1041f3977f57f): topics test
exchange(amq.topic),consumer_tag(ctag1.471b00b196a64293afe1041f3977f57f): topics test
exchange(amq.topic),consumer_tag(ctag1.2c23ee753bad4d1cb57b8eab7492ec04): topics test
exchange(amq.topic),consumer_tag(ctag1.471b00b196a64293afe1041f3977f57f): topics test
```
