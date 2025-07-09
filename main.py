import streamlit as st

# 定数
APP_NAME = "社内情報特化型生成AI検索アプリ"
ANSWER_MODE_1 = "社内文書検索"
ANSWER_MODE_2 = "社内問い合わせ"
CHAT_INPUT_HELPER_TEXT = "こちらからメッセージを送信してください。"

st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS追加: サイドバー・全体・フッター・英語UI非表示 ---
st.markdown("""
    <style>
    /* 全体paddingなど */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    .main {
        background-color: #fcfaf7 !important;
    }
    /* サイドバーを画面左に強制固定・高さ100vh */
    .my-sidebar {
        background-color: #F5F6FA;
        min-height: 100vh !important;
        height: 100vh !important;
        padding: 32px 18px 32px 36px;
        border-right: 1px solid #e6e6e6;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        position: relative;
    }
    hr {
        border: none;
        border-top: 1.5px solid #e4e4e4;
        margin:14px 0 18px 0;
    }
    .ex-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 7px;
        margin-top: 18px;
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
    /* Chat input/footer 英語UI非表示 */
    footer, #MainMenu, .st-emotion-cache-1avcm0n.ezrtsby2, .stActionButton, .stDeployButton, .css-jn99sy {
        display: none !important;
    }
    .stChatFloatingInputContainer button {
        font-size: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2カラムレイアウト作成 ---
col_sidebar, col_main = st.columns([0.33, 0.67], gap="small")

# --- 左側サイドバー ---
with col_sidebar:
    st.markdown(f"""
    <div class="my-sidebar">
        <div style="font-size:1.23rem; font-weight:700; margin-bottom:18px;">
            利用目的
        </div>
        <div style="margin-bottom:12px;">
    """, unsafe_allow_html=True)
    # ラジオボタンのみPythonで
    mode = st.radio(
        "",
        [ANSWER_MODE_1, ANSWER_MODE_2],
        key="mode",
        label_visibility="collapsed"
    )
    st.markdown("""
        </div>
        <hr>
        <div class="ex-title">「社内文書検索」を選択した場合</div>
        <div class="ex-info">入力内容と関連性が高い社内文書のありかを検索できます。</div>
        <div style="font-size:1.01rem; font-weight: 500; margin-bottom:3px; margin-top:8px;">【入力例】</div>
        <div class="ex-code">社員の育成方針に関するMTGの議事録</div>

        <div class="ex-title">「社内問い合わせ」を選択した場合</div>
        <div class="ex-info">質問・要望に対して、社内文書の情報をもとに回答を得られます。</div>
        <div style="font-size:1.01rem; font-weight: 500; margin-bottom:3px; margin-top:8px;">【入力例】</div>
        <div class="ex-code">人事部に所属している従業員情報を一覧化して</div>
    </div>
    """, unsafe_allow_html=True)

# --- 右側メインエリア ---
with col_main:
    st.markdown(f"<h1 style='text-align:center; margin-bottom:24px;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    st.success("こんにちは。私は社内文書の情報をもとに回答する生成AIチャットボットです。サイドバーで利用目的を選択し、画面下部のチャット欄からメッセージを送信してください。")
    st.warning("具体的に入力したほうが期待通りの回答を得やすいです。")

# --- チャット欄（日本語プレースホルダで全幅・下部） ---
chat_message = st.chat_input(CHAT_INPUT_HELPER_TEXT)
if chat_message:
    st.write("チャット送信：" + chat_message)
    # ここにチャット履歴やAI応答処理を追加
