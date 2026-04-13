import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
 
// T6-2 note: add a proxy entry here when wiring POST /upload:
//   server: { proxy: { "/upload": "http://localhost:8000", "/download": "http://localhost:8000" } }
// Not added now — no API calls in T6-0 or T6-1.
export default defineConfig({
  plugins: [react()],
});
