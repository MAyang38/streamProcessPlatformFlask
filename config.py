'''

'''

bind = "0.0.0.0:8080"
# 并行工作进程数
workers = 3
# 指定每个工作者的线程数
threads = 4
# 工作模式协程
worker_class = 'gevent'
# 设置最大并发量
worker_connections = 2000

# 设置访问日志和错误信息日志路径
accesslog = './log/gunicorn_acess.log'
errorlog = './log/gunicorn_error.log'
# 设置日志记录水平
loglevel = 'warning'