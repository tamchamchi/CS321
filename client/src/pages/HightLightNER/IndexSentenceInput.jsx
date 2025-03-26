import { useState } from "react";

const IndexSentenceInput = ({ onClickSentenceInput }) => {
  const [inputNumber, setInputNumber] = useState("");

  const handleOnClickButton = () => {
   onClickSentenceInput(inputNumber)
  };

  const handleOnChange = (e) => {
    setInputNumber(e.target.value);
  };

  return (
    <div
      style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}
    >
      <label style={{ marginRight: "10px", whiteSpace: "nowrap" }}>
        Nhập STT của câu:
      </label>
      <input
        type="number"
        value={inputNumber}
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
