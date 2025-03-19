const EntityList = ({ tags, text, getColor, removeTag }) => (
    <div>
        <h3>Entities:</h3>
        <ul>
            {tags.map((tag, index) => (
                <li key={index} style={{ marginBottom: "5px" }}>
                    <span style={{ backgroundColor: getColor(tag.ner), padding: "2px 4px", borderRadius: "4px" }}>
                        {text.substring(tag.start, tag.end)} ({tag.ner})
                    </span>
                    <button 
                        onClick={() => removeTag(index)}
                        style={{
                           fontSize: "14px",   // Giảm kích thước font chữ
                           padding: "2px 10px", // Giảm padding để nút nhỏ gọn hơn
                           height: "25px",     // Giảm chiều cao của nút
                           marginLeft: "10px", // Khoảng cách bên trái
                           cursor: "pointer",  // Con trỏ chỉ vào nút
                           border: "none",     // Bỏ đường viền của nút
                       }}
                    >
                        ❌ Xóa
                    </button>
                </li>
            ))}
        </ul>
    </div>
);
export default EntityList