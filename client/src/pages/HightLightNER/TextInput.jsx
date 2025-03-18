const TextInput = ({ text, setText }) => (
     <textarea
         value={text}
         onChange={(e) => setText(e.target.value)}
         rows={4}
         cols={50}
         placeholder="Nhập đoạn văn bản vào đây..."
         style={{ width: "100%", padding: "10px", fontSize: "16px", marginBottom: "10px" }}
     />
)
export default TextInput