import pandas as pd
import csv
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from src.configs import PROCESSED_DATA_DIR, RAW_DATA_DIR
from tqdm import tqdm

class Dataset:
     def __init__(self):
          self.data = []

     def load_data(self, path):
          data = []
          try:
               file_list = list(path.rglob("*.muc")) + list(path.rglob("*.txt"))
               for index, file_path in enumerate(tqdm(file_list, desc="Loading files", unit="file")):
                    with open(file_path, "r", encoding="utf-8") as file:
                         raw_data = file.read()
                    data.append([index, file_path, raw_data])
               self.data = data.copy()
          except Exception as e:
               print(f"Error reading file {file_path}: {e}")

          return pd.DataFrame(data, columns=["id", "path", "raw_data"]) 
     
     def save_data(self, src_path):
          try:
               with open(src_path, "w", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["id", "path", "raw_data"])
                    writer.writerows(self.data)
               print(f"Data saved to {src_path}")
          except Exception as e:
               print(f"Error writing file {src_path}: {e}")

     @staticmethod
     def convert_sent_to_conll(sent):
          soup = BeautifulSoup(sent, "html.parser")
          tokens_with_tags = []
          
          for ele in soup.find_all(string=True):
               if ele.strip() == "":
                    continue

               parent = ele.parent
               entity_type = parent.get("type")
               tokens = word_tokenize(ele.strip())

               if entity_type:
                    tokens_with_tags.append((tokens[0], f"B-{entity_type}"))
                    tokens_with_tags.extend([(token, f"I-{entity_type}") for token in tokens[1:]])
               else:
                    tokens_with_tags.extend([(token, "O") for token in tokens])
          
          return tokens_with_tags
     
     def get_data_train(self, path_csv):
          raw_data = pd.read_csv(path_csv)

          train_data = []
          for data in raw_data["raw_data"]:
               sentences = sent_tokenize(data)
               sentences_conll = [self.convert_sent_to_conll(sent) for sent in sentences]
               train_data += sentences_conll
          
          return train_data
     

if __name__ == "__main__":
     dataset_train = Dataset()
     dataset_train.load_data(RAW_DATA_DIR / "nervlsp2018" / "VLSP2018-NER-train" / "VLSP2018-NER-train-Jan14")
     dataset_train.save_data(PROCESSED_DATA_DIR /"train.csv")

     dataset_test = Dataset()
     dataset_test.load_data(RAW_DATA_DIR / "nervlsp2018" / "VLSP2018-NER-Test-Domains" / "VLSP2018-NER-Test-Domains")
     dataset_test.save_data(PROCESSED_DATA_DIR /"test.csv")

     dataset_dev = Dataset()
     dataset_dev.load_data(RAW_DATA_DIR / "nervlsp2018" / "VLSP2018-NER-dev" / "VLSP2018-NER-dev")
     dataset_dev.save_data(PROCESSED_DATA_DIR /"dev.csv")