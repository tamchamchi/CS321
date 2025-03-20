from sklearn_crfsuite import CRF

class CRF_Model:
    def __init__(self, **kwargs):
        """
        Khởi tạo mô hình CRF với các siêu tham số tùy chỉnh.
        Nếu không truyền tham số, mô hình sẽ sử dụng giá trị mặc định.
        """
        self.model = CRF(**kwargs)

    def train(self, X_train, y_train):
        """Huấn luyện mô hình với dữ liệu đầu vào."""
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        """Dự đoán nhãn cho dữ liệu đầu vào."""
        return self.model.predict(X_test)
