const HighlightText = ({ text, handleSelection }) => (
   <div
      style={{
       minHeight: "30px",
       fontSize: "18px",
       border: "1px solid #ddd",
       padding: "10px",
       marginTop: "10px",
       whiteSpace: "pre-wrap", // Giữ xuống dòng với đoạn văn bản dài
       wordWrap: "break-word", // Ngắt từ để nằm gọn trong ô
       overflowWrap: "break-word", // Ngắt từ khi không có khoảng trắng
       boxSizing: "border-box", // Đảm bảo padding và border không làm thay đổi kích thước của ô
       cursor: "text"
     }}
     onMouseUp={handleSelection}
   >
      {text}
   </div>
 );
 
 export default HighlightText;
 