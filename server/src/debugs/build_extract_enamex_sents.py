from underthesea import sent_tokenize
from src.configs import PROCESSED_DATA_DIR
import pandas as pd
import csv
from tqdm import tqdm

def extract_enamex_sentences(text, count=0):
    l_split = sent_tokenize(text)
    extracted = []

    for l in l_split:
        if "</ENAMEX>" in l:  # Chỉ giữ lại câu có chứa </ENAMEX>
            count += 1
            extracted.append([count, l.strip()])

    return count, extracted

def build_enamex_sentences():
    # Load data
    dataset = pd.read_csv(PROCESSED_DATA_DIR / "test.csv")

    result = []
    id = 0
    for data in tqdm(dataset["raw_data"], desc="Extracting ENAMEX Sentences..."):
        count, extracted_sentences = extract_enamex_sentences(data, id)
        id = count
        result += extracted_sentences

    # Chuyển kết quả thành DataFrame
    df_result = pd.DataFrame(result, columns=["id", "sentences"])

    # Trộn các hàng ngẫu nhiên
    df_result = df_result.sample(frac=1, random_state=42).reset_index(drop=True)

    # Cập nhật lại chỉ mục theo thứ tự từ 1
    df_result["id"] = range(0, len(df_result))

    # Lưu kết quả vào file CSV
    df_result.to_csv(PROCESSED_DATA_DIR / "enamex_sentences.csv", index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)

    print(f"ENAMEX sentences saved to {PROCESSED_DATA_DIR / 'enamex_sentences.csv'}")

if __name__ == "__main__":
    build_enamex_sentences()
