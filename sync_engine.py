from synclogai.engine import SyncEngine

if __name__ == "__main__":
    engine = SyncEngine()
    engine.sync("work.md")
    if engine.verify("work.md"):
        print("整合性OK: MDとバイナリは同期されています。")
    else:
        print("警告: 乖離が検出されました！")
