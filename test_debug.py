"""
最小限のテスト用ファイル
"""
import streamlit as st

try:
    print("Step 1: Streamlitインポート成功")
    
    import constants as ct
    print("Step 2: constants.pyインポート成功")
    
    from initialize import initialize
    print("Step 3: initialize.pyインポート成功")
    
    from langchain_openai import OpenAIEmbeddings
    print("Step 4: OpenAIEmbeddingsインポート成功")
    
    from dotenv import load_dotenv
    load_dotenv()
    print("Step 5: .env読み込み成功")
    
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"Step 6: APIキー確認成功 (最初の10文字: {api_key[:10]}...)")
    else:
        print("Step 6: APIキーが見つかりません")
    
    embeddings = OpenAIEmbeddings()
    print("Step 7: OpenAIEmbeddings作成成功")
    
    st.write("テスト完了：すべて正常")
    
except Exception as e:
    print(f"エラー発生: {e}")
    import traceback
    traceback.print_exc()
    st.error(f"エラー: {e}")