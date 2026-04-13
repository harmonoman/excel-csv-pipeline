import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
 
export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy /upload and /download to the FastAPI backend.
    // This avoids CORS issues during local development.
    // Both containers share the docker network — backend is reachable at
    // its service name "backend" from inside docker, but from the host
    // browser we use localhost:8000.
    proxy: {
      "/upload": "http://localhost:8000",
      "/download": "http://localhost:8000",
    },
  },
});
 