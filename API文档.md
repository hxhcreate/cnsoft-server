## 统一格式说明

### code说明：

> 200 成功
>
> 403 账号或密码验证失败
>
> 4000 数据不正确或不合理
>
> 4001 数据库操作出错
>
> 4002 数据库连接出错

### 地址

> http://127.0.0.1:5000/

### 格式说明

在任何情况下，服务器返回的`body`中的JSON数据必须是一个对象，用`code`返回业务状态，用`data`返回客户端要请求的实际数据，用`message`返回业务失败后的提示信息；其中`code`值为200时表示业务成功，`code`值为其它时表示业务失败；其中`data`可以是`Entity（对象）`，也可以是`List<Entity>（数组）`。

服务端返回的数据的结构应该是：

```json
{
    "code": 200,
    "data": ?,
    "message": "I am message."
}
```

- 例如返回的业务数据是空时：

  ```json
  {
      "code": 200,
      "data": null,
      "message": "Succeed"
  }
  ```

- 例如返回的业务数据是字符串或者数字时：

  ```json
  {
      "code": 200,
      "data": "20180101",
      "message": "Succeed"
  }
  ```

- 例如返回的业务数据是一个对象时：

  ```json
  {
      "code": 200,
      "data": {
          "name": "Kalle",
          "url": "https://github.com/yanzhenjie/Kalle",
      },
      "message": "Succeed"
  }
  ```

- 例如返回的业务数据是一个数组时：

  ```json
  {
      "code": 200,
      "data": [
          {
              "name": "Kalle",
              "url": "https://github.com/yanzhenjie/Kalle",
          },
          {
              "name": "Kalle",
              "url": "https://github.com/yanzhenjie/Kalle",
          },
      ],
      "message": "Succeed."
  }
  ```

- 例如当业务失败时返回失败原因：

  ```json
  {
      "code": 403,
      "data": null,
      "message": "帐号密码错误"
  }
  ```

## 安卓客户端

### 会话管理

- 注册

  ```
  请求：POST
  url: /register
  Content-Type：Aplication/json
  body: {
      "username": "",
      "password": ""
  }
  正确结果： { 
      data:
      msg: "",
      status: 200
  }
  错误结果： {
      msg: "",
      status: 
  }
  ```

- 登录

  ```
  请求：POST
  url: /login
  Content-Type：Aplication/json
  body: {
      "username": "",
      "password": ""
  }
  正确结果： { 
      data:
      msg: "",
      status: 200
  }
  错误结果： {
      msg: "",
      status: 
  }
  ```


- 注销

  ```
  请求：GET
  url：/logout
  参数：[]
  响应：{"success"}
  ```

### 新闻获取

- 按ID获取

  ```
  
  ```

- 获取推荐

  ```
  ```

### 用户行为

- 记录进入某新闻

  ```
  ```

  

## 管理页面前端

