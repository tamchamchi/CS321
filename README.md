# 🏷️ Công Cụ Gán Nhãn NER Cho Tiếng Việt

Công cụ hỗ trợ huấn luyện mô hình và gán nhãn dữ liệu cho bài toán Nhận diện Thực thể Tên (Named Entity Recognition - NER) trong tiếng Việt.

---

## 📁 1. Clone Repository

```bash
git clone https://github.com/tamchamchi/CS321.git
cd CS321
```

---

## ⚙️ 2. Cài Đặt Môi Trường và Phụ Thuộc

Bạn cần cài đặt các gói phụ thuộc riêng cho hai thành phần: `server` và `client`.

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

## 🛠️ 3. Cài Đặt và Sử Dụng Preprocessing Tool

### 📌 Bước 1: Chuẩn Bị Dữ Liệu

Tạo thư mục chứa dữ liệu đã xử lý:

```bash
mkdir -p server/data/processed
```

Tạo ba tệp CSV trong thư mục `server/data/processed/` với định dạng như sau:

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

### 🚀 Bước 2: Huấn Luyện Mô Hình

```bash
./scripts/train.sh
```

### 🔍 Bước 3: Dự Đoán Dữ Liệu Cho Công Cụ Gán Nhãn

```bash
./scripts/predict.sh
```

File kết quả `predict_result.csv` sẽ được tạo tại `server/data/processed/`. Đây là dữ liệu đầu vào cho công cụ gán nhãn.

---

## 🖍️ 4. Hướng Dẫn Sử Dụng Annotation Tool

Annotation Tool cung cấp giao diện trực quan để người dùng thực hiện gán nhãn thực thể cho câu văn, dựa trên kết quả dự đoán từ mô hình.

### 📥 Bước 1: Chuẩn Bị Dữ Liệu Gán Nhãn

Chạy lệnh dự đoán:

```bash
./scripts/predict.sh
```

File `predict_result.csv` sẽ được tạo tại:

```
server/data/processed/predict_result.csv
```

### ⚙️ Bước 2: Khởi Động Hệ Thống

#### ✅ Backend (FastAPI)

```bash
cd server
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
uvicorn src.main:app --reload
```

#### 🌐 Frontend (ReactJS)

Mở một terminal mới:

```bash
cd client
npm run dev
```

### 🔗 Bước 3: Truy Cập Giao Diện Gán Nhãn

* Truy cập: [http://localhost:5173/](http://localhost:5173/)
* Giao diện sẽ hiển thị danh sách câu cần gán nhãn cùng với gợi ý từ mô hình.

### ✍️ Bước 4: Thực Hiện Gán Nhãn

* **Bước 1**: Import file `predict_result.csv` bằng nút "Choose File".
  ![Import dữ liệu](./assets/image_01.png)

* **Bước 2**: Chọn câu cần gán nhãn.
  ![Chọn câu](./assets/image_02.png)

* **Bước 3**: Gán nhãn thực thể qua 4 bước:

  1. Bôi đen thực thể trong câu.
  2. Chọn loại nhãn thực thể.
  3. Nhấn **Gán nhãn & Gửi**.
  4. Nhấn **Lưu tạm thời**.

  ![Gán nhãn](./assets/image_03.png)

### 💾 Bước 5: Xuất Kết Quả

Khi hoàn thành, bấm nút **Tải xuống CSV** để lưu kết quả gán nhãn. Dữ liệu có thể được lưu dưới dạng `annotated_data.json` hoặc CSV tùy chỉnh.
![Xuất kết quả](./assets/image_04.png)

---

## ✅ 5. Hoàn Tất

* Truy cập frontend tại: [http://localhost:5173](http://localhost:5173)
* Backend API hoạt động tại: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---
