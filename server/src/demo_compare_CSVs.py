import streamlit as st
import pandas as pd

st.title("So sánh nội dung tagged_sents giữa hai file CSV")

# Tải file CSV
uploaded_file1 = st.file_uploader("Tải lên file CSV đầu tiên", type=["csv"])
uploaded_file2 = st.file_uploader("Tải lên file CSV thứ hai", type=["csv"])

if uploaded_file1 and uploaded_file2:
    try:
        # Đọc file CSV thành DataFrame
        df1 = pd.read_csv(uploaded_file1)
        df2 = pd.read_csv(uploaded_file2)

        # Kiểm tra sự tồn tại của cột 'index' và 'tagged_sents'
        if 'index' not in df1.columns or 'index' not in df2.columns:
            st.error("Lỗi: Một hoặc cả hai file không có cột 'index'.")
        elif 'tagged_sents' not in df1.columns or 'tagged_sents' not in df2.columns:
            st.error("Lỗi: Một hoặc cả hai file không có cột 'tagged_sents'.")
        else:
            # Merge dựa trên cột 'index'
            merged_df = df1[['index', 'tagged_sents']].merge(
                df2[['index', 'tagged_sents']], 
                on='index', 
                how='inner', 
                suffixes=('_file1', '_file2')
            )

            # Lọc ra những dòng có sự khác biệt trong 'tagged_sents'
            diff_df = merged_df[merged_df['tagged_sents_file1'] != merged_df['tagged_sents_file2']]

            # Hiển thị kết quả so sánh
            if not diff_df.empty:
                st.write("### Kết quả so sánh (chỉ hiển thị các dòng khác nhau):")
                st.dataframe(diff_df)
            else:
                st.success("Không có sự khác biệt trong cột 'tagged_sents' giữa hai file.")

    except Exception as e:
        st.error(f"Lỗi: {e}")
