from flask import Blueprint


"""管理员操作接口"""
admin = Blueprint("admin", __name__)

from . import api