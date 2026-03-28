# vision_analizer

画像をドラッグ＆ドロップすることで解析し、その内容をテキスト形式で表示するWebアプリケーションです。

## 概要

vision_analizerは、画像ファイルを簡単にアップロードし、LLMを使用して画像内容を自然言語で説明・分析するためのツールです。
複数のプロンプトを選択して、画像の概要、詳細、UI構造、テキスト内容などさまざまな視点からの解釈を得ることができます。

## 主な機能

- 画像ファイル（JPEG, PNG, BMP, WEBP）のドラッグ＆ドロップによるアップロード
- アップロードされた画像のプレビュー表示
- 複数の解析プロンプトでの画像解釈（簡易説明、詳細説明、UI構造、テキスト抽出など）
- クリップボードへの解析結果コピー機能
- 再解析とクリア機能
- クリップボードからのペースト対応

## 技術スタック

- Python + FastAPI (Uvicorn)
- htmx 
- Tailwind CSS
- Lucide Icons
- Pillow, httpx, pydantic

## インストール手順

### 必須条件
- Python 3.8以上
- pip

### セットアップ手順

```bash
# リポジトリのクローン
git clone <repository-url>
cd vision_analizer

# 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# アプリケーションの起動
./run.sh
```

または systemdサービスとして利用することも可能です:

```bash
sudo cp vision_analizer.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vision_analizer.service
sudo systemctl start vision_analizer.service
```

## 使用方法

1. ブラウザから `http://localhost:8001` にアクセスします
2. 画像ファイルをドラッグ＆ドロップするか、クリップボードからペーストしてください
3. 解析プロンプトを選択します（デフォルトは「画像を簡素に説明せよ」）
4. 解析結果がテキストエリアに表示されます
5. 「コピー」ボタンで結果をクリップボードに保存できます
6. 「再解析」や「クリア」ボタンで操作を行います

## 設定

設定ファイル `config.toml` を編集することで、以下の項目をカスタマイズできます：

- OpenAI互換エンドポイント (`[openai] endpoint`)
- システムプロンプト文言 (`[system_prompt] text`)
- プロンプト選択肢 (`[prompts] choices`)
- 行数目安 (`[prompts] planned_lines`)

## 開発者向け情報

- ソースコードは `/src/main.py` に配置されています
- フロントエンドUIは `/templates/index.html` に記述されています
- スタイルシートは `/static/style.css` に配置されています

## 依存関係

必要なライブラリは `requirements.txt` に記載されており、以下のようなものがあります：
- fastapi==0.110.0
- uvicorn[standard]==0.29.0
- jinja2==3.1.3
- tomli==2.0.1
- httpx==0.25.0
- Pillow==10.2.0
- pydantic==2.5.0
- python-multipart==0.0.6

## 注意事項

- このアプリケーションはLLM APIとの連携が必要です。デフォルトでは `http://kuro.local:8081/v1` への接続を想定しています。
- アプリケーションは `/tmp` ディレクトリに一時ファイルを作成します。

---
Powered by [unsloth/Qwen3-VL-2B-Instruct](https://huggingface.co/unsloth/Qwen3-VL-2B-Instruct)
