import Papa from "papaparse";

const CSVReader = ({ onCsvDataUpdate }) => {
  
  // Hàm để đọc và parse file CSV
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    Papa.parse(file, {
      complete: (result) => {
        // Duyệt qua từng dòng của CSV và xây dựng đối tượng dataObj
        const dataObj = result.data.slice(1).map(([id, sentences, xml_format, tags]) => ({
          id: id.trim(),
          sentences: sentences.trim(),
          xml_format: xml_format.trim(),
          tags: tags.trim()
        }));
        
        onCsvDataUpdate(dataObj); 
      },
      skipEmptyLines: true,
    });
  };

  return (
    <div style={{ height: "50px", fontSize: "20px" }}>
      <label>Upload file đã được gán tự động: </label>
      {/* Input để upload file */}
      <input
        type="file"
        accept=".csv"
        onChange={handleFileUpload}
        style={{ marginBottom: "10px", fontSize: "20px" }}
      />
    </div>
  );
};

export default CSVReader;
