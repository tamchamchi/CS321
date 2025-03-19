from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tools.annotation_tool import insert_tags
from tools.auto_pos_tag_tool import predict

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả domain (có thể giới hạn lại)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức (GET, POST, PUT, DELETE,...)
    allow_headers=["*"],  # Cho phép tất cả headers
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/pos_tagging")
async def pos_tagging(data: dict):
    print(data)
    return insert_tags(data)  # Gọi insert_tags bất đồng bộ nếu nó hỗ trợ async

@app.post("/auto_pos_tagging")
async def auto_pos_tagging(data: dict):
    if "text" not in data:
        return {"error": "Missing 'text' in request body."}
    if not data["text"]:
        return {"error": "Empty 'text' in request body."}

    return predict(data["text"])  # Gọi predict bất đồng bộ nếu nó hỗ trợ async
