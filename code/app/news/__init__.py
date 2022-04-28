from flask import Blueprint

"""用户操作接口"""
news = Blueprint("news", __name__)

from . import api
