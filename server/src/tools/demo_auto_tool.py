import streamlit as st
import re
from server.src.tools.auto_pos_tag_tool import predict  # Hàm predict từ mô hình CRF

# Hàm tô màu theo entity
def highlight_entities(text, labels):
    """
    Tô màu các thực thể trong văn bản theo nhãn dự đoán từ CRF.
    
    text: Câu đầu vào (chuỗi)
    labels: Nhãn CRF đầu ra (list các nhãn O, B-*, I-*)
    """
    words = text.split()
    highlighted_text = ""

    entity_colors = {
        "PERSON": "#FFD700",  # Màu vàng
        "ORGANIZATION": "#FF6347",     # Màu đỏ cam
        "LOCATION": "#90EE90",     # Màu xanh lá nhạt
        "MISCELLANEOUS" : "#0000FF" # Màu xanh dương
    }

    entity = ""
    entity_type = None

    for word, label in zip(words, labels):
        if label.startswith("B-"):
            if entity:  
                highlighted_text += f'<span style="background-color: {entity_colors.get(entity_type, "#ADD8E6")}; padding: 2px 5px; border-radius: 3px;">{entity}</span> '
            entity = word
            entity_type = label.split("-")[1]
        elif label.startswith("I-") and entity:
            entity += " " + word
        else:
            if entity:
                highlighted_text += f'<span style="background-color: {entity_colors.get(entity_type, "#ADD8E6")}; padding: 2px 5px; border-radius: 3px;">{entity}</span> '
                entity = ""
            highlighted_text += word + " "

    # Thêm entity cuối cùng nếu có
    if entity:
        highlighted_text += f'<span style="background-color: {entity_colors.get(entity_type, "#ADD8E6")}; padding: 2px 5px; border-radius: 3px;">{entity}</span> '

    return highlighted_text.strip()


# Giao diện Streamlit
st.title("📝 Trực quan hóa NER với CRF")

# Ô nhập văn bản từ người dùng
user_input = st.text_area("Nhập văn bản cần nhận diện thực thể:")

if st.button("Dự đoán"):
    if user_input:
        sent_list, predicted_labels_list = predict(user_input)  # Nhận danh sách câu và nhãn

        if len(sent_list) == len(predicted_labels_list):  # Kiểm tra dữ liệu hợp lệ
            for sent, predicted_labels in zip(sent_list, predicted_labels_list):
                words = sent.split()
                if len(words) == len(predicted_labels):  # Kiểm tra số từ khớp nhãn
                    styled_text = highlight_entities(sent, predicted_labels)
                    st.markdown(f'<p style="font-size:18px;">{styled_text}</p>', unsafe_allow_html=True)
                else:
                    st.error(f"⚠️ Lỗi: Số lượng từ trong câu `{sent}` không khớp với số lượng nhãn dự đoán!")
        else:
            st.error("⚠️ Số lượng câu và nhãn dự đoán không khớp!")
    else:
        st.warning("⚠️ Vui lòng nhập văn bản để nhận diện thực thể.")
