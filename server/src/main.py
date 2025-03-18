from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tools.annotation_tool import insert_tags

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
def read_root():
    return {"Hello": "World"}

@app.post("/pos_tagging")
def pos_tagging(data: dict):
    print(data)
    return insert_tags(data)
