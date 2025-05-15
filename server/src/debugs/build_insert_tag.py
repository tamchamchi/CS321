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
        """Đệ quy chuyển đổi cây thành văn bản có tag"""
        tagged_text = self.text
        # Sắp xếp con theo start giảm dần để không bị lệch vị trí khi chèn tag
        for child in sorted(self.children, key=lambda x: x.start, reverse=True):
            start_rel = child.start - self.start
            end_rel = child.end - self.start
            tagged_text = (
                tagged_text[:start_rel]
                + child.to_tagged_text()
                + tagged_text[end_rel:]
            )

        if self.ner == "ROOT":
            return tagged_text
        return f'<ENAMEX TYPE="{self.ner}">{tagged_text}</ENAMEX>'


def build_tree(tags, text):
    """Xây dựng cây thực thể dựa trên danh sách tag"""
    # Sắp xếp theo start tăng dần, end giảm dần để tag bao ngoài đứng trước
    tags = sorted(tags, key=lambda x: (x["start"], -x["end"]))
    root = Node(0, len(text), "ROOT", text)

    stack = [root]
    for tag in tags:
        node = Node(tag["start"], tag["end"], tag["ner"], text)
        # Tìm cha bao trùm node hiện tại
        while stack and not (stack[-1].start <= node.start and node.end <= stack[-1].end):
            stack.pop()
        stack[-1].add_child(node)
        stack.append(node)

    return root


def insert_tags(data):
    text = data.get("text", "").strip()
    tags = data.get("tags", [])
    tree = build_tree(tags, text)
    return tree.to_tagged_text()


if __name__ == "__main__":
    data = {
        "text": "Tuy vậy, cựu cầu thủ Chicago Bulls vẫn chưa đủ điều kiện để có thể ra sân ở trận đấu này.",
        "tags": [
            {"start": 21, "end": 34, "ner": "ORGANIZATION"},
            {"start": 21, "end": 28, "ner": "LOCATION"},
        ]
    }

    print(insert_tags(data))
