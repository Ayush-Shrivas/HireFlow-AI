import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiClient } from "../../services/api-client";

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault(); setLoading(true); setError("");
    try {
      const { data } = await apiClient.post("/auth/login/", { email, password });
      localStorage.setItem("hireflow_access", data.access); localStorage.setItem("hireflow_refresh", data.refresh);
      const me = await apiClient.get("/auth/me/", { headers: { Authorization: `Bearer ${data.access}` } });
      localStorage.setItem("hireflow_user", JSON.stringify(me.data)); navigate("/dashboard");
    } catch { setError("Unable to sign in. Check your credentials."); } finally { setLoading(false); }
  }

  return <main><h1>Sign in to HireFlow AI</h1><form onSubmit={submit}>
    <label>Email<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required /></label>
    <label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required /></label>
    {error && <p role="alert">{error}</p>}<button disabled={loading}>{loading ? "Signing in…" : "Sign in"}</button>
  </form><Link to="/register">Create an account</Link></main>;
}
