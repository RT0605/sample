"""
このファイルは、画面表示に特化した関数定義のファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
import streamlit as st
import utils
import constants as ct

############################################################
# 関数定義
############################################################

def display_app_title():
    """
    タイトル表示
    """
    st.markdown(f"## {ct.APP_NAME}")

def display_select_mode():
    """
    回答モードのラジオボタンを表示
    """
    col1, col2 = st.columns([100, 1])
    with col1:
        st.session_state.mode = st.radio(
            label="",
            options=[ct.ANSWER_MODE_1, ct.ANSWER_MODE_2],
            label_visibility="collapsed"
        )

def display_initial_ai_message():
    """
    AIメッセージの初期表示
    """
    with st.chat_message("assistant"):
        st.markdown("こんにちは。私は社内文書の情報をもとに回答する生成AIチャットボットです。上記で利用目的を選択し、画面下部のチャット欄からメッセージを送信してください。")

        st.markdown("**【「社内文書検索」を選択した場合】**")
        st.info("入力内容と関連性が高い社内文書のありかを検索できます。")
        st.code("【入力例】\n社員の育成方針に関するMTGの議事録", wrap_lines=True, language=None)

        st.markdown("**【「社内問い合わせ」を選択した場合】**")
        st.info("質問・要望に対して、社内文書の情報をもとに回答を得られます。")
        st.code("【入力例】\n人事部に所属している従業員情報を一覧化して", wrap_lines=True, language=None)

def display_conversation_log():
    """
    会話ログの一覧表示
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])
            else:
                # 社内文書検索
                if message["content"]["mode"] == ct.ANSWER_MODE_1:
                    if not "no_file_path_flg" in message["content"]:
                        st.markdown(message["content"]["main_message"])
                        icon = utils.get_source_icon(message['content']['main_file_path'])
                        main_file_path = message['content']['main_file_path']
                        main_page_number = message['content'].get('main_page_number')
                        display_name = utils.get_file_display_name(main_file_path, main_page_number)
                        st.success(display_name, icon=icon)

                        if "sub_message" in message["content"]:
                            st.markdown(message["content"]["sub_message"])
                            for sub_choice in message["content"]["sub_choices"]:
                                icon = utils.get_source_icon(sub_choice['source'])
                                sub_file_path = sub_choice['source']
                                sub_page_number = sub_choice.get('page_number')
                                sub_display_name = utils.get_file_display_name(sub_file_path, sub_page_number)
                                st.info(sub_display_name, icon=icon)
                    else:
                        st.markdown(message["content"]["answer"])
                else:
                    # 社内問い合わせ
                    st.markdown(message["content"]["answer"])
                    if "file_info_list" in message["content"]:
                        st.divider()
                        st.markdown(f"##### {message['content']['message']}")
                        for file_info in message["content"]["file_info_list"]:
                            # file_infoは「ファイルパス」のみが渡ってくる場合があるため、ページ番号情報を分離する必要あり
                            # ここではutils.get_file_display_name()を呼ぶために分割パターンを想定
                            if isinstance(file_info, dict):
                                file_path = file_info.get("file_path")
                                page_number = file_info.get("page_number")
                                icon = utils.get_source_icon(file_path)
                                display_name = utils.get_file_display_name(file_path, page_number)
                                st.info(display_name, icon=icon)
                            else:
                                # 古い構造ならそのまま
                                icon = utils.get_source_icon(file_info)
                                st.info(file_info, icon=icon)

def display_search_llm_response(llm_response):
    """
    「社内文書検索」モードにおけるLLMレスポンスを表示
    """
    if llm_response["context"] and llm_response["answer"] != ct.NO_DOC_MATCH_ANSWER:
        main_file_path = llm_response["context"][0].metadata["source"]
        main_page_number = llm_response["context"][0].metadata.get("page")
        main_message = "入力内容に関する情報は、以下のファイルに含まれている可能性があります。"
        st.markdown(main_message)
        icon = utils.get_source_icon(main_file_path)
        main_display = utils.get_file_display_name(main_file_path, main_page_number)
        st.success(main_display, icon=icon)

        sub_choices = []
        duplicate_check_list = []
        for document in llm_response["context"][1:]:
            sub_file_path = document.metadata["source"]
            if sub_file_path == main_file_path or sub_file_path in duplicate_check_list:
                continue
            duplicate_check_list.append(sub_file_path)
            sub_page_number = document.metadata.get("page")
            sub_display = utils.get_file_display_name(sub_file_path, sub_page_number)
            icon = utils.get_source_icon(sub_file_path)
            sub_choices.append({"display": sub_display, "icon": icon})

        if sub_choices:
            sub_message = "その他、ファイルありかの候補を提示します。"
            st.markdown(sub_message)
            for sub in sub_choices:
                st.info(sub["display"], icon=sub["icon"])

        # 会話ログ用に渡すデータ
        content = {}
        content["mode"] = ct.ANSWER_MODE_1
        content["main_message"] = main_message
        content["main_file_path"] = main_file_path
        if main_page_number is not None:
            content["main_page_number"] = main_page_number
        if sub_choices:
            content["sub_message"] = sub_message
            # サブドキュメント用のファイル名とページ番号を渡す
            content["sub_choices"] = [
                {"source": document.metadata["source"], "page_number": document.metadata.get("page")}
                for document in llm_response["context"][1:]
                if document.metadata["source"] not in [main_file_path] + duplicate_check_list[:-1]
            ]
    else:
        st.markdown(ct.NO_DOC_MATCH_MESSAGE)
        content = {}
        content["mode"] = ct.ANSWER_MODE_1
        content["answer"] = ct.NO_DOC_MATCH_MESSAGE
        content["no_file_path_flg"] = True
    return content

def display_contact_llm_response(llm_response):
    """
    「社内問い合わせ」モードにおけるLLMレスポンスを表示
    """
    st.markdown(llm_response["answer"])
    if llm_response["answer"] != ct.INQUIRY_NO_MATCH_ANSWER:
        st.divider()
        message = "情報源"
        st.markdown(f"##### {message}")
        file_info_list = []
        for document in llm_response["context"]:
            file_path = document.metadata["source"]
            page_number = document.metadata.get("page")
            display_name = utils.get_file_display_name(file_path, page_number)
            icon = utils.get_source_icon(file_path)
            st.info(display_name, icon=icon)
            file_info_list.append({"file_path": file_path, "page_number": page_number})
        content = {}
        content["mode"] = ct.ANSWER_MODE_2
        content["answer"] = llm_response["answer"]
        content["message"] = message
        content["file_info_list"] = file_info_list
    else:
        content = {}
        content["mode"] = ct.ANSWER_MODE_2
        content["answer"] = llm_response["answer"]
    return content
