import time
from datetime import datetime

from flask import request, jsonify, session

from . import cloudAPI
import implement


"""云API接口"""

@cloudAPI.route("/", methods=['GET'])
def cloudAPI_index():
    return "success!"

# 先不实时
@cloudAPI.route("/audio2text", methods=['POST'])
def cloudAPI_audio2text():
    return ''

@cloudAPI.route("/text2audio", methods=['POST'])
def cloudAPI_text2audio():
    return ''

@cloudAPI.route("/img2text", methods=['POST'])
def cloudAPI_img2text():
    imgBase64 = request.json.get("imgBase64", "")
    text, res = implement.img2text()
    if res:
        return jsonify(code=200, msg="success", data={'text': text})
    else:
        return jsonify(code=401, msg="img to text error", data={'text': ''})

