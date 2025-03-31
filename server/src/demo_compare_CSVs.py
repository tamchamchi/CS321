import streamlit as st
from features.build_compare_between_CSVs import compare_tagged_sents
# Streamlit UI
st.title("So sánh nội dung tagged_sents giữa hai file CSV")

uploaded_file1 = st.file_uploader("Tải lên file CSV đầu tiên", type=["csv"])
uploaded_file2 = st.file_uploader("Tải lên file CSV thứ hai", type=["csv"])

if uploaded_file1 and uploaded_file2:
    try:
        result_df = compare_tagged_sents(uploaded_file1, uploaded_file2)
        st.write("### Kết quả so sánh (chỉ hiển thị các dòng khác nhau):")
        st.dataframe(result_df)
    except Exception as e:
        st.error(f"Lỗi: {e}")