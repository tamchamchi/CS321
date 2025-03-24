class Node:
    def __init__(self, start, end, ner, text):
        self.start = start
        self.end = end
        self.ner = ner
        self.text = text[start:end]
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def to_tagged_text(self):
        """ Đệ quy chuyển đổi cây thành văn bản có tag """
        tagged_text = self.text
        for child in sorted(self.children, key=lambda x: x.start, reverse=True):
            tagged_text = (tagged_text[:child.start - self.start] + 
                           child.to_tagged_text() + 
                           tagged_text[child.end - self.start:])
            
        # Nếu là ROOT, chỉ lấy nội dung bên trong, không bọc thẻ
        if self.ner == "ROOT":
            return tagged_text
        
        return f'<ENAMEX TYPE="{self.ner}">{tagged_text}</ENAMEX>'

def build_tree(tags, text):
    """ Xây dựng cây thực thể dựa trên danh sách tag """
    tags = sorted(tags, key=lambda x: x["start"])  # Sắp xếp theo start
    root = Node(0, len(text), "ROOT", text)  # Gốc bao toàn bộ văn bản

    stack = [root]  # Stack để theo dõi cấp cha hiện tại
    for tag in tags:
        node = Node(tag["start"], tag["end"], tag["ner"], text)
        while stack and (stack[-1].end <= node.start):  # Lùi lại nếu node không thuộc cha hiện tại
            stack.pop()
        stack[-1].add_child(node)
        stack.append(node)

    return root

def insert_tags(data):
    text = data.get("text", "").strip()
    tags = data.get("tags", [])

    # Kiểm tra nếu text hoặc tags rỗng
    if not text or not tags:
        return "Không có dữ liệu để xử lý!"

    tree = build_tree(tags, text)
    return tree.to_tagged_text()

if __name__ == "__main__":
    data = {
        "text": "Trường Đại học, Bách Khoa Hà Nội",
        "tags": [
            {"start": 16, "end": 36, "ner": "ORG"},
            {"start": 26, "end": 36, "ner": "LOC"},
        ]
    }

    print(insert_tags(data))
