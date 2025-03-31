import pandas as pd

def compare_tagged_sents(file1, file2):
    # Đọc dữ liệu từ CSV
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Kiểm tra xem cột 'tagged_sents' có tồn tại không
    if 'tagged_sents' not in df1.columns or 'tagged_sents' not in df2.columns:
        raise ValueError("Cột 'tagged_sents' không tồn tại trong một hoặc cả hai tệp CSV.")
    
    # Tạo DataFrame để so sánh
    df_comparison = pd.DataFrame({'File 1': df1['tagged_sents'], 'File 2': df2['tagged_sents']})
    
    # Lọc ra các dòng khác nhau
    df_comparison = df_comparison[df_comparison['File 1'] != df_comparison['File 2']]
    
    return df_comparison