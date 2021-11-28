#coding: utf-8
#----- 標準ライブラリ -----#
import os
from os.path import join, dirname

#----- 専用ライブラリ -----#
from dotenv import load_dotenv
import streamlit
import requests

#----- 自作モジュール -----#
# None

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API_KEY")

_AI_DICT = {'Dream':            "https://api.deepai.org/api/deepdream",
            'Similarity':       "https://api.deepai.org/api/image-similarity",
            'Color':            "https://api.deepai.org/api/colorizer",
            'Style Transfer':   "https://api.deepai.org/api/fast-style-transfer",
            'Resolution':       "https://api.deepai.org/api/torch-srgan",
            'Toy':              "https://api.deepai.org/api/toonify",
            }


def deep_ai_func(AI_key, **kwargs):
    if not AI_key in _AI_DICT:  # キーがあるかどうか
        raise KeyError("AI_keyが{}以外の文字になっています。".format(list(_AI_DICT.keys())))

    output = requests.post(
        _AI_DICT[AI_key],
        files=kwargs,
        headers={'api-key': API_KEY}
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
