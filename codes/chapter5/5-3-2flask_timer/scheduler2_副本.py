# -*- coding: utf-8 -*-
# File : scheduler2.py
# Author: taoyahui
# Date : 2022/4/1

from flask import Flask       #引入必要的库
from flask_apscheduler import APScheduler
import datetime

app = Flask(__name__)       #第一步：创建Flask应用对象app
scheduler = APScheduler()   #第二步：创建APScheduler调度器对象

class Config(object):       # 第三步：定义一个配置类，用于配置Flask应用和调度器
    SCHEDULER_API_ENABLED = True  #启用调度器API

app.config.from_object(Config())  # 第四步：在Flask对象中app中加载配置

scheduler.init_app(app)    # 第五步：初始化调度器，使其与Flask执行对象app绑定

# 第六步：创建定时启动的任务
@scheduler.task('interval', id='job1', seconds=5, misfire_grace_time=900)
def job1():
    print(str(datetime.datetime.now()) + ' executed job1!')

if __name__ == '__main__':  #代码在直接运行脚本时执行
    scheduler.start()       # 第七步：启动定时器
    app.run(port=8000)      # 第八步：启动Flask进程

