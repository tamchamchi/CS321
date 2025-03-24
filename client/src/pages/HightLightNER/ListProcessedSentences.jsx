import React from "react";
import Papa from "papaparse";

const ListProcessedSentences = ({ dataSave }) => {
   // Hàm để tải xuống file CSV
   const downloadCSV = () => {
      const csvData = Papa.unparse(
         dataSave.map((row, index) => ({
            Index: index + 1,
            Sentence: row.sentence,
            Predict: row.predict,
            Annotation: row.annotation,
         }))
      );

      const blob = new Blob([csvData], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "data.csv");
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
               <tr style={{ backgroundColor: "#32728d", textAlign: "left" }}>
                  <th style={{ padding: "10px", borderBottom: "2px solid #cbbcbc" }}>Index</th>
                  <th style={{ padding: "10px", borderBottom: "2px solid #cbbcbc" }}>Sentence</th>
                  <th style={{ padding: "10px", borderBottom: "2px solid #cbbcbc" }}>Predict</th>
                  <th style={{ padding: "10px", borderBottom: "2px solid #cbbcbc" }}>Annotation</th>
               </tr>
            </thead>
            <tbody>
               {dataSave.map((row, index) => (
                  <tr key={index}>
                     <td style={{ padding: "10px", borderBottom: "1px solid #cbbcbc" }}>{index + 1}</td>
                     <td
                        style={{
                           padding: "10px",
                           borderBottom: "1px solid #ddd",
                           wordBreak: "break-word", // Xử lý câu dài
                        }}
                     >
                        {row.sentence}
                     </td>
                     <td style={{ padding: "10px", borderBottom: "1px solid #cbbcbc" }}>{row.predict}</td>
                     <td style={{ padding: "10px", borderBottom: "1px solid #cbbcbc" }}>{row.annotation}</td>
                  </tr>
               ))}
            </tbody>
         </table>
      </div>
   );
};

export default ListProcessedSentences;
