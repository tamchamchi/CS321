const IndexSentenceInput = ({ indexSentence, setIndexSentence }) => {
   return (
     <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
       <label style={{ marginRight: "10px", whiteSpace: "nowrap" }}>
         Nhập số thứ tự của câu:
       </label>
       <input
         value={indexSentence}
         onChange={(e) => setIndexSentence(e.target.value)}
         style={{
           width: "100%", 
           padding: "10px",
           fontSize: "16px",
           flex: 1,
         }}
       />
       {/* <button style={{marginLeft: "20px", padding: "15px"}}>Xác nhận</button> */}
     </div>
   );
 };
 
 export default IndexSentenceInput;
 