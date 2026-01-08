# -*- coding: utf-8 -*-
# File : scheduler1.py
# Author: taoyahui
# Date : 2022/4/2

from flask import Flask   #引入必要的库
import datetime
from flask_apscheduler import APScheduler
class Config(object):     #定义一个配置类Config，用于配置定时任务
    """
    创建定时器的配置内容，需要加载进入Flask进程
    """
    # 执行任务内容，这里以间隔的方式实现
    JOBS = [
        {
            'id': 'job1',
            'func': 'scheduler1:task1',  # 这里表示task1函数在scheduler1.py中定义
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 10
        }
    ]
    # 用于启动定时器，True表示启动
    SCHEDULER_API_ENABLED = True

# 定义间隔执行任务时执行的函数
def task1(a, b):
    print(f'{datetime.datetime.now()} execute simple task a+b is {a}+{b}={a+b} ')


if __name__ == '__main__':
    # 第一步：创建Flask执行对象app
    app = Flask(__name__)
    # 第二步：在Flask对象中加载定时任务的配置
    app.config.from_object(Config())
    # 第三步： 创建APScheduler调度器
    scheduler = APScheduler()
    # 第四步： 将Flask执行对象和调度器绑定
    scheduler.init_app(app)
    # 第五步： 启动调度器
    scheduler.start()
    # 第六步： 启动Flask进程
    app.run(port=8001)
