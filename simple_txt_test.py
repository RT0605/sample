"""
.txtファイル対応の簡易テスト
"""
import os
from pathlib import Path

print("=== .txtファイル対応テスト ===")

# 1. 定数ファイル確認
print("1. constants.py の確認...")
import constants as ct
print(f"   サポートされている拡張子: {list(ct.SUPPORTED_EXTENSIONS.keys())}")

# 2. .txtファイル検出確認
print("2. .txtファイル検出...")
import utils
files = utils.get_file_list(ct.RAG_TOP_FOLDER_PATH, ct.SUPPORTED_EXTENSIONS)
txt_files = [f for f in files if f.endswith('.txt')]
print(f"   検出された.txtファイル数: {len(txt_files)}")
for txt_file in txt_files:
    print(f"     - {txt_file}")

# 3. TextLoader単体テスト
print("3. TextLoader 単体テスト...")
try:
    from langchain_community.document_loaders import TextLoader
    
    # 議事録ルール.txtを直接読み込み
    txt_path = "./data/MTG議事録/議事録ルール.txt"
    if os.path.exists(txt_path):
        loader = TextLoader(txt_path, encoding="utf-8")
        documents = loader.load()
        print(f"   ✓ ファイル読み込み成功: {len(documents)}件")
        if documents:
            content_preview = documents[0].page_content[:100].replace('\n', ' ')
            print(f"     内容プレビュー: {content_preview}...")
    else:
        print(f"   ✗ ファイルが見つかりません: {txt_path}")
except Exception as e:
    print(f"   ✗ TextLoaderエラー: {e}")

# 4. 初期化テスト
print("4. initialize() 関数テスト...")
try:
    from initialize import initialize
    initialize()
    print("   ✓ 初期化成功！.txtファイルもRAGに組み込まれました！")
except Exception as e:
    print(f"   ✗ 初期化エラー: {e}")
    import traceback
    traceback.print_exc()

print("\n=== テスト完了 ===")
