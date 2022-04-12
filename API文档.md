code说明：
> 200 成功
> 
> 4000 数据不正确或不合理
> 
> 4001 数据库操作出错
> 
> 4002 数据库连接出错

地址
> http:127.0.0.1:5000/

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

