# 创建认证蓝本,蓝本构造文件
from flask import Blueprint

ncov = Blueprint('ncov', __name__)

from . import views