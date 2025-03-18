const HighlightText = ({ text, handleSelection }) => (
     <div
         style={{
             position: "relative",
             fontSize: "18px",
             border: "1px solid #ddd",
             padding: "10px",
             marginTop: "10px",
             whiteSpace: "pre-wrap",
             cursor: "text"
         }}
         onMouseUp={handleSelection}
     >
         {text}
     </div>
);
export default HighlightText