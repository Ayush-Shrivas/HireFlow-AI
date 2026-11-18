import { Navigate, Route, Routes } from "react-router-dom";
import LoginPage from "./features/auth/LoginPage";
import RegisterPage from "./features/auth/RegisterPage";
import AuthCallbackPage from "./features/auth/AuthCallbackPage";
import ProfessionalDashboard from "./features/dashboard/ProfessionalDashboard";
import { ForgotPasswordPage, InterviewsPage, MessagesPage, ProfilePage, ResetPasswordPage, ResourcesPage } from "./features/portal/PortalPages";
import "./features/dashboard/styles";
import "./features/dashboard/professional.css";

export default function App() {
  return <Routes><Route path="/" element={<LoginPage />} /><Route path="/login" element={<LoginPage />} /><Route path="/register" element={<RegisterPage />} /><Route path="/forgot-password" element={<ForgotPasswordPage />} /><Route path="/reset-password" element={<ResetPasswordPage />} /><Route path="/auth/callback" element={<AuthCallbackPage />} /><Route path="/dashboard" element={<ProfessionalDashboard />} /><Route path="/profile" element={<ProfilePage />} /><Route path="/messages" element={<MessagesPage />} /><Route path="/resources" element={<ResourcesPage />} /><Route path="/interviews" element={<InterviewsPage />} /><Route path="*" element={<Navigate to="/dashboard" replace />} /></Routes>;
}
