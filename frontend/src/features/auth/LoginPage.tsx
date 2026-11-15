import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiClient, googleLoginUrl } from "../../services/api-client";

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

  return <div className="auth-page"><section className="auth-visual"><div className="visual-top"><div className="brand light"><span className="brand-mark">✦</span><span>ASTREA</span></div><span className="visual-label">TALENT, ELEVATED</span></div><div className="visual-content"><div className="orbit orbit-one" /><div className="orbit orbit-two" /><div className="visual-star">✦</div><p className="visual-kicker">THE FUTURE OF WORK</p><h2>Find the place<br />you <em>belong.</em></h2><p className="visual-description">A more human way to discover meaningful work and the people who make it happen.</p></div><div className="visual-footer"><span>01</span><span className="footer-line" /><span>Designed for possibility</span></div></section><main className="auth-card"><div className="mobile-brand brand"><span className="brand-mark">✦</span><span>ASTREA</span></div><div className="form-heading"><p className="eyebrow">WELCOME BACK</p><h1>Sign in to your<br /><span>next chapter.</span></h1><p>Enter your details to continue your journey.</p></div><form onSubmit={submit}><label>Email address<input type="email" placeholder="you@example.com" value={email} onChange={(e) => setEmail(e.target.value)} required /></label><label>Password<div className="input-wrap"><input type="password" placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} required /><span className="input-icon">⌁</span></div></label><div className="form-meta"><label className="check-label"><input type="checkbox" /> <span>Remember me</span></label><a href="#forgot">Forgot password?</a></div>{error && <p role="alert">{error}</p>}<button className="primary-button full-width" disabled={loading}>{loading ? "Signing in…" : "Sign in"}<span>→</span></button></form><div className="form-divider"><span>or continue with</span></div><button className="social-button" type="button" onClick={() => { window.location.href = googleLoginUrl; }}><span className="social-g">G</span> Continue with Google</button><p className="switch-auth">New to ASTREA? <Link to="/register">Create an account <span>→</span></Link></p></main></div>;
}
