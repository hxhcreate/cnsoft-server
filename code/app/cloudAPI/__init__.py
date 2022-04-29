from flask import Blueprint


"""管理员操作接口"""
cloudAPI = Blueprint("cloudAPI", __name__)

from . import api
