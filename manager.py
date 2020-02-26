#coding=utf-8
# 启动脚本
import os
from app import create_app
from flask_script import Manager
from flask import render_template



app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # 统一进行实例化
manager = Manager(app)



@app.route('/')
def index():
    return render_template('index_2.html')


# @manager.command
# def test():
#     """Run the unit tests."""
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    # manager.run(host='0.0.0.0', port='5001')  #使用manager时不允许内部指定端口号 可以python manage.py runserver -p 8066
    manager.run()




