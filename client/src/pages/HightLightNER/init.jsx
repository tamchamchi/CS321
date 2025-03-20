import React, { useState } from "react";
import IndexSentenceInput from "./IndexSentenceInput";
import EntityList from "./EntityList";
import NERSelection from "./NERSelection";
import HighlightText from "./HighLightText";
import CSVReader from "./CSVReader";
import ListProcessedSentences from "./ListProcessedSentences";

const HighlightNER = () => {
  const [csvData, setCsvData] = useState({});
  const [dataSave, setDataSave] = useState([]);
  const [indexSentence, setIndexSentence] = useState("");
  const [textInput, setTextInput] = useState("");
  const [selectedRange, setSelectedRange] = useState(null);
  const [tags, setTags] = useState([]);
  const [selectedNER, setSelectedNER] = useState("");
  const [nerOptions, setNerOptions] = useState([
    "ORGANIZATION",
    "LOCATION",
    "PERSON",
    "MISCELLANEOUS",
  ]);
  const [newNER, setNewNER] = useState("");
  const [DataTagging, setDataTagging] = useState(null);
  const [dataPredict, setDataPredict] = useState(null);
  const [loading, setLoading] = useState(false);
  const [nerColors, setNerColors] = useState({
    ORGANIZATION: "rgba(173, 216, 230, 0.5)",
    LOCATION: "rgba(144, 238, 144, 0.5)",
    PERSON: "rgba(240, 128, 128, 0.5)",
    MISCELLANEOUS: "rgba(255, 215, 0, 0.5)",
  });

  const handleCsvDataUpdate = (data) => {
    setCsvData(data);
  };

  const getRandomColor = () => {
    const r = Math.floor(Math.random() * 200 + 50);
    const g = Math.floor(Math.random() * 200 + 50);
    const b = Math.floor(Math.random() * 200 + 50);
    return `rgba(${r}, ${g}, ${b}, 0.5)`;
  };

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
    if (
      selectedRange &&
      !tags.some(
        (tag) =>
          tag.start === selectedRange.startOffset &&
          tag.end === selectedRange.endOffset
      )
    ) {
      setTags([
        ...tags,
        {
          start: selectedRange.startOffset,
          end: selectedRange.endOffset,
          ner: ner,
          color: getColor(ner),
        },
      ]);
      setSelectedRange(null);
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
      sentence:
        `"` + textInput === "" ? csvData[indexSentence] : textInput + `"`,
      predict: dataPredict[0],
      annotation: DataTagging,
    });
  };

  const sendDataToBackend = async () => {
    const text = textInput === "" ? csvData[indexSentence] : textInput;
    console.log(text, tags);
    const payload = { text, tags };
    setLoading(true);
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

  const handlePredict = async () => {
    const text = textInput === "" ? csvData[indexSentence] : textInput;
    console.log(text);
    const payload = { text };
    setLoading(true);
    setDataPredict(null);

    try {
      const response = await fetch("http://localhost:8000/auto_pos_tagging", {
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
      setDataPredict(result);
    } catch (error) {
      console.error("Lỗi:", error);
      setDataPredict({ error: "Lỗi khi gửi dữ liệu!" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "10px", fontFamily: "Arial" }}>
      <h2>NER Highlighter</h2>
      <CSVReader onCsvDataUpdate={handleCsvDataUpdate} />

      <IndexSentenceInput
        setText={setTextInput}
        setIndexSentence={setIndexSentence}
      />
      <div style={{ display: "flex", marginBottom: "10px"}}>
        <div
          style={{
            marginTop: "20px",
            padding: "5px",
            backgroundColor: "#f9f9f9",
            borderRadius: "5px",
            flex: "1"
          }}
        >
         <h3>Kết quả dự đoán</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>
            {dataPredict}
          </pre>
        </div>
        <button
          onClick={handlePredict}
          style={{
            marginTop: "20px",
            marginLeft: "30px",
            padding: "10px",
            fontSize: "16px",
            cursor: "pointer",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "5px",
          }}
        >
          {loading ? "Đang xử lý..." : "Dự đoán"}
        </button>
      </div>

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
        text={textInput === "" ? csvData[indexSentence] : textInput}
        handleSelection={handleSelection}
      />

      <EntityList
        tags={tags}
        text={textInput === "" ? csvData[indexSentence] : textInput}
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
