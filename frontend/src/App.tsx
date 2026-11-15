import { Navigate, Route, Routes } from "react-router-dom";
import LoginPage from "./features/auth/LoginPage";
import RegisterPage from "./features/auth/RegisterPage";
import AuthCallbackPage from "./features/auth/AuthCallbackPage";
import ProfessionalDashboard from "./features/dashboard/ProfessionalDashboard";
import "./features/dashboard/styles";

export default function App() {
  return <Routes><Route path="/" element={<LoginPage />} /><Route path="/login" element={<LoginPage />} /><Route path="/register" element={<RegisterPage />} /><Route path="/auth/callback" element={<AuthCallbackPage />} /><Route path="/dashboard" element={<ProfessionalDashboard />} /><Route path="*" element={<Navigate to="/dashboard" replace />} /></Routes>;
}
