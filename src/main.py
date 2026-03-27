import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx
import uuid
from typing import List
import logging
import base64

# 設定ファイルの読み込み
import tomli

with open("config.toml", "rb") as f:
    config = tomli.load(f)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

class PromptRequest(BaseModel):
    prompt: str
    image_path: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "prompts": config["prompts"]["choices"],
            "default_prompt": config["prompts"]["choices"][0],
            "endpoint": config["openai"]["endpoint"]
        }
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 一時ファイル名を作成
    file_extension = file.filename.split(".")[-1]
    temp_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # /tmpディレクトリに保存
    file_path = f"/tmp/{temp_filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    logger.info(f"Uploaded file: {file_path}")
    return {"filename": temp_filename}

@app.post("/analyze")
async def analyze_image(prompt_request: PromptRequest):
    try:
        # 画像ファイルをbase64エンコード
        image_path = f"/tmp/{prompt_request.image_path}"
        if not os.path.exists(image_path):
            return JSONResponse(status_code=404, content={"error": "Image file not found"})
        
        # ファイルの拡張子からMIMEタイプを判定
        file_extension = prompt_request.image_path.split('.')[-1].lower()
        # 対応するMIMEタイプをマッピング
        mime_types = {
            'png': 'png',
            'jpg': 'jpeg',
            'jpeg': 'jpeg',
            'bmp': 'bmp',
            'webp': 'webp'
        }
        mime_type = mime_types.get(file_extension, 'jpeg')  # デフォルトはjpeg
        
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config["openai"]["endpoint"] + "/chat/completions",
                json={
                    "model": "llava",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt_request.prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/{mime_type};base64,{encoded_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    "temperature": 0.7
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                # 解析結果と画像データを返す
                return {
                    "response": result["choices"][0]["message"]["content"],
                    "image_data": f"data:image/{mime_type};base64,{encoded_image}"
                }
            else:
                return {"error": f"OpenAI API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=server_host, port=server_port, reload=True)