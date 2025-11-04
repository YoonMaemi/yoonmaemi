const defaultApiBaseUrl = "http://localhost:8000";

export const API_BASE_URL =
  typeof import.meta !== "undefined" && import.meta.env?.VITE_API_BASE_URL
    ? String(import.meta.env.VITE_API_BASE_URL)
    : defaultApiBaseUrl;

