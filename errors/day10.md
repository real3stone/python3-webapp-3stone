#### 注册模块

1、在用户注册api装饰器@post('api/users')中，在一开始的数据检查时，有一行少写了一个'not',在注册时js就会报‘value:not found’错误，找了一下午，真是蠢啊

2、上1中的错误改正后，注册新用户时js会报'网络好像出问题了（HTTP 500）' 错误，但是数据库中已有该条用户信息，而且登录模块也能正常使用。待debug？？
  报错 ‘ERROR:aiohttp.server:Error handling request’
  发现所有的await handler(request) 语句都出问题，包括web框架里的
应该异步IO的问题，哪个地方的协程装饰器有问题？
  错误原因分析：
  （1）、await 与 yield from 的语法不一致问题？ 已验证，不对！
  （2）、哪个地方多加或漏写 await 了？ 已验证，不对！
  找到了，好蠢啊，@post('api/users')api_registers_user()中倒数第二行少写个括号！！！
  
  可是看了讨论区很多人，虽然错误类型是一样的（HTTP 500），但是具体错误实际各不相同，在StackOverflow看到个查看错误详情的方法，先mark下！
  https://stackoverflow.com/questions/5385714/deploying-website-500-internal-server-error

#### 登录模块

1、数据库中由于前几天的测试，已经有一些用户数据，不能用他们测试登录模块，因为这些密码没有经过sha1算法处理，不能匹配登录

2、遗留问题：
  登录以后，从控制台可以看到，session中已有用户信息，但是页面没有显示，而且登出按钮在那里？？

