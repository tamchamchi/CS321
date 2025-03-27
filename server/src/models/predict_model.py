import os
from pathlib import Path
import pickle
from nltk.tokenize import sent_tokenize, word_tokenize
from src.models.extract_feature import sent2features
from src.configs import MODEL_DIR
from src.data.make_dataset import Dataset

CRF_MODEL = None

def predict(sents):
    global CRF_MODEL
    if CRF_MODEL is None:
        with open(f"{MODEL_DIR}\\crf_model.pkl", "rb") as f:
            CRF_MODEL = pickle.load(f)

    sents = sent_tokenize(sents)
    sents_to_conll = [Dataset.convert_sent_to_conll(sent) for sent in sents]
    sents_to_features = [sent2features(sent) for sent in sents_to_conll]

    return word_tokenize(sents[0]), CRF_MODEL.predict(sents_to_features).tolist()[0]
    
if __name__ == "__main__":
    print(predict("Trường Đại học, Đại Bách Khoa Hà Nội"))