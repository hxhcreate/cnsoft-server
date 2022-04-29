import time
from datetime import datetime

from flask import request, jsonify, session

from . import cloudAPI
from . import implement


"""云API接口"""

@cloudAPI.route("/", methods=['GET'])
def cloudAPI_index():
    return "success!"

# 先不实时
@cloudAPI.route("/audio2text", methods=['POST'])
def cloudAPI_audio2text():
    audioBase64 = request.json.get("audioBase64", "")
    text, res = implement.audio2text(audioBase64)
    if res:
        return jsonify(code=200, msg="success", data={"text": text})
    else:
        return jsonify(code=401, msg="audio to text error", data={'text': ''})

@cloudAPI.route("/text2audio", methods=['POST'])
def cloudAPI_text2audio():
    text = request.json.get("text", "")
    audioBase64, res = implement.text2audio(text)
    if res:
        return jsonify(code=200, msg="success", data={"audioBase64": audioBase64})
    else:
        return jsonify(code=401, msg="text to audio error", data={'audioBase64': ''})

@cloudAPI.route("/img2text", methods=['POST'])
def cloudAPI_img2text():
    imgBase64 = request.json.get("imgBase64", "")
    text, res = implement.img2text()
    if res:
        return jsonify(code=200, msg="success", data={'text': text})
    else:
        return jsonify(code=401, msg="img to text error", data={'text': ''})

