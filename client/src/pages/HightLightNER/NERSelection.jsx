const NERSelection = ({
  nerOptions,
  newNER,
  setNewNER,
  addNewNER,
  removeNEROption,
  getColor,
  handleSetTag,
}) => (
  <div>
    <span style={{ marginBottom: "10px", fontSize: "16px" }}>
      Danh sách NER:
    </span>
    <div style={{ marginBottom: "20px" }}>
      <input
        type="text"
        placeholder="Thêm NER mới"
        value={newNER}
        onChange={(e) => setNewNER(e.target.value.toUpperCase())}
        style={{
          height: "20px",
          marginLeft: "30px",
          padding: "5px",
          fontSize: "15px",
        }}
      />
      <button
        onClick={addNewNER}
        style={{ minHeight: "30px", marginLeft: "20px" }}
      >
        ➕ Thêm
      </button>
    </div>
    <div
      style={{
        marginBottom: "10px",
        display: "flex",
        flexDirection: "row",
        flexWrap: "wrap",
      }}
    >
      {nerOptions.map((ner, index) => (
        <button
          onClick={() => handleSetTag(ner)}
          key={index}
          style={{
            display: "flex", // Sử dụng flex để căn chỉnh nội dung bên trong
            alignItems: "center", // Căn giữa theo chiều dọc
            marginRight: "15px",
            marginBottom: "10px",
            padding: "5px 5px 5px 5px",
            backgroundColor: getColor(ner),
            borderRadius: "5px",
            height: "40px",
          }}
        >
          {ner}
          {ner !== "ORGANIZATION" &&
            ner !== "LOCATION" &&
            ner !== "PERSON" &&
            ner !== "MISCELLANEOUS" && (
              <button
                onClick={() => removeNEROption(ner)}
                style={{
                  marginLeft: "10px", // Đẩy nút về sát bên phải
                  fontSize: "12px", // Giảm kích thước chữ
                  padding: "2px 5px", // Giảm padding
                  height: "25px", // Giảm chiều cao của nút
                  cursor: "pointer", // Thêm hiệu ứng con trỏ khi hover
                }}
              >
                ❌
              </button>
            )}
        </button>
      ))}
    </div>
  </div>
);

export default NERSelection;
