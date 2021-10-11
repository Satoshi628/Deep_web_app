#coding: utf-8
#----- 標準ライブラリ -----#
# None

#----- 専用ライブラリ -----#
import streamlit
import requests
#----- 自作モジュール -----#
# None

_API_KEY = 'd6faf39d-dd5e-4516-b817-fcc776ae3a94'

_AI_DICT = {'Dream':        "https://api.deepai.org/api/deepdream",
            'Similarity':   "https://api.deepai.org/api/image-similarity",
            'Color':        "https://api.deepai.org/api/colorizer",
            'Resolution':   "https://api.deepai.org/api/torch-srgan",
            'Toy':          "https://api.deepai.org/api/toonify",
            }


def deep_ai_func(AI_key, **kwargs):
    if not AI_key in _AI_DICT:  # キーがあるかどうか
        raise KeyError("AI_keyが{}以外の文字になっています。".format(list(_AI_DICT.keys())))

    output = requests.post(
        _AI_DICT[AI_key],
        files=kwargs,
        headers={'api-key': _API_KEY}
    )
    output = output.json()
    #return None
    if "output_url" in output.keys():
        image_response = requests.get(output["output_url"])
        image = image_response.content
        return image
    if "output" in output.keys():
        if "distance" in output["output"].keys():
            distance = output["output"]["distance"]
            return distance
    return None


#deep_ai_func(AI_key="Dream", image=open('content.jpg', 'rb'))

"""
#恐怖画像に(Style Transfer)
r = requests.post(
    "https://api.deepai.org/api/deepdream",
    files={
        'image': open('style.jpg', 'rb'),
    },
    headers={'api-key': 'd6faf39d-dd5e-4516-b817-fcc776ae3a94'}
)
print(r.json())



#neural style transfer
#使えない
r = requests.post(
    "https://api.deepai.org/api/neural-style",
    files={
        'style': open('style.jpg', 'rb'),
        'content': open('content.jpg', 'rb'),
    },
    headers={'api-key': 'd6faf39d-dd5e-4516-b817-fcc776ae3a94'}
)



#画像同士が似ているか似ていないか
r = requests.post(
    "https://api.deepai.org/api/image-similarity",
    files={
        'image1': open('content.jpg', 'rb'),
        'image2': open('style.jpg', 'rb'),
    },
    headers={'api-key': 'd6faf39d-dd5e-4516-b817-fcc776ae3a94'}
)
print(r.json())


#白黒をカラーに
r = requests.post(
    "https://api.deepai.org/api/colorizer",
    files={
        'image': open('content.jpg', 'rb'),
    },
    headers={'api-key': 'd6faf39d-dd5e-4516-b817-fcc776ae3a94'}
)
print(r.json())


#高解像度に
r = requests.post(
    "https://api.deepai.org/api/torch-srgan",
    files={
        'image': open('content.jpg', 'rb'),
    },
    headers={'api-key': 'd6faf39d-dd5e-4516-b817-fcc776ae3a94'}
)
print(r.json())


#テキストから画像を
r = requests.post(
    "https://api.deepai.org/api/text2img",
    files={
        'text': open('text.txt', 'rb'),
    },
    headers={'api-key': 'd6faf39d-dd5e-4516-b817-fcc776ae3a94'}
)
print(r.json())


#顔をディズニー、ピクサー風に
r = requests.post(
    "https://api.deepai.org/api/toonify",
    files={
        'image': open('content.jpg', 'rb'),
    },
    headers={'api-key': 'd6faf39d-dd5e-4516-b817-fcc776ae3a94'}
)
print(r.json())

"""
