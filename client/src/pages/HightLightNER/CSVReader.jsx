// CsvReader.js
import Papa from "papaparse";

const CSVReader = ({onCsvDataUpdate}) => {


   // Hàm để đọc và parse file CSV
  const handleFileUpload = (event) => {
   const file = event.target.files[0];
   Papa.parse(file, {
     complete: (result) => {
       const dataObj = result.data.reduce((acc, [index, content]) => {
         acc[index.trim()] = content.trim();
         return acc;
       }, {});
       onCsvDataUpdate(dataObj); // Gửi dữ liệu CSV lên component cha
     },
     skipEmptyLines: true,
   });
 };

   return (
      <div style={{height: "50px", fontSize: "20px"}}>
      <label>Upload source file(File đã được xóa nhãn):  </label>
     {/* Thêm input để upload file */}
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
 