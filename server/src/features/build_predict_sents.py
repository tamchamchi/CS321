from src.models.predict_model import predict
from src.features.build_convert_output_of_model_to_xml import convert_to_ner_format
from src.features.build_insert_tag import insert_tags
from src.configs import PROCESSED_DATA_DIR
import pandas as pd
from tqdm import tqdm
import csv

def build_predict_sents():
    # Load data an toàn với quotechar
    dataset = pd.read_csv(PROCESSED_DATA_DIR / "clear_label_id.csv")
    result = []
    # Predict
    for sent in tqdm(dataset["sentences"], desc="Predicting..."):
        tokens, labels = predict(sent)
        tags = convert_to_ner_format(tokens, labels)
        sent_format_xml = insert_tags(tags)
        result.append([sent, sent_format_xml, tags])

    # Save result với quoting an toàn
    with open(PROCESSED_DATA_DIR / "predict_result.csv", "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # QUOTE_ALL để đảm bảo dữ liệu không bị lỗi
        writer.writerow(["sentences", "xml_format", "tags"])
        writer.writerows(result)

    print(f"Predict result saved to {PROCESSED_DATA_DIR / 'predict_result.csv'}")

if __name__ == "__main__":
    build_predict_sents()

