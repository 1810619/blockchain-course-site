# -*- coding: utf-8 -*-
# File : scheduler2.py
# Author: taoyahui
# Date : 2022/4/1
from flask import Flask
from flask_apscheduler import APScheduler
import datetime
# 第一步：创建Flask执行对象app
app = Flask(__name__)
# 第二步： 创建APScheduler调度器
scheduler = APScheduler()
# 第三步：配置Flask app进程，打开调度器
class Config(object):
    SCHEDULER_API_ENABLED = True
# 第四步：在Flask对象中加载配置
app.config.from_object(Config())
# 第五步：将Flask执行对象和调度器绑定
scheduler.init_app(app)

# 第六步：创建定时启动的任务
@scheduler.task('interval', id='job1', seconds=5, misfire_grace_time=900)
def job1():
    print(str(datetime.datetime.now()) + ' executed job1!')

if __name__ == '__main__':
    # 第七步：启动定时器
    scheduler.start()
    # 第八步：启动Flask进程
    app.run(port=8000)

