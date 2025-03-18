import React, { useState } from "react";
import TextInput from "./TextInput";
import EntityList from "./EntityList";
import NERSelection from "./NERSelection";
import HighlightText from "./HighLightText";

const HighlightNER = () => {
    const [text, setText] = useState();
    const [tags, setTags] = useState([]);
    const [selectedNER, setSelectedNER] = useState("ORGANIZATION");
    const [nerOptions, setNerOptions] = useState(["ORGANIZATION", "LOCATION", "PERSON", "MISCELLANEOUS"]);
    const [newNER, setNewNER] = useState("");
    const [responseData, setResponseData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [nerColors, setNerColors] = useState({
        "ORGANIZATION": "rgba(173, 216, 230, 0.5)", // Light Blue
        "LOCATION": "rgba(144, 238, 144, 0.5)", // Light Green
        "PERSON": "rgba(240, 128, 128, 0.5)", // Light Coral
        "MISCELLANEOUS": "rgba(255, 215, 0, 0.5)", // Light Yellow
    });

    const getRandomColor = () => {
        const r = Math.floor(Math.random() * 200 + 50);
        const g = Math.floor(Math.random() * 200 + 50);
        const b = Math.floor(Math.random() * 200 + 50);
        return `rgba(${r}, ${g}, ${b}, 0.5)`;
    };

    const getColor = (ner) => {
        return nerColors[ner] || "rgba(211, 211, 211, 0.5)"; // Default Gray
    };

    const handleSelection = () => {
        const selection = window.getSelection();
        if (!selection.rangeCount) return;

        const range = selection.getRangeAt(0);
        const start = range.startOffset;
        const end = range.endOffset;

        if (start !== end && !tags.some(tag => tag.start === start && tag.end === end)) {
            setTags([...tags, { start, end, ner: selectedNER, color: getColor(selectedNER) }]);
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
            const updatedOptions = nerOptions.filter(item => item !== ner);
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

    const sendDataToBackend = async () => {
        const payload = { text, tags };
        setLoading(true);
        setResponseData(null);

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

            const result = await response.json();
            setResponseData(result);
        } catch (error) {
            console.error("Lỗi:", error);
            setResponseData({ error: "Lỗi khi gửi dữ liệu!" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "20px", fontFamily: "Arial" }}>
            <h2>NER Highlighter</h2>
            <TextInput text={text} setText={setText} />
            <NERSelection 
                nerOptions={nerOptions} 
                selectedNER={selectedNER} 
                setSelectedNER={setSelectedNER} 
                newNER={newNER} 
                setNewNER={setNewNER} 
                addNewNER={addNewNER} 
                removeNEROption={removeNEROption}
                getColor={getColor}
            />
            <HighlightText text={text} handleSelection={handleSelection} />
            <EntityList tags={tags} text={text} getColor={getColor} removeTag={removeTag} />

            {/* Button gửi dữ liệu */}
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
            {/* Button Reset */}
            <button 
                onClick={() => {
                    setText("");
                    setTags([]);
                    setResponseData(null);
                }} 
                style={{
                    marginTop: "20px",
                    marginLeft: "10px",
                    padding: "10px",
                    fontSize: "16px",
                    cursor: "pointer",
                    backgroundColor: "#f44336",
                    color: "white",
                    border: "none",
                    borderRadius: "5px"
                }}
            >
                Reset
            </button>

            {/* Hiển thị phản hồi từ Backend */}
            {responseData && (
                <div style={{ marginTop: "20px", padding: "10px", backgroundColor: "#f9f9f9", borderRadius: "5px" }}>
                    <h3>Kết quả từ Backend:</h3>
                    <pre style={{ whiteSpace: "pre-wrap", wordWrap: "break-word" }}>
                        {responseData}
                    </pre>
                </div>
            )}
        </div>
    );
};

export default HighlightNER;