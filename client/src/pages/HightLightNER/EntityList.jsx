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
                        style={{ marginLeft: "10px", cursor: "pointer" }}
                    >
                        ❌ Xóa
                    </button>
                </li>
            ))}
        </ul>
    </div>
);
export default EntityList