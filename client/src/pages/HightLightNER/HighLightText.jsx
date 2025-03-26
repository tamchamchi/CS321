const HighlightText = ({ text, handleSelection }) => {
  return (
    <div
      style={{
        minHeight: "30px",
        fontSize: "18px",
        border: "1px solid #ddd",
        padding: "10px",
        marginTop: "10px",
        whiteSpace: "pre-wrap",
        wordWrap: "break-word",
        overflowWrap: "break-word",
        boxSizing: "border-box",
        cursor: "text",
      }}
      onMouseUp={handleSelection}
    >
      {text}
    </div>
  );
};

export default HighlightText;
