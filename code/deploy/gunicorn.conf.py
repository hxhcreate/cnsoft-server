#Ԥ������Դ
preload_app = True
 
# ���й���������
workers = 2
 
# ָ��ÿ�������ߵ��߳���
threads = 2
 
# �˿� 5000
bind = '127.0.0.1:5001'
 
# �����ػ�����,�����̽���supervisor����
daemon = 'false'
 
# ����ģʽЭ��
worker_class = 'gevent'
 
# ������󲢷���
worker_connections = 2000
 
# ���ý����ļ�Ŀ¼
pidfile = '/var/run/gunicorn.pid'
 
# ���÷�����־�ʹ�����Ϣ��־·��
accesslog = "/home/gunicorn/access.log"
errorlog = "/home/gunicorn/error.log"
 
# ������־��¼ˮƽ 
loglevel = 'warning'

keyfile = cert/server.key
certfile = cert/server.crt