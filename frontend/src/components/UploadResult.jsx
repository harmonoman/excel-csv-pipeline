// UploadResult.jsx — T6-2 results display
//
// Receives the API response and renders:
//   - Summary counts (total / clean / rejected)
//   - Download buttons for both CSVs
//
// Intentionally stateless — all data flows in via props.
// Download links use relative URLs (e.g. /download/{filename}) so the
// Vite proxy routes them correctly — consistent with how POST /upload is called.

export default function UploadResult({ result, onReset }) {
  const { total_rows, clean_rows, rejected_rows, clean_file, rejected_file } = result;

  return (
    <div style={styles.wrap}>

      {/* Summary */}
      <div style={styles.summary}>
        <div style={styles.stat}>
          <span style={styles.statLabel}>Total rows</span>
          <span style={styles.statValue}>{total_rows}</span>
        </div>
        <div style={styles.stat}>
          <span style={styles.statLabel}>Clean</span>
          <span style={{ ...styles.statValue, color: "#166534" }}>{clean_rows}</span>
        </div>
        <div style={styles.stat}>
          <span style={styles.statLabel}>Rejected</span>
          <span style={{ ...styles.statValue, color: rejected_rows > 0 ? "#991b1b" : "#888" }}>
            {rejected_rows}
          </span>
        </div>
      </div>

      {/* Download buttons — relative URLs, proxied by Vite to the backend */}
      <div style={styles.downloads}>
        <a href={clean_file} download style={styles.downloadBtn}>
          Download clean CSV
        </a>
        <a href={rejected_file} download style={styles.downloadBtnSecondary}>
          Download rejected CSV
        </a>
      </div>

      {/* Upload another file */}
      <button onClick={onReset} style={styles.resetBtn}>
        Upload another file
      </button>

    </div>
  );
}

const styles = {
  wrap: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
  },
  summary: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: "10px",
  },
  stat: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "12px 8px",
    border: "1px solid #e5e7eb",
    borderRadius: "8px",
    background: "#f9fafb",
  },
  statLabel: {
    fontSize: "11px",
    color: "#6b7280",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    marginBottom: "4px",
  },
  statValue: {
    fontSize: "22px",
    fontWeight: "600",
    color: "#111",
  },
  downloads: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  downloadBtn: {
    display: "block",
    padding: "10px",
    textAlign: "center",
    fontSize: "14px",
    fontWeight: "500",
    border: "1px solid #ccc",
    borderRadius: "6px",
    background: "#fff",
    color: "#111",
    textDecoration: "none",
    cursor: "pointer",
  },
  downloadBtnSecondary: {
    display: "block",
    padding: "10px",
    textAlign: "center",
    fontSize: "14px",
    fontWeight: "500",
    border: "1px solid #e5e7eb",
    borderRadius: "6px",
    background: "#f9fafb",
    color: "#374151",
    textDecoration: "none",
    cursor: "pointer",
  },
  resetBtn: {
    padding: "8px",
    fontSize: "13px",
    border: "none",
    background: "none",
    color: "#6b7280",
    cursor: "pointer",
    textDecoration: "underline",
  },
};