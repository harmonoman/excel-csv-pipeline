import { useState } from "react";
import { useDropzone } from "react-dropzone";
import UploadResult from "./UploadResult";

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

// State machine:
//   idle     → file selected or rejected
//   loading  → POST /upload in flight, UI locked
//   success  → API responded with result, show UploadResult
//   error    → API call failed, show error, allow retry

export default function UploadDropzone() {
  const [file, setFile] = useState(null);
  const [validationError, setValidationError] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [apiError, setApiError] = useState("");

  function handleFile(incoming) {
    // Clear any previous API error when user selects a new file
    setApiError("");
    if (!isXlsx(incoming)) {
      setFile(null);
      setValidationError("Only .xlsx files are supported.");
      return;
    }
    if (incoming.size === 0) {
      setFile(null);
      setValidationError("This file is empty. Please select a valid .xlsx file.");
      return;
    }
    setFile(incoming);
    setValidationError("");
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
    },
    multiple: false,
    // Disable dropzone while request is in flight — prevents mid-upload file swaps
    disabled: loading,
    onDragEnter() {
      if (validationError) setValidationError("");
    },
    onDrop(accepted, rejected) {
      if (accepted.length > 0) handleFile(accepted[0]);
      if (rejected.length > 0) {
        setFile(null);
        setValidationError("Only .xlsx files are supported.");
      }
    },
  });

  async function handleSubmit() {
    if (!file || loading) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setApiError("");
    setResult(null);

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData,
        // Do NOT set Content-Type header — browser sets it automatically
        // with the correct multipart boundary when using FormData.
      });

      if (!response.ok) {
        // Check response.ok before parsing JSON — error responses may not be JSON
        // (e.g. a 502 from nginx returns HTML). Inner try/catch handles that safely.
        let message = "Upload failed. Please try again.";
        try {
          const data = await response.json();
          message = data?.error?.message || message;
        } catch {}
        setApiError(message);
        return;
      }

      const data = await response.json();
      setResult(data);
      setFile(null);

    } catch (err) {
      // Network failure or JSON parse error on success response
      setApiError("Upload failed. Check your connection and try again.");
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setFile(null);
    setValidationError("");
    setApiError("");
    setResult(null);
    setLoading(false);
  }

  function handleClear(e) {
    e.stopPropagation();
    setFile(null);
    setValidationError("");
  }

  // Success state — replace the dropzone with results
  if (result) {
    return <UploadResult result={result} onReset={handleReset} />;
  }

  const submitDisabled = !file || loading;

  return (
    <div style={styles.wrap}>

      {/* Drop zone — locked during upload */}
      <div
        {...getRootProps()}
        style={{
          ...styles.zone,
          ...(isDragActive ? styles.zoneActive : {}),
          ...(loading ? styles.zoneLocked : {}),
        }}
      >
        <input {...getInputProps()} />
        <p style={styles.zoneLabel}>
          {loading
            ? "Processing..."
            : isDragActive
            ? "Drop it here"
            : "Drag & drop an .xlsx file, or click to select"}
        </p>
      </div>

      {/* Valid file info */}
      {file && !loading && (
        <div style={styles.fileRow}>
          <span style={styles.fileName}>{file.name}</span>
          <span style={styles.fileSize}>{formatSize(file.size)}</span>
          <button onClick={handleClear} style={styles.clearBtn} aria-label="Remove">
            &times;
          </button>
        </div>
      )}

      {/* Client-side validation error */}
      {validationError && <p style={styles.error}>{validationError}</p>}

      {/* API error */}
      {apiError && <p style={styles.error}>{apiError}</p>}

      {/* Submit */}
      <button
        onClick={handleSubmit}
        disabled={submitDisabled}
        style={{ ...styles.submit, ...(submitDisabled ? styles.submitDisabled : {}) }}
      >
        {loading ? "Uploading..." : "Upload"}
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
  zoneLocked: {
    cursor: "default",
    opacity: 0.6,
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
