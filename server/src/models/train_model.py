from sklearn_crfsuite import CRF, metrics, scorers
from pathlib import Path
from src.configs import CRF_CONFIG
from src.data.make_dataset import Dataset
from src.models.extract_feature import sent2features, sent2labels
import pickle
import os


PATH_DATA_TRAIN = Path(__file__).resolve().parents[2] / "data" / "processed" 

def train_crf(X_train, y_train, config):
     crf_model = CRF(
          algorithm=config["algorithm"],
          c1=config["c1"],
          c2=config["c2"],
          max_iterations=config["max_iterations"],
          verbose=config["verbose"],
          all_possible_transitions=True
     )
     crf_model.fit(X_train, y_train)

     return crf_model

if __name__ == "__main__":
     LEN_TRAIN_DATA = 2000
     LEN_DEV_DATA = 400

     train_dataset = Dataset()
     dev_dataset = Dataset()

     train_data = train_dataset.get_data_train(PATH_DATA_TRAIN / "train.csv")
     dev_data = dev_dataset.get_data_train(PATH_DATA_TRAIN / "dev.csv")

     X_train = [sent2features(sent) for sent in train_data][:LEN_TRAIN_DATA]
     y_train = [sent2labels(sent) for sent in train_data][:LEN_TRAIN_DATA]

     X_dev = [sent2features(sent) for sent in dev_data][:LEN_DEV_DATA]
     y_dev = [sent2labels(sent) for sent in dev_data][:LEN_DEV_DATA]

     crf_model = train_crf(X_train, y_train, CRF_CONFIG)
     y_pred = crf_model.predict(X_dev)

     labels = list(crf_model.classes_)
     labels.remove('O')
     print(metrics.flat_classification_report(y_dev, y_pred, labels=labels, digits=3))
     f1_score = metrics.flat_f1_score(y_dev, y_pred, average='weighted', labels=labels)
     print(f"F1 score: {f1_score}")

     # Tạo thư mục nếu chưa tồn tại
     model_dir = os.path.dirname(CRF_CONFIG["model_path"])
     os.makedirs(model_dir, exist_ok=True)

     # Lưu model
     with open(f'{CRF_CONFIG["model_path"]}', "wb") as file:
          pickle.dump(crf_model, file)

     print(f"Saving model to: {CRF_CONFIG['model_path']}")
