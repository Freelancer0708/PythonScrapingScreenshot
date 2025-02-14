# Screenshot & HTML Scraper

## 使い方
1. `pip install -r backend/requirements.txt` で依存関係をインストール
2. `uvicorn backend.app:app --reload` でFastAPIを起動
3. `frontend/index.html` をブラウザで開く
4. URLを入力し「取得」を押すと、スクリーンショットとHTMLが表示される

## Dockerを使用する場合
1. `docker build -t screenshot-app .`
2. `docker run -p 8000:8000 screenshot-app`
