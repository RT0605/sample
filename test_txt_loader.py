from constants import safe_text_loader

if __name__ == "__main__":
    path = "./data/MTG議事録/議事録ルール.txt"
    loader = safe_text_loader(path)
    docs = loader.load()
    print("読み込み成功:", len(docs), "件")
    print("内容プレビュー:", docs[0].page_content[:100])
