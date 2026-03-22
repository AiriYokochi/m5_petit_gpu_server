# M5 PETIT SPEECH (piper-plus TTS server)

■ 概要
GPUミニPC上で動作する音声合成サーバー。
piper-plus のプリビルドバイナリを使い、日本語TTS（つくよみちゃん）を生成する。

FastAPI + uvicorn でHTTP APIとして提供。

---

■ 構成
m5_petit_speech/
├── src/m5_petit_speech/
│   ├── main.py
│   ├── config.py
│   ├── api/routes.py
│   └── services/piper_service.py
├── outputs/
├── .env
├── pyproject.toml

外部依存:
~/work/piper-bin/piper/   ← piper-plusバイナリ

---

■ セットアップ

## ① piper-plus (バイナリ)

cd ~/work
mkdir -p piper-bin
cd piper-bin

curl -L -o piper.tar.gz 
https://github.com/ayutaz/piper-plus/releases/latest/download/piper-linux-x64.tar.gz

tar xzf piper.tar.gz
cd piper

※ libonnxruntime のために LD_LIBRARY_PATH が必要

## ② モデルダウンロード

cd ~/work/piper-bin/piper

LD_LIBRARY_PATH=$PWD/lib ./bin/piper --download-model tsukuyomi

モデル保存先:
~/.local/share/piper/models/

## ③ Python環境

cd ~/work/m5_petit_gpu_server/m5_petit_speech

uv sync

## ④ .env 設定

HOST=0.0.0.0
PORT=8766

PIPER_BIN=/home/puchipuchi/work/piper-bin/piper/bin/piper
PIPER_LD_LIBRARY_PATH=/home/puchipuchi/work/piper-bin/piper/lib
PIPER_MODEL_PATH=/home/puchipuchi/.local/share/piper/models/tsukuyomi-chan-6lang-fp16.onnx

OUTPUT_DIR=./outputs

---

■ 起動

uv run uvicorn m5_petit_speech.main:app --host 0.0.0.0 --port 8766

---

■ API

## GET /help

使い方表示

## POST /speak

音声生成（wav返却）

curl -X POST http://127.0.0.1:8766/speak 
-H "Content-Type: application/json" 
-d '{"text":"こんにちは"}' --output out.wav

## POST /speak_summary

ファイル名だけ返す

curl -X POST http://127.0.0.1:8766/speak_summary 
-H "Content-Type: application/json" 
-d '{"text":"こんにちは"}'

---

■ systemd 化

① service 作成

sudo nano /etc/systemd/system/m5_speech.service

② 内容

[Unit]
Description=M5 Petit Speech Server
After=network.target

[Service]
User=puchipuchi
WorkingDirectory=/home/puchipuchi/work/m5_petit_gpu_server/m5_petit_speech

Environment="PYTHONUNBUFFERED=1"
Environment="LD_LIBRARY_PATH=/home/puchipuchi/work/piper-bin/piper/lib"

ExecStart=/home/puchipuchi/.local/bin/uv run uvicorn m5_petit_speech.main:app --host 0.0.0.0 --port 8766

Restart=always
RestartSec=3

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target

③ 反映

sudo systemctl daemon-reload
sudo systemctl enable m5_speech
sudo systemctl start m5_speech

④ 確認

sudo systemctl status m5_speech
journalctl -u m5_speech -f

---

■ 別PCからアクセス

Tailscale IP を使う

curl http://100.xxx.xxx.xxx:8766/help

---

■ よくあるエラー

・音が出ない
→ wavではなくエラーメッセージが保存されている
→ file out.wav で確認

・libonnxruntime.so エラー
→ LD_LIBRARY_PATH が必要

・piper が動かない
→ バイナリパス or モデルパス確認

---

■ 今後拡張

・音声認識サーバーと連携
・感情 → 音声パラメータ変化
・顔認識 → 話者変更
・リアルタイム会話

---
