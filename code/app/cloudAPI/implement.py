from .ecloud import CMSSEcloudOcrClient
import json
import base64
import traceback
import time
import requests

from .ecloud.Signature import sign

def log(e):
    traceback.print_stack()
    print(e)

accesskey = 'e74480e45cd5404aa72d6c536e1f3933'
secretkey = '25c9f0e30e0d4ba6aa4c6b302985f8cf'
url = 'https://api-wuxi-1.cmecloud.cn:8443'

# 语音转文字
def audio2text(audioBase64):
    if not audioBase64:
        return '', False
    try:
        sendId = '123456'
        response = request_audio2text_send(audioBase64, sendId)
        while True:
            response = request_audio2text_recv(sendId)
            j = json.loads(response.text)
            if j.get('state', '') != 'OK':
                time.sleep(1)
                continue
            results = j.get('body', {}).get('frame_results', [])
            text = ''
            for res in results:
                text += res.get('ansStr', '')
            return text, True if text else False
    except Exception as e:
        log(e)
    return '', False

# 文字转语音
def text2audio(text):
    if not text:
        return '', False
    try:
        response = request_text2audio(text)
        if response:
            audioBase64 = response.json().get('body', {}).get('data', '')
            # play_audio(audioBase64)
            return audioBase64, True if audioBase64 else False
    except Exception as e:
        log(e)
    return '', False


# 图片转文字
def img2text(imgBase64):
    # print("请求URL参数")
    if not imgBase64:
        return '', False
    try:
        response = request_img2text(imgBase64)
        j = json.loads(response.text)
        # print(json.dumps(j, indent=2))
        if j.get('errorcode', '1') == 0:
            text = ''
            for row in j.get('items', []):
                text += row.get('itemstring', '')
            return text, True
    except ValueError as e:
        log(e)
    except Exception as e:
        log(e)
    return "", False

def play_audio(audioBase64):
    import pyaudio
    audio = base64.b64decode(audioBase64)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
            channels=2,
            rate=8000,
            output=True)
    stream.write(audio)
    stream.stop_stream()
    stream.close()
    p.terminate()
    import wave
    with wave.open("./audio.mp3", 'wb') as wave_file:
        wave_file.setframerate(16000)
        wave_file.setsampwidth(2)
        wave_file.setnchannels(1)
        wave_file.writeframes(audio)

def request_img2text(imgBase64):
    requesturl = '/api/ocr/v1/general'
    ocr_client = CMSSEcloudOcrClient(accesskey, secretkey, url)
    response = ocr_client.request_ocr_service_base64(requesturl, imgBase64)
    return response

def request_text2audio(text):
    requesturl = '/api/lingxiyun/cloud/tts/v1'
    querystring = sign('POST', accesskey, secretkey, requesturl)
    params = ''
    for(k,v) in querystring.items():
        params += str(k) + '=' + str(v) + '&'
    params = params[:-1]
    fullurl = url + requesturl + '?' + params
    s = requests.session()
    s.keep_alive = False
    body = {
        "text": text,
        "sessionParam": {
            "sid": "123456",
            "audio_coding": "raw",
            "native_voice_name": "xiaofeng"
        }
    }
    response = requests.post(fullurl, data = json.dumps(body), 
                            headers = {"Content-Type":"application/json"}, 
                            timeout = (5, 60), 
                            verify = False)
    return response

def request_audio2text_send(audioBase64, sendId):
    requesturl = '/api/lingxiyun/cloud/iat/send_request/v1'
    querystring = sign('POST', accesskey, secretkey, requesturl)
    params = ''
    for(k,v) in querystring.items():
        params += str(k) + '=' + str(v) + '&'
    params = params[:-1]
    fullurl = url + requesturl + '?' + params
    s = requests.session()
    s.keep_alive = False
    body = {
        "endFlag": 1,
        "data": audioBase64,
        "sessionParam": {
            "sid": "123456",
            "aue": "raw",
            "bos": 3000,
            "eos": 3000,
            "rst": "plain"
        }
    }
    response = requests.post(fullurl, data = json.dumps(body),
                            headers = {"Content-Type":"application/json", "streamId": sendId, "number": "1"},
                            timeout = (5, 60),
                            verify = False)
    return response

def request_audio2text_recv(sendId):
    requesturl = '/api/lingxiyun/cloud/iat/query_result/v1'
    querystring = sign('GET', accesskey, secretkey, requesturl)
    params = ''
    for(k,v) in querystring.items():
        params += str(k) + '=' + str(v) + '&'
    params = params[:-1]
    fullurl = url + requesturl + '?' + params
    s = requests.session()
    s.keep_alive = False
    response = requests.get(fullurl,
                            headers = {"Content-Type":"application/json", "streamId": sendId},
                            timeout = (5, 60),
                            verify = False)
    return response

if __name__ == '__main__':
    # import requests
    # imageurl = r'https://img2.baidu.com/it/u=2026838953,131045863&fm=253&fmt=auto&app=138&f=PNG?w=500&h=658'
    # img = requests.get(imageurl).content
    # imgBase64 = base64.encodebytes(img).decode()
    # print(img2text(imgBase64))
    audio, res = text2audio('智能语音交互')
    if res:
        print(audio2text(audio))
    else:
        print('!')