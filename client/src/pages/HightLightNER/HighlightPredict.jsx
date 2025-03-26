const HighlightPredict = ({ text, tags, getColor }) => {
   // Hàm này sẽ tạo ra đoạn text có highlight dựa trên tags
   const renderHighlightedText = () => {
     const highlightedText = [];
     let currentIndex = 0;
 
     // Duyệt qua danh sách các tag
     tags.forEach(tag => {
       const { start, end, ner } = tag;
 
       // Thêm phần không có highlight từ currentIndex đến vị trí start
       if (currentIndex < start) {
         highlightedText.push(
           <span key={currentIndex}>{text.slice(currentIndex, start)}</span>
         );
       }
 
       // Thêm phần có highlight từ start đến end
       highlightedText.push(
         <span
           key={start}
           style={{
             backgroundColor: getColor(ner),
             color: "#fff", // Màu chữ trắng cho dễ đọc
             padding: "2px 4px",
             borderRadius: "4px",
           }}
         >
           {text.slice(start, end)}
         </span>
       );
 
       // Cập nhật currentIndex đến vị trí end
       currentIndex = end;
     });
 
     // Thêm phần còn lại của text sau vị trí tag cuối cùng
     if (currentIndex < text.length) {
       highlightedText.push(
         <span key={currentIndex}>{text.slice(currentIndex)}</span>
       );
     }
 
     return highlightedText;
   };
 
   return (
     <div style={{ display: "flex", flexDirection: "row" }}>
       <p>Dự đoán tự động</p>
       <div
         style={{
           minWidth: "1100px",
           fontSize: "18px",
           border: "1px solid #ddd",
           padding: "10px",
           marginTop: "10px",
           whiteSpace: "pre-wrap",
           wordWrap: "break-word",
           overflowWrap: "break-word",
           boxSizing: "border-box",
           cursor: "text",
           textAlign: "left",
         }}
       >
         {renderHighlightedText()}
       </div>
     </div>
   );
 };
 
 export default HighlightPredict;
 