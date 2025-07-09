"""
main.pyの簡易テスト版
"""
import streamlit as st
import logging
from initialize import initialize
import utils
import components as cn
import constants as ct

st.set_page_config(
    page_title=ct.APP_NAME,
    layout="wide"
)

# フッター・右下英語の非表示
st.markdown("""
    <style>
    footer, #MainMenu, .st-emotion-cache-1avcm0n, .css-jn99sy {visibility: hidden !important; display: none !important;}
    </style>
""", unsafe_allow_html=True)

try:
    print("main.py: initialize()開始")
    initialize()
    print("main.py: initialize()完了")
    st.write("初期化成功！")
except Exception as e:
    print(f"main.py: initialize()エラー: {e}")
    import traceback
    traceback.print_exc()
    st.error(f"初期化エラー: {e}")