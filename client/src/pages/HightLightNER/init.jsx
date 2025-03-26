import React, { useState } from "react";
import IndexSentenceInput from "./IndexSentenceInput";
import EntityList from "./EntityList";
import NERSelection from "./NERSelection";
import HighlightText from "./HighLightText";
import CSVReader from "./CSVReader";
import ListProcessedSentences from "./ListProcessedSentences";
import HighlightPredict from "./HighlightPredict";

const HighlightNER = () => {
  const [csvData, setCsvData] = useState([]);
  const [dataSave, setDataSave] = useState([]);
  const [indexSentence, setIndexSentence] = useState("");
  const [selectedRange, setSelectedRange] = useState(null);
  const [tags, setTags] = useState([]);
  const [textHighlight, setTextHighlight] = useState("");
  const [selectedNER, setSelectedNER] = useState("");
  const [nerOptions, setNerOptions] = useState([
    "ORGANIZATION",
    "LOCATION",
    "PERSON",
    "MISCELLANEOUS",
  ]);
  const [newNER, setNewNER] = useState("");
  const [DataTagging, setDataTagging] = useState(null);
  const [loading, setLoading] = useState(false);
  const [nerColors, setNerColors] = useState({
    ORGANIZATION: "rgba(173, 216, 230, 0.5)",
    LOCATION: "rgba(144, 238, 144, 0.5)",
    PERSON: "rgba(240, 128, 128, 0.5)",
    MISCELLANEOUS: "rgba(255, 215, 0, 0.5)",
    ORGANIZATION: "rgba(173, 216, 230, 0.5)",
    LOCATION: "rgba(144, 238, 144, 0.5)",
    PERSON: "rgba(240, 128, 128, 0.5)",
    MISCELLANEOUS: "rgba(255, 215, 0, 0.5)",
  });

  const handleCsvDataUpdate = (data) => {
    setCsvData(data);
  };

  const handleOnClickSentenceInput = (inputNumber) => {
    if (parseInt(inputNumber) >= 0) {
      setIndexSentence(inputNumber);
      let json_str = csvData[inputNumber].tags.replace(/'/g, '"');
      const data_tags = JSON.parse(json_str);
      setTags(data_tags.tags);
      setTextHighlight(data_tags.text);
    } else {
      setIndexSentence("0");
    }
  };

  const getRandomColor = () => {
    const r = Math.floor(Math.random() * 200 + 50);
    const g = Math.floor(Math.random() * 200 + 50);
    const b = Math.floor(Math.random() * 200 + 50);
    return `rgba(${r}, ${g}, ${b}, 0.5)`;
  };

  const getColor = (ner) => nerColors[ner] || "rgba(211, 211, 211, 0.5)";
  const getColor = (ner) => nerColors[ner] || "rgba(211, 211, 211, 0.5)";

  const handleSelection = () => {
   const selection = window.getSelection();
   if (selection.rangeCount === 0) return;

   const range = selection.getRangeAt(0);
   if (range.startOffset !== range.endOffset) {
     setSelectedRange(range);
   }
 };


  const handleSetTag = (ner) => {
    setSelectedNER(ner);
    if (selectedRange) {
      const existingTagIndex = tags.findIndex(
        (tag) =>
          tag.start === selectedRange.startOffset &&
          tag.end === selectedRange.endOffset
      );

      if (existingTagIndex !== -1 && tags[existingTagIndex].ner === ner) {
        // Nếu tồn tại tag đã được bôi đen và có cùng giá trị ner, xóa tag đó
        const updatedTags = [...tags];
        updatedTags.splice(existingTagIndex, 1);
        setTags(updatedTags);
      } else if (existingTagIndex !== -1) {
        // Nếu tag tồn tại nhưng khác giá trị ner, cập nhật tag đó
        const updatedTags = [...tags];
        updatedTags[existingTagIndex] = {
          ...updatedTags[existingTagIndex],
          ner: ner,
          color: getColor(ner),
        };
        setTags(updatedTags);
      } else {
        // Nếu chưa có tag ở đoạn văn bản này, thêm tag mới
        setTags([
          ...tags,
          {
            start: selectedRange.startOffset,
            end: selectedRange.endOffset,
            ner: ner,
            color: getColor(ner),
          },
        ]);
      }
    }
  };

  const addNewNER = () => {
    if (newNER && !nerOptions.includes(newNER)) {
      const newColor = getRandomColor();
      setNerOptions([...nerOptions, newNER]);
      setNerColors({ ...nerColors, [newNER]: newColor });
      setSelectedNER(newNER);
      setNewNER("");
    }
  };

  const removeNEROption = (ner) => {
    if (nerOptions.length > 1) {
      const updatedOptions = nerOptions.filter((item) => item !== ner);
      const updatedColors = { ...nerColors };
      delete updatedColors[ner];

      setNerOptions(updatedOptions);
      setNerColors(updatedColors);
      if (selectedNER === ner) {
        setSelectedNER(updatedOptions[0]);
      }
    }
  };

  const removeTag = (index) => {
    setTags(tags.filter((_, i) => i !== index));
  };

  const handleSaveDataTemp = () => {
    setIndexSentence("");
    setTags([]);
    setDataTagging(null);
    setDataSave(...dataSave, {
      index: indexSentence,
      sentence: csvData[indexSentence],
      annotation: DataTagging,
    });
  };

  const sendDataToBackend = async () => {
    const texts = csvData[indexSentence];
    const payload = { texts, tags };
    setLoading(true);
    setDataTagging(null);
    setDataTagging(null);

    try {
      const response = await fetch("http://localhost:8000/pos_tagging", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Lỗi khi gửi dữ liệu!");
      }

      console.log(response);

      const result = await response.json();

      setDataTagging(result);
    } catch (error) {
      console.error("Lỗi:", error);
      setDataTagging({ error: "Lỗi khi gửi dữ liệu!" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "10px", fontFamily: "Arial", width:"1200px"}}>
      <h2>NER Highlighter</h2>
      <CSVReader onCsvDataUpdate={handleCsvDataUpdate} />
      <CSVReader onCsvDataUpdate={handleCsvDataUpdate} />

      <IndexSentenceInput onClickSentenceInput={handleOnClickSentenceInput} />
      <HighlightPredict
         text={textHighlight}
         tags = {tags}
         getColor = {getColor}
      />
      <NERSelection
        nerOptions={nerOptions}
        selectedNER={selectedNER}
        setSelectedNER={setSelectedNER}
        newNER={newNER}
        setNewNER={setNewNER}
        addNewNER={addNewNER}
        removeNEROption={removeNEROption}
        getColor={getColor}
        handleSetTag={handleSetTag}
      />

      <HighlightText
        text={textHighlight}
        handleSelection={handleSelection}
      />

      <EntityList
        tags={tags}
        text={textHighlight}
        getColor={getColor}
        removeTag={removeTag}
      />

      <button
        onClick={sendDataToBackend}
        style={{
          marginTop: "20px",
          padding: "10px",
          fontSize: "16px",
          cursor: "pointer",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "5px",
        }}
      >
        {loading ? "Đang xử lý..." : "Gán Nhãn & Gửi"}
      </button>

      <div
        style={{
          marginTop: "20px",
          padding: "5px",
          backgroundColor: "#f9f9f9",
          borderRadius: "5px",
        }}
      >
        <h3>Kết quả gán tag</h3>
        <pre style={{ whiteSpace: "pre-wrap", wordWrap: "break-word" }}>
          {DataTagging}
        </pre>
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          justifyContent: "center",
          marginTop: "20px",
        }}
      >
        <button
          onClick={handleSaveDataTemp}
          style={{
            padding: "10px",
            fontSize: "16px",
            marginRight: "10px",
            cursor: "pointer",
            backgroundColor: "#243ba0",
            color: "white",
            border: "none",
            borderRadius: "5px",
          }}
        >
          Lưu tạm thời
        </button>

        <button
          onClick={() => {
            setIndexSentence("");
            setTags([]);
            setDataTagging(null);
          }}
          style={{
            padding: "10px",
            fontSize: "16px",
            cursor: "pointer",
            backgroundColor: "#f44336",
            color: "white",
            border: "none",
            borderRadius: "5px",
          }}
        >
          Reset
        </button>
      </div>

      <ListProcessedSentences dataSave={dataSave} />
    </div>
  );
};

export default HighlightNER;
