#预加载资源
preload_app = True
 
# 并行工作进程数
workers = 2
 
# 指定每个工作者的线程数
threads = 2
 
# 端口 5000
bind = '127.0.0.1:5001'
 
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
 
# 工作模式协程
worker_class = 'gevent'
 
# 设置最大并发量
worker_connections = 2000
 
# 设置进程文件目录
pidfile = '/var/run/gunicorn.pid'
 
# 设置访问日志和错误信息日志路径
accesslog = "/home/gunicorn/access.log"
errorlog = "/home/gunicorn/error.log"
 
# 设置日志记录水平 
loglevel = 'warning'

keyfile = cert/server.key
certfile = cert/server.crt