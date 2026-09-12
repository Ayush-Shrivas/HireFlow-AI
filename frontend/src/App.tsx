import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import LoginPage from "./features/auth/LoginPage";
import RegisterPage from "./features/auth/RegisterPage";

function Dashboard() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("hireflow_user") || "null");
  if (!localStorage.getItem("hireflow_access")) return <Navigate to="/login" replace />;
  function logout() { localStorage.removeItem("hireflow_access"); localStorage.removeItem("hireflow_refresh"); localStorage.removeItem("hireflow_user"); navigate("/login"); }
  return <main><h1>HireFlow AI Dashboard</h1><p>Signed in as {user?.email || "user"}.</p><button onClick={logout}>Log out</button></main>;
}

export default function App() {
  return <Routes><Route path="/" element={<LoginPage />} /><Route path="/login" element={<LoginPage />} /><Route path="/register" element={<RegisterPage />} /><Route path="/dashboard" element={<Dashboard />} /></Routes>;
}
