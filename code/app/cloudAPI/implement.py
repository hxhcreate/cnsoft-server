from ecloud import CMSSEcloudOcrClient
import json
import base64


accesskey = 'e74480e45cd5404aa72d6c536e1f3933'
secretkey = '25c9f0e30e0d4ba6aa4c6b302985f8cf'
url = 'https://api-wuxi-1.cmecloud.cn:8443'

# 语音转文字
def audio2text(audioBase64):
    pass

# 文字转语音
def text2audio(text):
    pass

# 图片转文字
def img2text(imgBase64):
    # print("请求URL参数")
    if not imgBase64:
        return '', False
    requesturl = '/api/ocr/v1/general'
    try:
        ocr_client = CMSSEcloudOcrClient(accesskey, secretkey, url)
        response = ocr_client.request_ocr_service_base64(requesturl, imgBase64)
        j = json.loads(response.text)
        # print(json.dumps(j, indent=2))
        if j.get('errorcode', '1') == 0:
            text = ''
            for row in j.get('items', []):
                text += row.get('itemstring', '')
            return text, True
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)
    return "", False

if __name__ == '__main__':
    import requests
    imageurl = r'https://img2.baidu.com/it/u=2026838953,131045863&fm=253&fmt=auto&app=138&f=PNG?w=500&h=658'
    img = requests.get(imageurl).content
    imgBase64 = base64.encodebytes(img).decode()
    print(img2text(imgBase64))
