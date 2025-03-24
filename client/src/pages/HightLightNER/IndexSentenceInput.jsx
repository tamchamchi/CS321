import { useState } from "react";

const IndexSentenceInput = ({setText, setIndexSentence }) => {
   const [inputText, setInputText] = useState("");

   const handleOnClickButton = () => {
      if (!isNaN(inputText) && Number.isInteger(Number(inputText))) {
         setIndexSentence(inputText);
         setText("");
      } else {
         setText(inputText);
         setIndexSentence("");
      }
      setIndexSentence(inputText);
   };

   const handleOnChange = (e) => {
      setInputText(e.target.value);
   };

import { useState } from "react";

const IndexSentenceInput = ({setText, setIndexSentence }) => {
   const [inputText, setInputText] = useState("");

   const handleOnClickButton = () => {
      if (!isNaN(inputText) && Number.isInteger(Number(inputText))) {
         setIndexSentence(inputText);
         setText("");
      } else {
         setText(inputText);
         setIndexSentence("");
      }
      setIndexSentence(inputText);
   };

   const handleOnChange = (e) => {
      setInputText(e.target.value);
   };

   return (
     <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
       <label style={{ marginRight: "10px", whiteSpace: "nowrap" }}>
         Nhập câu hoặc STT của câu:
       </label>
       <input
         value={inputText}
         onChange={handleOnChange}
         style={{ width: "100%", padding: "10px", fontSize: "16px", flex: 1 }}
       />
       <button
         onClick={handleOnClickButton}
         style={{ marginLeft: "20px", padding: "15px" }}
       >
         Xác nhận
       </button>
         value={inputText}
         onChange={handleOnChange}
         style={{ width: "100%", padding: "10px", fontSize: "16px", flex: 1 }}
       />
       <button
         onClick={handleOnClickButton}
         style={{ marginLeft: "20px", padding: "15px" }}
       >
         Xác nhận
       </button>
     </div>
   );
};

export default IndexSentenceInput;

};

export default IndexSentenceInput;
