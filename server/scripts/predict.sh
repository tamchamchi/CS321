#!/bin/bash
echo "Đang xóa nhãn gốc ...."
python -m src.features.build_clear_label
echo "Hoàn thành"

echo "Đang dự đoán nhãn ...."
python -m src.features.build_predict_sents
echo "Hoàn thành"
