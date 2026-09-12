import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiClient } from "../../services/api-client";

export default function RegisterPage() {
  const navigate = useNavigate(); const [form, setForm] = useState({ email: "", password: "", password_confirmation: "", role: "CANDIDATE" }); const [error, setError] = useState("");
  async function submit(event: FormEvent) { event.preventDefault(); setError(""); try { await apiClient.post("/auth/register/", form); navigate("/login"); } catch { setError("Registration failed. Check the form and try again."); } }
  return <main><h1>Create your HireFlow account</h1><form onSubmit={submit}>
    <label>Email<input type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
    <label>Password<input type="password" minLength={8} required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
    <label>Confirm password<input type="password" minLength={8} required value={form.password_confirmation} onChange={(e) => setForm({ ...form, password_confirmation: e.target.value })} /></label>
    <label>Role<select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}><option value="CANDIDATE">Candidate</option><option value="RECRUITER">Recruiter</option></select></label>
    {error && <p role="alert">{error}</p>}<button>Create account</button>
  </form><Link to="/login">Already have an account?</Link></main>;
}
