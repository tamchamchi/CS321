def convert_to_ner_format(words, tags):
    text = "".join([w if w in ",.:;!?" else " " + w for w in words]).strip()  # Ghép từ, xử lý dấu câu
    entities = []
    start, end = -1, -1
    current_entity = ""
    inside_entity = False
    
    offset = 0  # Vị trí ký tự hiện tại trong chuỗi
    for i, (word, tag) in enumerate(zip(words, tags)):
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
     words = ['Trường', 'Đại', 'học', ',', 'Đại', 'Bách', 'Khoa', 'Hà', 'Nội']
     tags = ['O', 'B-PERSON', 'O', 'O', 'B-LOCATION', 'I-LOCATION', 'I-LOCATION', 'I-LOCATION', 'I-LOCATION']
     result = convert_to_ner_format(words, tags)
     print(result)