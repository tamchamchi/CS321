def merge_words(words):
    """Ghép danh sách từ thành câu, xử lý dấu câu, dấu ngoặc và dấu nháy hợp lý."""
    opening_brackets = {"(", "{", "[", "“", "‘"}
    closing_brackets = {")", "}", "]", "”", "’"}
    punctuation_marks = {",", ".", "?", "!"}
    
    result = []
    inside_quotes = False  # Trạng thái của dấu ' và "
    last_token = ""  # Theo dõi từ hoặc dấu trước đó

    for i, w in enumerate(words):
        if w in {"'", '"'}:  # Xử lý dấu ' và "
            if inside_quotes:
                result.append(w)  # Nếu là dấu đóng, nối trực tiếp
                if i + 1 < len(words) and words[i + 1] not in closing_brackets | punctuation_marks:  
                    result.append(" ")  # Thêm khoảng trắng sau dấu đóng nếu từ tiếp theo không phải dấu câu
            else:
                if result and last_token not in opening_brackets | {"'", '"'}:
                    result.append(" ")  # Thêm khoảng trắng trước dấu mở nếu cần
                result.append(w)  # Thêm dấu mở
            inside_quotes = not inside_quotes  # Đảo trạng thái dấu nháy

        elif w in opening_brackets:  # Xử lý dấu mở (, {, [, “, ‘
            if result and last_token not in opening_brackets | {"'", '"'}:
                result.append(" ")  # Thêm khoảng trắng trước dấu mở nếu cần
            result.append(w)  # Thêm dấu mở

        elif w in closing_brackets:  # Xử lý dấu đóng ), }, ], ”, ’
            result.append(w)  # Nối trực tiếp dấu đóng

        elif w in punctuation_marks:  # Xử lý dấu câu ,.!?
            while result and result[-1] == " ":
                result.pop()  # Xóa khoảng trắng dư trước dấu câu
            result.append(w)  # Thêm dấu câu (không có khoảng trắng trước nó)

        else:  # Xử lý từ bình thường
            if result and last_token not in opening_brackets | {"'", '"'}:
                if not (last_token in {"'", '"'} and inside_quotes):  # Đảm bảo không có khoảng trắng giữa "tam" và anh
                    result.append(" ")
            result.append(w)

        last_token = w  # Cập nhật từ hoặc dấu vừa xử lý

    return "".join(result)  # Ghép các phần tử trong list thành chuỗi hoàn chỉnh

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
    # words = ['Trường', 'Đại', 'học', '(', 'Đại', 'Bách', 'Khoa', 'Hà', 'Nội', ')']
    # tags = ['O', 'B-PERSON', 'O', 'O', 'B-LOCATION', 'I-LOCATION', 'I-LOCATION', 'I-LOCATION', 'I-LOCATION', 'O']
    words = ['\ufeffCông', 'nghệ', 'học', 'máy', 'Machine', 'learning', "'lên", 'ngôi', "'", 'trong', 'năm', '2018', 'Học', 'máy', '(', 'machine', 'learning', ')', 'sẽ', 'là', 'công', 'nghệ', 'định', 'hình', 'năm', '2018', ',', 'góp', 'phần', 'thay', 'đổi', 'lối', 'sống', 'và', 'làm', 'việc', 'của', 'con', 'người', 'hơn', 'bất', 'cứ', 'công', 'nghệ', 'nào', ',', 'kể', 'từ', 'khi', 'Internet', 'ra', 'đời', '.']
    tags = ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    result = convert_to_ner_format(words, tags)
    print(result)
    # Kết quả mong muốn: {'text': 'Trường Đại học (Đại Bách Khoa Hà Nội)', 'tags': [{'start': 16, 'end': 36, 'ner': 'LOCATION'}]}