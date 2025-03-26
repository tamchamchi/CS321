def merge_words(words):
    """Ghép danh sách từ thành câu, xử lý dấu câu và dấu ngoặc hợp lý."""
    text = ""
    for i, w in enumerate(words):
        if i > 0 and words[i - 1] not in "({[\"'":
            text += " "  # Chỉ thêm khoảng trắng nếu từ trước đó không phải dấu mở ngoặc
        if w in ",.!?;:)":
            text = text.strip()
        text += w
    return text.strip()  # Loại bỏ khoảng trắng dư thừa đầu/cuối chuỗi

def convert_to_ner_format(words, tags):
    """Chuyển danh sách từ và nhãn thành định dạng NER với vị trí thực thể."""
    text = merge_words(words)  # Ghép câu từ danh sách words
    entities = []
    start, end = -1, -1
    current_entity = ""
    inside_entity = False
    
    offset = 0  # Vị trí ký tự hiện tại trong chuỗi
    for word, tag in zip(words, tags):
        word_start = text.find(word, offset)
        word_end = word_start + len(word)
        offset = word_end  # Cập nhật vị trí offset mới
        
        if tag.startswith("B-"):
            if inside_entity:
                entities.append({"start": start, "end": end, "ner": current_entity})
            start = word_start
            end = word_end
            current_entity = tag.split("-")[1]
            inside_entity = True
        elif tag.startswith("I-") and inside_entity:
            end = word_end
        else:
            if inside_entity:
                entities.append({"start": start, "end": end, "ner": current_entity})
            inside_entity = False
    
    if inside_entity:
        entities.append({"start": start, "end": end, "ner": current_entity})
    
    return {"text": text, "tags": entities}

if __name__ == "__main__":
    # Test
    words = ['Trường', 'Đại', 'học', '(', 'Đại', 'Bách', 'Khoa', 'Hà', 'Nội', ')']
    tags = ['O', 'B-PERSON', 'O', 'O', 'B-LOCATION', 'I-LOCATION', 'I-LOCATION', 'I-LOCATION', 'I-LOCATION', 'O']
    result = convert_to_ner_format(words, tags)
    print(result)
    # Kết quả mong muốn: {'text': 'Trường Đại học (Đại Bách Khoa Hà Nội)', 'tags': [{'start': 16, 'end': 36, 'ner': 'LOCATION'}]}