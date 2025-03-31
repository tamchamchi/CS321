from src.models.predict_model import predict
from src.features.build_convert_output_of_model_to_xml import convert_to_ner_format
from src.features.build_insert_tag import insert_tags
from src.configs import PROCESSED_DATA_DIR
import pandas as pd
from tqdm import tqdm
import csv
import json

def build_predict_sents():
    # Load data an toàn với quotechar
    dataset = pd.read_csv(PROCESSED_DATA_DIR / "clear_label_id.csv")
    count = 0
    flag = 0
    index = 0
    
    result = []
    for idx, sent in tqdm(enumerate(dataset["sentences"]), desc="Predicting...", total=len(dataset)):
        if not isinstance(sent, str) or sent.strip() == "":  # Kiểm tra nếu câu rỗng
            continue

        tokens, labels = predict(sent)  # Dự đoán nhãn NER
        tags = convert_to_ner_format(tokens, labels)  # Chuyển đổi định dạng

        if len(tags.get("tags")) > 0:
            flag = 1
            count += 1

        sent_format_xml = insert_tags(tags)  # Gắn thẻ vào câu
        tags = json.dumps(tags, ensure_ascii=False, indent=2)
        
        if flag == 1:
            result.append([index, sent, sent_format_xml, tags])  # Lưu kết quả
            index += 1
            flag = 0    

    # Save result với quoting an toàn
    with open(PROCESSED_DATA_DIR / "predict_result.csv", "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # QUOTE_ALL để đảm bảo dữ liệu không bị lỗi
        writer.writerow(["id", "sentences", "xml_format", "tags"])
        writer.writerows(result)

    print(f"Predict result saved to {PROCESSED_DATA_DIR / 'predict_result.csv'}")
    print(f"Total sentences have tags: {count} sentences")

if __name__ == "__main__":
    build_predict_sents()

