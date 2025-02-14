from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import base64

# 環境変数を読み込む
load_dotenv()

# 認証情報を環境変数から取得
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")

app = FastAPI()

# CORS（クロスオリジン制約を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ベーシック認証の Middleware を追加
@app.middleware("http")
async def basic_auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/screenshots") or request.url.path == "/favicon.ico":
        return await call_next(request)  # 画像取得時やfaviconは認証不要
    
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Basic "):
        return Response(
            headers={"WWW-Authenticate": "Basic"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Unauthorized",
        )

    # 認証情報のデコード
    auth_decoded = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8")
    username, password = auth_decoded.split(":")

    if username != BASIC_AUTH_USERNAME or password != BASIC_AUTH_PASSWORD:
        return Response(
            headers={"WWW-Authenticate": "Basic"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Unauthorized",
        )

    return await call_next(request)

# スクリーンショット保存フォルダ
SCREENSHOT_FOLDER = "screenshots"
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

# スクリーンショットの静的ファイルサーバー
app.mount("/screenshots", StaticFiles(directory=SCREENSHOT_FOLDER), name="screenshots")
