import streamlit as st

# --- 定数 ---
APP_NAME = "社内情報特化型生成AI検索アプリ"
ANSWER_MODE_1 = "社内文書検索"
ANSWER_MODE_2 = "社内問い合わせ"
CHAT_INPUT_HELPER_TEXT = "こちらからメッセージを送信してください。"

st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS（画像通りに余白やフォント調整） ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    .main {
        background-color: #fcfaf7;
    }
    .sidebar-style {
        background-color: #F5F6FA;
        min-height: 100vh;
        height: 100%;
        padding: 32px 18px 32px 36px;
        border-right: 1px solid #e6e6e6;
    }
    .app-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: bold;
        margin-top: 28px;
        margin-bottom: 32px;
        letter-spacing: .02em;
    }
    .msg-success {
        background: #E9F9ED;
        color: #23492d;
        border-radius: 7px;
        padding: 14px 22px 14px 45px;
        margin-bottom: 14px;
        border-left: 8px solid #b5edcc;
        position: relative;
        font-size: 1.05rem;
    }
    .msg-success:before {
        content: "💬";
        position: absolute;
        left: 15px;
        top: 12px;
        font-size: 1.3rem;
    }
    .msg-warning {
        background: #FFF7E3;
        color: #6b531d;
        border-radius: 7px;
        padding: 14px 22px 14px 45px;
        margin-bottom: 12px;
        border-left: 8px solid #ffe299;
        position: relative;
        font-size: 1.05rem;
    }
    .msg-warning:before {
        content: "⚠️";
        position: absolute;
        left: 15px;
        top: 11px;
        font-size: 1.25rem;
    }
    .ex-section {
        margin-top: 18px;
        margin-bottom: 0px;
    }
    .ex-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 7px;
        margin-top: 18px;
    }
    .stRadio > div {
        gap: 8px;
    }
    .ex-info {
        background: #e3f0fb;
        color: #1d3755;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-left: 5px solid #93bde9;
        font-size: 0.98rem;
    }
    .ex-code {
        background: #f8f9fa;
        color: #222;
        border-radius: 4px;
        padding: 8px 12px;
        margin-top: 2px;
        margin-bottom: 8px;
        font-family: "Consolas", "Menlo", "monospace";
        font-size: 0.98rem;
        border: 1px solid #ececec;
    }
    .stChatInputContainer {
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2カラムレイアウト作成 ---
col_sidebar, col_main = st.columns([0.33, 0.67])

# --- 左側（サイドバー風） ---
with col_sidebar:
    st.markdown('<div class="sidebar-style">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:1.23rem; font-weight:700; margin-bottom:26px;">利用目的</div>', unsafe_allow_html=True)
    mode = st.radio(
        "",
        [ANSWER_MODE_1, ANSWER_MODE_2],
        key="mode",
        label_visibility="collapsed"
    )

    # 社内文書検索の説明
    st.markdown('<div class="ex-section"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ex-title">「社内文書検索」を選択した場合</div>', unsafe_allow_html=True)
    st.markdown('<div class="ex-info">入力内容と関連性が高い社内文書のありかを検索できます。</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:1.01rem; font-weight: 500; margin-bottom:3px; margin-top:8px;">【入力例】</div>', unsafe_allow_html=True)
    st.markdown('<div class="ex-code">社員の育成方針に関するMTGの議事録</div>', unsafe_allow_html=True)

    # 社内問い合わせの説明
    st.markdown('<div class="ex-title">「社内問い合わせ」を選択した場合</div>', unsafe_allow_html=True)
    st.markdown('<div class="ex-info">質問・要望に対して、社内文書の情報をもとに回答を得られます。</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:1.01rem; font-weight: 500; margin-bottom:3px; margin-top:8px;">【入力例】</div>', unsafe_allow_html=True)
    st.markdown('<div class="ex-code">人事部に所属している従業員情報を一覧化して</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 右側（メインエリア） ---
with col_main:
    st.markdown(f'<div class="app-title">{APP_NAME}</div>', unsafe_allow_html=True)
    st.markdown('<div class="msg-success">こんにちは。私は社内文書の情報をもとに回答する生成AIチャットボットです。サイドバーで利用目的を選択し、画面下部のチャット欄からメッセージを送信してください。</div>', unsafe_allow_html=True)
    st.markdown('<div class="msg-warning">具体的に入力したほうが期待通りの回答を得やすいです。</div>', unsafe_allow_html=True)

    # ここにチャット履歴を表示する場合は、追加
    # for msg in st.session_state.get("messages", []):
    #     with st.chat_message(msg["role"]):
    #         st.markdown(msg["content"])

# --- チャット欄（全幅・最下部） ---
chat_message = st.chat_input(CHAT_INPUT_HELPER_TEXT)

# チャット送信時の処理（例：履歴に追加など）
if chat_message:
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    st.session_state["messages"].append({"role": "user", "content": chat_message})
    # ここでAIのレスポンスを追加してもOK
    # st.session_state["messages"].append({"role": "assistant", "content": "AIの回答"})
