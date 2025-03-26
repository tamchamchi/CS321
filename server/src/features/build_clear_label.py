from underthesea import sent_tokenize
from src.configs import PROCESSED_DATA_DIR
import re
import pandas as pd
import csv
from tqdm import tqdm

def clean_enamex_tags(text, count=0):
    l_split = sent_tokenize(text)
    clear_ = []

    for l in l_split:
        if l.strip() == "":  # Kiểm tra chuỗi rỗng
            continue

        line = re.sub(r'\s+', ' ', l)  # Chuẩn hóa khoảng trắng
        line = re.sub(r'(<ENAMEX TYPE="[^"]+">)([^<]+)(<ENAMEX)', r'\1\2 \3', line)  # Đảm bảo cách khoảng

        # Xóa tất cả thẻ <ENAMEX> một lần thay vì dùng while
        while re.search(r'<ENAMEX TYPE="[^"]+">(.+?)</ENAMEX>', line):
            line = re.sub(r'<ENAMEX TYPE="[^"]+">(.+?)</ENAMEX>', r'\1', line)

        # Thêm bước loại bỏ khoảng trắng dư thừa sau khi xử lý ENAMEX
        line = re.sub(r'\s+', ' ', line).strip()

        count += 1
        clear_.append([count, line])

    return count, clear_

def build_clear_label():
    # Load data
    dataset = pd.read_csv(PROCESSED_DATA_DIR / "test.csv")

    result = []
    id = 0
    for data in tqdm(dataset["raw_data"], desc="Cleaning..."):
        count, clear_label = clean_enamex_tags(data, id)
        id = count
        result += clear_label

    # Save result
    with open(PROCESSED_DATA_DIR / "clear_label_id.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "sentences"])
        writer.writerows(result)

    print(f"Clear label saved to {PROCESSED_DATA_DIR / 'clear_label_id.csv'}")

if __name__ == "__main__":
    build_clear_label()
