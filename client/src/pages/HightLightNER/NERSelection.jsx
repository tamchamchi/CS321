const NERSelection = ({ nerOptions, selectedNER, setSelectedNER, newNER, setNewNER, addNewNER, removeNEROption, getColor }) => (
     <div>
         <h4>Danh sách NER:</h4>
         {nerOptions.map((ner, index) => (
             <span 
                 key={index} 
                 style={{ 
                     marginRight: "10px", 
                     padding: "5px", 
                     backgroundColor: getColor(ner), 
                     borderRadius: "5px" 
                 }}
             >
                 {ner} <button onClick={() => removeNEROption(ner)} style={{ marginLeft: "5px" }}>❌</button>
             </span>
         ))}
         <div>
             <select onChange={(e) => setSelectedNER(e.target.value)} value={selectedNER}>
                 {nerOptions.map((ner, index) => (
                     <option key={index} value={ner}>{ner}</option>
                 ))}
             </select>
             <input
                 type="text"
                 placeholder="Thêm NER mới"
                 value={newNER}
                 onChange={(e) => setNewNER(e.target.value.toUpperCase())}
                 style={{ marginLeft: "10px", padding: "5px" }}
             />
             <button onClick={addNewNER} style={{ marginLeft: "5px" }}>➕ Thêm</button>
         </div>
     </div>
);

export default NERSelection;
