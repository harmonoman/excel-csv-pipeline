import UploadDropzone from "./components/UploadDropzone";

export default function App() {
  return (
    <main style={{ maxWidth: 560, margin: "3rem auto", padding: "0 1.5rem" }}>
      <h1 style={{ fontSize: "18px", fontWeight: "500", marginBottom: "1.5rem" }}>
        Donor Bureau — Upload
      </h1>
      <UploadDropzone />
    </main>
  );
}