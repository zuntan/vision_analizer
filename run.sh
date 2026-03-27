#!/bin/bash

# 仮想環境のセットアップ
python3 -m venv venv
. venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# アプリケーションの実行
echo "Starting vision_analizer..."
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
