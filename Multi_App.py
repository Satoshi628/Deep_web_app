#coding: utf-8
#----- 標準ライブラリ -----#
#None

#----- 専用ライブラリ -----#
import streamlit as st
#----- 自作モジュール -----#
#None
import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = {}

    def add_app(self, title, func):
        """

        Args:
            title ([type]): [description]
            func ([type]): [description]
        """        
        self.apps.update({title: func})

    def run(self):
        app = st.sidebar.radio(
            'AI 選択',
            [app for app in self.apps.keys()])
        
        self.apps[app]()
