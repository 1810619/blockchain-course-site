# -*- coding: utf-8 -*-
# File : scheduler1.py
# Author: taoyahui
# Date : 2022/4/2

from flask import Flask   #引入必要的库
import datetime
from flask_apscheduler import APScheduler
class Config(object):     #定义一个配置类Config，用于配置定时任务
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

'''定义间隔执行的任务函数task1，该函数将在定时任务触发时执行。
它接收两个参数a和b，并打印当前时间和它们的和'''
def task1(a, b):
    print(f'{datetime.datetime.now()} execute simple task a+b is {a}+{b}={a+b} ')

#通过以下六个步骤启动Flask应用和调度器
if __name__ == '__main__':
    app = Flask(__name__)            # 第一步：创建Flask执行对象app
    app.config.from_object(Config()) # 第二步：在Flask对象中加载定时任务的配置
    scheduler = APScheduler()        # 第三步：创建APScheduler调度器
    scheduler.init_app(app)          # 第四步：初始化调度器，使其与Flask应用对象绑定
    scheduler.start()                # 第五步：启动调度器
    app.run(port=8001)               # 第六步：启动Flask进程,使其运行在端口8001上
