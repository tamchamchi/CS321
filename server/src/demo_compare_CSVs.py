import streamlit as st
import pandas as pd

st.title("So sánh nội dung tagged_sents giữa ba file CSV")

# Tải lên ba file CSV
uploaded_file1 = st.file_uploader("Tải lên file CSV đầu tiên", type=["csv"])
uploaded_file2 = st.file_uploader("Tải lên file CSV thứ hai", type=["csv"])
uploaded_file3 = st.file_uploader("Tải lên file CSV thứ ba", type=["csv"])

if uploaded_file1 and uploaded_file2 and uploaded_file3:
    try:
        # Đọc các file thành DataFrame
        df1 = pd.read_csv(uploaded_file1)
        df2 = pd.read_csv(uploaded_file2)
        df3 = pd.read_csv(uploaded_file3)

        # Kiểm tra sự tồn tại của cột cần thiết
        required_columns = ['index', 'tagged_sents']
        for i, df in enumerate([df1, df2, df3], start=1):
            if not all(col in df.columns for col in required_columns):
                st.error(f"Lỗi: File thứ {i} không có đầy đủ cột 'index' và 'tagged_sents'.")
                st.stop()

        # Gộp 3 dataframe theo cột 'index'
        merged_df = df1[['index', 'tagged_sents']].rename(columns={'tagged_sents': 'tagged_sents_file1'}) \
            .merge(df2[['index', 'tagged_sents']].rename(columns={'tagged_sents': 'tagged_sents_file2'}),
                   on='index', how='inner') \
            .merge(df3[['index', 'tagged_sents']].rename(columns={'tagged_sents': 'tagged_sents_file3'}),
                   on='index', how='inner')

        # # So sánh 3 cột và lọc ra những dòng khác nhau
        # diff_df = merged_df[
        #     (merged_df['tagged_sents_file1'] != merged_df['tagged_sents_file2']) |
        #     (merged_df['tagged_sents_file1'] != merged_df['tagged_sents_file3']) |
        #     (merged_df['tagged_sents_file2'] != merged_df['tagged_sents_file3'])
        # ]

        # Hiển thị kết quả
        if not merged_df.empty:
            st.write("### Kết quả so sánh (các dòng khác nhau giữa 3 file):")
            st.dataframe(merged_df)
        else:
            st.success("Không có sự khác biệt trong cột 'tagged_sents' giữa ba file.")

    except Exception as e:
        st.error(f"Lỗi xảy ra: {e}")
