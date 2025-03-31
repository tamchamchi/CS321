import React from "react";
import Papa from "papaparse";

const ListProcessedSentences = ({ dataSave }) => {
  // Hàm để tải xuống file CSV
  const downloadCSV = () => {
    const filteredData = dataSave
      .filter((row) => row.index !== undefined && row.index !== null)
      .sort((a, b) => a.index - b.index); // Sắp xếp theo index

    console.log("Filtered Data:", filteredData); // Kiểm tra dữ liệu đã lọc

    const csvData = Papa.unparse(
      filteredData.map((row) => ({
        index: row.index,
        src_sents: row.src_sents?.sentences || "", // Kiểm tra nếu có giá trị
        predict_sents: row.src_sents?.xml_format || "",
        tagged_sents: row.tagged_sents || "",
        manual_tags: JSON.stringify(row.manual_tags || {}),
      }))
    );

    const blob = new Blob([csvData], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "annotation.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <button
        onClick={downloadCSV}
        style={{
          marginBottom: "20px",
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Tải xuống CSV
      </button>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginBottom: "20px",
          boxShadow: "0 2px 10px rgba(0, 0, 0, 0.1)",
        }}
      >
        <thead>
          <tr
            style={{
              backgroundColor: "#32728d",
              textAlign: "left",
              color: "white",
            }}
          >
            <th style={{ padding: "10px", borderBottom: "2px solid #cbbcbc" }}>
              Index
            </th>
            <th style={{ padding: "10px", borderBottom: "2px solid #cbbcbc" }}>
              Annotation
            </th>
          </tr>
        </thead>
        <tbody>
          {dataSave
            .filter((row) => row.index) // Chỉ lấy những dòng có row.index
            .map((row, index) => (
              <tr key={index}>
                <td
                  style={{ padding: "10px", borderBottom: "1px solid #cbbcbc" }}
                >
                  {row.index}
                </td>
                <td
                  style={{
                    padding: "10px",
                    borderBottom: "1px solid #cbbcbc",
                    wordBreak: "break-word",
                  }}
                >
                  {row.tagged_sents || "N/A"}
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default ListProcessedSentences;
