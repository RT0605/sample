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

# ---- サイドバーエリア ----
with st.sidebar:
    st.markdown(
        """
        <div style="font-size:1.23rem; font-weight:700; margin-bottom:18px;">
            利用目的
        </div>
        """, unsafe_allow_html=True)
    mode = st.radio(
        "",
        [ct.ANSWER_MODE_1, ct.ANSWER_MODE_2],
        key="mode",
        label_visibility="collapsed"
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="ex-title" style="font-size: 1.05rem; font-weight: 600; margin-bottom: 7px; margin-top: 18px;">
            「社内文書検索」を選択した場合
        </div>
        <div class="ex-info" style="background: #e3f0fb; color: #1d3755; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; border-left: 5px solid #93bde9; font-size: 0.98rem;">
            入力内容と関連性が高い社内文書のありかを検索できます。
        </div>
        <div style="font-size:1.01rem; font-weight: 500; margin-bottom:3px; margin-top:8px;">
            【入力例】
        </div>
        <div class="ex-code" style="background: #f8f9fa; color: #222; border-radius: 4px; padding: 8px 12px; margin-top: 2px; margin-bottom: 8px; font-family: 'Consolas', 'Menlo', 'monospace'; font-size: 0.98rem; border: 1px solid #ececec;">
            社員の育成方針に関するMTGの議事録
        </div>
        <div class="ex-title" style="font-size: 1.05rem; font-weight: 600; margin-bottom: 7px; margin-top: 18px;">
            「社内問い合わせ」を選択した場合
        </div>
        <div class="ex-info" style="background: #e3f0fb; color: #1d3755; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; border-left: 5px solid #93bde9; font-size: 0.98rem;">
            質問・要望に対して、社内文書の情報をもとに回答を得られます。
        </div>
        <div style="font-size:1.01rem; font-weight: 500; margin-bottom:3px; margin-top:8px;">
            【入力例】
        </div>
        <div class="ex-code" style="background: #f8f9fa; color: #222; border-radius: 4px; padding: 8px 12px; margin-top: 2px; margin-bottom: 8px; font-family: 'Consolas', 'Menlo', 'monospace'; font-size: 0.98rem; border: 1px solid #ececec;">
            人事部に所属している従業員情報を一覧化して
        </div>
        """, unsafe_allow_html=True)

# --------- ここからは右側の「本体」処理（既存のロジックを維持）---------
try:
    initialize()
except Exception as e:
    logger = logging.getLogger(ct.LOGGER_NAME)
    logger.error(f"{ct.INITIALIZE_ERROR_MESSAGE}\n{e}")
    st.error(utils.build_error_message(ct.INITIALIZE_ERROR_MESSAGE), icon=ct.ERROR_ICON)
    st.stop()

if not "initialized" in st.session_state:
    st.session_state.initialized = True
    logger = logging.getLogger(ct.LOGGER_NAME)
    logger.info(ct.APP_BOOT_MESSAGE)

# タイトル表示
cn.display_app_title()

# AIメッセージの初期表示
cn.display_initial_ai_message()

# 会話ログ
try:
    cn.display_conversation_log()
except Exception as e:
    logger = logging.getLogger(ct.LOGGER_NAME)
    logger.error(f"{ct.CONVERSATION_LOG_ERROR_MESSAGE}\n{e}")
    st.error(utils.build_error_message(ct.CONVERSATION_LOG_ERROR_MESSAGE), icon=ct.ERROR_ICON)
    st.stop()

# チャット欄
chat_message = st.chat_input(ct.CHAT_INPUT_HELPER_TEXT)

if chat_message:
    logger = logging.getLogger(ct.LOGGER_NAME)
    logger.info({"message": chat_message, "application_mode": st.session_state.mode})

    with st.chat_message("user"):
        st.markdown(chat_message)

    res_box = st.empty()
    with st.spinner(ct.SPINNER_TEXT):
        try:
            llm_response = utils.get_llm_response(chat_message)
        except Exception as e:
            logger.error(f"{ct.GET_LLM_RESPONSE_ERROR_MESSAGE}\n{e}")
            st.error(utils.build_error_message(ct.GET_LLM_RESPONSE_ERROR_MESSAGE), icon=ct.ERROR_ICON)
            st.stop()

    with st.chat_message("assistant"):
        try:
            if st.session_state.mode == ct.ANSWER_MODE_1:
                content = cn.display_search_llm_response(llm_response)
            elif st.session_state.mode == ct.ANSWER_MODE_2:
                content = cn.display_contact_llm_response(llm_response)
            logger.info({"message": content, "application_mode": st.session_state.mode})
        except Exception as e:
            logger.error(f"{ct.DISP_ANSWER_ERROR_MESSAGE}\n{e}")
            st.error(utils.build_error_message(ct.DISP_ANSWER_ERROR_MESSAGE), icon=ct.ERROR_ICON)
            st.stop()

    st.session_state.messages.append({"role": "user", "content": chat_message})
    st.session_state.messages.append({"role": "assistant", "content": content})
