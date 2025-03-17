from bs4 import BeautifulSoup
import os
from pathlib import Path
import pickle
from underthesea import sent_tokenize

def convert_to_conll(text):
    """
    Chuyển đổi văn bản HTML thành định dạng CoNLL với các nhãn thực thể.

    Args:
        text (str): Văn bản HTML chứa các thực thể có thẻ bao quanh.

    Returns:
        list: Danh sách các tuple (token, label) theo định dạng CoNLL.
    """
    # Phân tích cú pháp HTML
    soup = BeautifulSoup(text, "html.parser")
    tokens_with_labels = []  # Danh sách lưu các từ và nhãn của chúng

    # Duyệt qua tất cả các phần tử văn bản trong HTML
    for elem in soup.find_all(string=True):  
        if elem.strip() == "":  # Bỏ qua chuỗi rỗng hoặc chỉ chứa khoảng trắng
            continue
        
        parent = elem.parent  # Lấy thẻ cha bao quanh văn bản
        entity_type = parent.get("type")  # Lấy loại thực thể nếu có
        
        words = elem.strip().split()  # Tách văn bản thành danh sách từ

        if entity_type:  # Nếu từ nằm trong một thực thể có gán nhãn
            # Gán nhãn B- (Begin) cho từ đầu tiên của thực thể
            tokens_with_labels.append((words[0], f"B-{entity_type}"))  
            # Gán nhãn I- (Inside) cho các từ còn lại trong thực thể
            for word in words[1:]:  
                tokens_with_labels.append((word, f"I-{entity_type}"))  
        else:
            # Nếu từ không thuộc thực thể nào, gán nhãn "O" (Outside)
            for word in words:  
                tokens_with_labels.append((word, "O"))  
    
    return tokens_with_labels

#https://sklearn-crfsuite.readthedocs.io/en/latest/tutorial.html
def word2features(sent, i):
    """
    Trích xuất đặc trưng (feature) cho từ tại vị trí i trong câu.
    
    Args:
        sent (list of tuples): Danh sách chứa các tuple (từ, nhãn).
        i (int): Vị trí của từ trong câu.

    Returns:
        dict: Dictionary chứa các đặc trưng của từ.
    """
    word = sent[i][0]  # Lấy từ tại vị trí i
    
    # Khởi tạo dictionary chứa các đặc trưng
    features = {
        'bias': 1.0,                  # Thêm bias để mô hình có thể học trọng số
        'word.lower()': word.lower(),  # Chuyển từ thành chữ thường
        'word[-3:]': word[-3:],        # 3 ký tự cuối của từ
        'word[-2:]': word[-2:],        # 2 ký tự cuối của từ
        'word.isupper()': word.isupper(),  # Từ có viết hoa hoàn toàn không?
        'word.istitle()': word.istitle(),  # Từ có viết hoa chữ cái đầu tiên không?
        'word.isdigit()': word.isdigit(),  # Từ có phải là số không?
    }

    # Đặc trưng của từ trước đó (nếu có)
    if i > 0:
        word1 = sent[i-1][0]  # Lấy từ trước đó
        features.update({
            '-1:word.lower()': word1.lower(),  # Chữ thường của từ trước
            '-1:word.istitle()': word1.istitle(),  # Từ trước có viết hoa đầu không?
            '-1:word.isupper()': word1.isupper(),  # Từ trước có viết hoa toàn bộ không?
        })
    else:
        features['BOS'] = True  # Nếu là từ đầu tiên trong câu -> đánh dấu là "BOS" (Beginning of Sentence)

    # Đặc trưng của từ tiếp theo (nếu có)
    if i < len(sent) - 1:
        word1 = sent[i+1][0]  # Lấy từ tiếp theo
        features.update({
            '+1:word.lower()': word1.lower(),  # Chữ thường của từ tiếp theo
            '+1:word.istitle()': word1.istitle(),  # Từ tiếp theo có viết hoa đầu không?
            '+1:word.isupper()': word1.isupper(),  # Từ tiếp theo có viết hoa toàn bộ không?
        })
    else:
        features['EOS'] = True  # Nếu là từ cuối cùng trong câu -> đánh dấu là "EOS" (End of Sentence)

    return features


def sent2features(sent):
    """
    Chuyển đổi toàn bộ câu thành danh sách các đặc trưng cho từng từ.
    
    Args:
        sent (list of tuples): Danh sách chứa các tuple (từ, nhãn).

    Returns:
        list: Danh sách các dictionary chứa đặc trưng của từng từ trong câu.
    """
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    """
    Trích xuất danh sách nhãn từ câu.
    
    Args:
        sent (list of tuples): Danh sách chứa các tuple (từ, nhãn).

    Returns:
        list: Danh sách nhãn của từng từ trong câu.
    """
    return [label for token, label in sent]


def sent2tokens(sent):
    """
    Trích xuất danh sách các từ từ câu.
    
    Args:
        sent (list of tuples): Danh sách chứa các tuple (từ, nhãn).

    Returns:
        list: Danh sách từ trong câu.
    """
    return [token for token, label in sent]

def predict(sents):
    with open("crf_model.pkl", "rb") as f:
        crf_model = pickle.load(f)

    sents = sent_tokenize(sents)
    sents_to_conll = [convert_to_conll(sent) for sent in sents]
    sents_to_features = [sent2features(sent) for sent in sents_to_conll]

    return sents, crf_model.predict(sents_to_features)
    
if __name__ == "__main__":
    print(predict("con cháu của Bà Trưng, Bà Triệu."))