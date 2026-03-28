#!/bin/bash

# アプリケーションの実行
echo "Starting vision_analizer..."
cd /opt3/ollama/vision_analizer
. venv/bin/activate
exec uvicorn src.main:app --host 0.0.0.0 --port 8001
