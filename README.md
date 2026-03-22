# m5_petit_gpu_server


## 概要

m5_petit_gpu_server は、GPU付きPC上で動作する
M5 petit 向けの重い処理をまとめるためのサーバー群のリポジトリです。

このPCは常時起動用ではなく、必要なときだけ起動して、
音声処理、画像処理、顔認識、感情推定などの
計算負荷の高い処理を担当することを想定しています。

常時ONの小型PCやメイン制御PCからHTTPやTailscale経由で呼び出し、
必要な結果だけを返す構成を目指します。

想定役割:
- 音声認識
- 環境音分類
- 音声特徴量抽出
- 顔認識
- 表情推定
- カメラ画像解析
- 将来的なマルチモーダル統合

## 設計方針

1. Claude本体や会話制御は常時ONの軽量PCに置く
2. GPU PC は重い処理専用のワーカーとして使う
3. 各機能は独立したサブディレクトリで管理する
4. 各機能は単独でも起動・テストできるようにする
5. 将来的には複数の処理結果を統合するAPIも作る

## 想定構成

[常時ONのミニPC]
- Claude
- 制御ロジック
- ROS2
- ユーザーとの対話
- GPU PCへのAPIリクエスト送信

[GPU付きPC]
- m5_petit_gpu_server
- Whisper / faster-whisper
- 環境音分類
- 顔認識
- 表情推定
- 画像解析
- 音声特徴量抽出

通信方法:
- HTTP API
- Tailscale経由
- 必要に応じてROS2連携

## ディレクトリ構成（例）

m5_petit_gpu_server/
├── README.txt
├── m5_petit_voice_recognition/
├── m5_petit_face_recognition/
├── m5_petit_vision_analysis/
├── m5_petit_multimodal_analysis/
├── shared/
└── docs/

### 説明:

m5_petit_voice_recognition/
  音声認識、環境音分類、音声特徴量抽出

m5_petit_face_recognition/
  顔検出、顔認識、人物ID推定、表情分類など

m5_petit_vision_analysis/
  カメラ画像の一般解析、物体検出、姿勢推定など

m5_petit_multimodal_analysis/
  音声・画像・環境情報を統合して解釈する将来用モジュール

shared/
  複数サービスで共通利用するコード
  例:
  - 共通設定
  - 共通スキーマ
  - ログ
  - モデルローダー
  - ユーティリティ

docs/
  API仕様、設計メモ、セットアップ手順など

## 現在ある機能

現在は主に以下を実装しています。

- m5_petit_voice_recognition
  - 音声の文字起こし
  - 音声特徴量抽出
  - 環境音分類の土台
  - FastAPIによるHTTP API

主な用途:
- マイクで録音した音声の解析
- Claudeに渡すための要約生成
- 疲れや発話状態の手がかり抽出

## 今後追加したい機能

1. 顔認識
- 顔検出
- 顔の向き推定
- 登録済み人物の識別
- Unknown判定
- 顔特徴量抽出

2. 表情推定
- smiling / neutral / tired などの簡易分類
- Valence / Arousal推定の補助情報

3. 画像理解
- 物体検出
- 人の位置把握
- デスク上の状況把握
- 周囲環境の視覚的理解

4. マルチモーダル統合
- 音声 + 顔 + 環境音 + 画像情報を統合
- Claude向けの簡潔なコンテキスト生成

## 顔認識の将来イメージ

例:
- カメラ画像入力
- 顔検出
- 顔ID推定
- 表情推定
- 顔の向き推定
- Claude向け要約作成

想定出力例:

{
  "face_detected": true,
  "person_id": "user",
  "face_direction": "front",
  "expression": "neutral",
  "summary_for_claude": "ユーザーが正面を向いている。表情は落ち着いている。"
}

## マルチモーダル統合の将来イメージ

音声:
- transcript
- voice_state

画像:
- face_detected
- person_id
- expression

環境:
- sound_events
- objects

### 統合例:

{
  "transcript": "今日は少し疲れました",
  "voice_state": "slow, tired",
  "face_detected": true,
  "expression": "tired",
  "environment": "indoor, keyboard",
  "summary_for_claude": "ユーザーはやや疲れている可能性がある。室内でPC作業中。"
}

## 実装の基本ルール

- 機能ごとに独立したサブプロジェクトにする
- 各サブプロジェクトは単体で起動できるようにする
- APIは FastAPI ベースを基本とする
- モデルや重い依存は必要な機能だけに閉じ込める
- サマリーAPIと詳細APIを分ける
- Claudeに渡す情報は簡潔に要約する

## 推奨API設計

各機能では以下のように、
詳細版と要約版を分けることを推奨する。

例:

/analyze_xxx
  詳細な生データを返す

/analyze_xxx_summary
  Claude向けの簡潔な要約を返す

音声の例:
- /analyze_audio
- /analyze_audio_summary

顔認識の例:
- /analyze_face
- /analyze_face_summary

画像解析の例:
- /analyze_image
- /analyze_image_summary

運用方針

- 開発初期はCPUで動作確認
- 安定後にGPU化
- API単位で疎通確認
- 必要時だけGPU PCを起動
- Tailscale経由で他PCから利用

## Tailscale利用

このGPU PCは Tailscale に接続して、
他のPCから安全にアクセスする想定です。

例:
http://100.xxx.xxx.xxx:8765/analyze_audio

今後、顔認識や画像解析も同様に
別ポートまたは別APIで公開する想定です。

## 今後のおすすめディレクトリ追加

m5_petit_face_recognition/
  顔認識用

m5_petit_vision_analysis/
  一般画像解析用

shared/
  共通コード用

docs/
  設計・手順書用

開発の進め方のおすすめ

1. まず音声認識を安定化
2. 環境音分類を本実装化
3. 顔認識用サブディレクトリ作成
4. 画像処理API追加
5. マルチモーダル統合API追加
6. Claude連携を強化
7. ROS2との接続を整理

## 備考

このリポジトリは、M5 petit や関連ロボットのための
GPU処理バックエンドとして使うことを想定している。

目的は、重い処理をGPU PCに分離しつつ、
常時ONの軽量PCから柔軟に利用できるようにすること。

単なる推論サーバーではなく、
最終的には「人の状態や周囲状況を理解するための
マルチモーダル認識基盤」に育てることを目指す。