import { useState } from "react";
import { useDropzone } from "react-dropzone";

// Extension check only — intentionally minimal.
// Backend re-validates file type and contents.
// We check the name, not the MIME type, because MIME can be spoofed
// and react-dropzone's accept filter alone is not sufficient UX feedback.
function isXlsx(file) {
  return file.name.toLowerCase().endsWith(".xlsx");
}

function formatSize(bytes) {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function UploadDropzone() {
  // Three possible states: null (no file), File object (valid), "error" (invalid)
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

    function handleFile(incoming) {
    if (!isXlsx(incoming)) {
        setFile(null);
        setError("Only .xlsx files are supported.");
        return;
    }
    if (incoming.size === 0) {
        setFile(null);
        setError("This file is empty. Please select a valid .xlsx file.");
        return;
    }
    setFile(incoming);
    setError("");
    }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
    },
    multiple: false,
    onDragEnter() {
      if (error) setError("");
    },
    onDrop(accepted, rejected) {
      if (accepted.length > 0) {
        handleFile(accepted[0]);
      }
      if (rejected.length > 0) {
        setFile(null);
        setError("Only .xlsx files are supported.");
      }
    },
  });

  function handleSubmit() {
    if (!file) return;
    // T6-2 replaces this with POST /upload
    console.log("[T6-1] file ready for upload:", file.name, formatSize(file.size));
  }

  function handleClear(e) {
    e.stopPropagation();
    setFile(null);
    setError("");
  }

  return (
    <div style={styles.wrap}>

      {/* Drop zone */}
      <div
        {...getRootProps()}
        style={{
          ...styles.zone,
          ...(isDragActive ? styles.zoneActive : {}),
        }}
      >
        <input {...getInputProps()} />
        <p style={styles.zoneLabel}>
          {isDragActive ? "Drop it here" : "Drag & drop an .xlsx file, or click to select"}
        </p>
      </div>

      {/* Valid file info */}
      {file && (
        <div style={styles.fileRow}>
          <span style={styles.fileName}>{file.name}</span>
          <span style={styles.fileSize}>{formatSize(file.size)}</span>
          <button onClick={handleClear} style={styles.clearBtn} aria-label="Remove">
            &times;
          </button>
        </div>
      )}

      {/* Validation error */}
      {error && <p style={styles.error}>{error}</p>}

      {/* Submit — disabled until valid file selected */}
      <button
        onClick={handleSubmit}
        disabled={!file}
        style={{ ...styles.submit, ...(!file ? styles.submitDisabled : {}) }}
      >
        Upload
      </button>

    </div>
  );
}

const styles = {
  wrap: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  zone: {
    border: "2px dashed #ccc",
    borderRadius: "8px",
    padding: "2.5rem 1.5rem",
    textAlign: "center",
    cursor: "pointer",
    background: "#fafafa",
    transition: "border-color 0.15s, background 0.15s",
  },
  zoneActive: {
    borderColor: "#666",
    background: "#f0f0f0",
  },
  zoneLabel: {
    margin: 0,
    fontSize: "14px",
    color: "#555",
  },
  fileRow: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    padding: "8px 12px",
    border: "1px solid #ddd",
    borderRadius: "6px",
    background: "#fff",
  },
  fileName: {
    flex: 1,
    fontSize: "13px",
    fontWeight: "500",
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },
  fileSize: {
    fontSize: "12px",
    color: "#888",
    flexShrink: 0,
  },
  clearBtn: {
    background: "none",
    border: "none",
    cursor: "pointer",
    fontSize: "18px",
    color: "#aaa",
    lineHeight: 1,
    padding: 0,
    flexShrink: 0,
  },
  error: {
    margin: 0,
    padding: "8px 12px",
    background: "#fef2f2",
    border: "1px solid #fecaca",
    borderRadius: "6px",
    fontSize: "13px",
    color: "#b91c1c",
  },
  submit: {
    padding: "10px",
    fontSize: "14px",
    fontWeight: "500",
    border: "1px solid #ccc",
    borderRadius: "6px",
    background: "#fff",
    cursor: "pointer",
  },
  submitDisabled: {
    opacity: 0.4,
    cursor: "not-allowed",
  },
};