from flask import Blueprint

"""用户操作接口"""
user = Blueprint("user", __name__)

from . import api
