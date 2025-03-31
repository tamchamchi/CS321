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

    # Save result
    output_path = PROCESSED_DATA_DIR / "enamex_sentences.csv"
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["index", "sentences"])
        writer.writerows(result)

    print(f"ENAMEX sentences saved to {output_path}")

if __name__ == "__main__":
    build_enamex_sentences()
