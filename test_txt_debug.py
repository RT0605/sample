"""
.txtファイル対応のデバッグテスト
"""
import os
import sys
from pathlib import Path

def test_imports():
    print("=== インポートテスト ===")
    try:
        print("constants.py をインポート中...")
        import constants as ct
        print("✓ constants.py インポート成功")
        
        print("utils.py をインポート中...")
        import utils
        print("✓ utils.py インポート成功")
        
        print("initialize.py をインポート中...")
        from initialize import initialize
        print("✓ initialize.py インポート成功")
        
        print("components.py をインポート中...")
        import components as cn
        print("✓ components.py インポート成功")
        
        return True
    except Exception as e:
        print(f"✗ インポートエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_txt_file_detection():
    print("\n=== .txtファイル検出テスト ===")
    try:
        import constants as ct
        import utils
        
        print(f"サポートされている拡張子: {list(ct.SUPPORTED_EXTENSIONS.keys())}")
        
        # txtファイルが存在するかチェック
        data_path = Path(ct.RAG_TOP_FOLDER_PATH)
        txt_files = list(data_path.rglob("*.txt"))
        print(f"発見された.txtファイル: {len(txt_files)}個")
        for txt_file in txt_files:
            print(f"  - {txt_file}")
            
        # ファイル収集をテスト
        files = utils.get_file_list(ct.RAG_TOP_FOLDER_PATH, ct.SUPPORTED_EXTENSIONS)
        txt_count = len([f for f in files if f.endswith('.txt')])
        print(f"収集された.txtファイル: {txt_count}個")
        
        return True
    except Exception as e:
        print(f"✗ .txtファイル検出エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_txt_loader():
    print("\n=== .txtローダーテスト ===")
    try:
        from langchain_community.document_loaders import TextLoader
        
        # 議事録ルール.txtファイルを直接読み込みテスト
        txt_file = "./data/MTG議事録/議事録ルール.txt"
        if os.path.exists(txt_file):
            print(f"ファイル存在確認: {txt_file}")
            loader = TextLoader(txt_file, encoding="utf-8")
            documents = loader.load()
            print(f"✓ .txtファイル読み込み成功: {len(documents)}件のドキュメント")
            if documents:
                print(f"  内容プレビュー: {documents[0].page_content[:100]}...")
        else:
            print(f"✗ ファイルが見つかりません: {txt_file}")
            
        return True
    except Exception as e:
        print(f"✗ .txtローダーエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_initialize():
    print("\n=== 初期化テスト ===")
    try:
        from initialize import initialize
        print("initialize()実行中...")
        initialize()
        print("✓ 初期化成功！")
        return True
    except Exception as e:
        print(f"✗ 初期化エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== .txtファイル対応デバッグテスト開始 ===\n")
    
    success = True
    success &= test_imports()
    success &= test_txt_file_detection()
    success &= test_txt_loader()
    success &= test_initialize()
    
    print(f"\n=== テスト結果 ===")
    if success:
        print("✓ すべてのテストが成功しました！")
        print("🎉 .txtファイルがRAGに正常に組み込まれました！")
    else:
        print("✗ 一部のテストが失敗しました。")
        
    print("デバッグテスト終了")
