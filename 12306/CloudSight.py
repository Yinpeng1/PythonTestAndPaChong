import urllib.request
import  urllib.parse
import  cloudsight

auth = cloudsight.OAuth("nSmkfLGwl4-yW1s-swKoXA", "8u3iemtYYiIcFaZOK1E4QA")
api = cloudsight.API(auth)

with open('0_1.png', 'rb') as f:
    response = api.image_request(f, '0_1.png', {
        'image_request[locale]': 'zh-CN',
        'image_request[language]': 'zh-CN'
    })
print(response)