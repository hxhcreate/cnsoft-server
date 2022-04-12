code说明：
> 200 成功
> 
> 4000 数据不正确或不合理
> 
> 4001 数据库操作出错
> 
> 4002 数据库连接出错
> 

###用户
- 注册
```
请求：POST
请求头：Aplication/json
body: {
    "username": "",
    "password": ""
}
正确结果： { 
    data:
    msg: “”,
    status: 200
}
错误结果： {
    msg: "",
    status: 
}
```
- 登录

###管理员


###Web数据展示