import axios from "axios";

export const apiClient = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1" });

export const googleLoginUrl = `${import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1"}/auth/google/login/`;

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("hireflow_access");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
