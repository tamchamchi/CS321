# CS321 Annotation Tool

Công cụ hỗ trợ huấn luyện mô hình và gán nhãn dữ liệu cho bài toán xử lý ngôn ngữ tự nhiên.

---

## 📆 1. Clone repository

```bash
git clone https://github.com/tamchamchi/CS321.git
cd CS321
```

---

## ⚙️ 2. Cài đặt môi trường và dependencies

Bạn cần cài đặt các gói phụ thuộc riêng cho `server` và `client`.

### 📂 Server

```bash
cd server
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 📂 Client

```bash
cd client
npm install
cd ..
```

---

## 📁 3. Chuẩn bị dữ liệu

### Tạo thư mục chứa dữ liệu đã xử lý:

```bash
mkdir -p server/data/processed
```

### Tạo 3 file dữ liệu CSV trong `server/data/processed/` với định dạng:

#### `train.csv`

```csv
id,raw_data
1,"Câu dữ liệu huấn luyện 1"
2,"Câu dữ liệu huấn luyện 2"
...
```

#### `test.csv`

```csv
id,raw_data
1,"Câu dữ liệu kiểm thử 1"
2,"Câu dữ liệu kiểm thử 2"
...
```

#### `enamex_sentences.csv`

```csv
id,sentences
1,"Câu có thực thể cần gán nhãn 1"
2,"Câu có thực thể cần gán nhãn 2"
...
```

---

## 🚀 4. Huấn luyện mô hình

```bash
./scripts/train.sh
```

---

## 🔍 5. Dự đoán để chuẩn bị dữ liệu cho annotation tool

```bash
./scripts/predict.sh
```

Sau khi chạy, một file `predict_result.csv` sẽ được tạo trong thư mục dữ liệu. Đây là dữ liệu đầu vào cho công cụ gán nhãn.

---

## 🖥️ 6. Chạy annotation tool

### 📡 Chạy backend (FastAPI)

```bash
cd server
source .venv/bin/activate  # hoặc .venv\Scripts\activate trên Windows
uvicorn src.main:app --reload
```

### 🌐 Chạy frontend (Next.js)

Mở tab terminal mới:

```bash
cd client
npm run dev
```

---

## ✅ Hoàn tất

* Truy cập frontend ở `http://localhost:3000`
* API backend chạy ở `http://127.0.0.1:8000`

---
