"""
TXTファイルのsafe_text_loader動作テスト用スクリプト
"""
from constants import safe_text_loader
import sys

if __name__ == "__main__":
    path = "data/MTG議事録/議事録ルール.txt"
    try:
        loader = safe_text_loader(path)
        docs = loader.load()
        print(f"SUCCESS: {path} 読み込み成功。ドキュメント数: {len(docs)}")
        for i, doc in enumerate(docs):
            print(f"--- Document {i+1} ---")
            print(doc.page_content[:500])
    except Exception as e:
        print(f"ERROR: {path} 読み込み失敗: {e}")
        sys.exit(1)