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
   #  dataset = pd.read_csv(PROCESSED_DATA_DIR / "clear_label_id.csv")
   

    dataset = pd.read_csv(r"D:\HK6\CS321_NNHNL\clear_label.csv")
    
    result = []
    for idx, sent in tqdm(enumerate(dataset["sentences"]), desc="Predicting...", total=len(dataset)):
        if not isinstance(sent, str) or sent.strip() == "":  # Kiểm tra nếu câu rỗng
            continue

        tokens, labels = predict(sent)  # Dự đoán nhãn NER
        print(tokens, labels)
        tags = convert_to_ner_format(tokens, labels)  # Chuyển đổi định dạng

        sent_format_xml = insert_tags(tags)  # Gắn thẻ vào câu
        tags = json.dumps(tags, ensure_ascii=False, indent=2)
        result.append([idx, sent, sent_format_xml, tags])  # Lưu kết quả
 

    # Save result với quoting an toàn
    with open(r"D:\HK6\CS321_NNHNL\predict.csv", "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # QUOTE_ALL để đảm bảo dữ liệu không bị lỗi
        writer.writerow(["id", "sentences", "xml_format", "tags"])
        writer.writerows(result)

    print(f"Predict result saved to predict.csv'")

if __name__ == "__main__":
    build_predict_sents()

