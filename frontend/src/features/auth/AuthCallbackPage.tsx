import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { apiClient } from "../../services/api-client";

export default function AuthCallbackPage() {
  const navigate = useNavigate();
  const [params] = useSearchParams();

  useEffect(() => {
    async function finishSignIn() {
      const access = params.get("access");
      const refresh = params.get("refresh");
      if (!access || !refresh) {
        navigate("/login?error=google_failed", { replace: true });
        return;
      }
      localStorage.setItem("hireflow_access", access);
      localStorage.setItem("hireflow_refresh", refresh);
      try {
        const { data } = await apiClient.get("/auth/me/", { headers: { Authorization: `Bearer ${access}` } });
        localStorage.setItem("hireflow_user", JSON.stringify(data));
        navigate("/dashboard", { replace: true });
      } catch {
        localStorage.removeItem("hireflow_access");
        localStorage.removeItem("hireflow_refresh");
        navigate("/login?error=google_failed", { replace: true });
      }
    }
    void finishSignIn();
  }, [navigate, params]);

  return <main className="auth-card"><div className="form-heading"><p className="eyebrow">AUTHENTICATING</p><h1>Preparing your<br /><span>next chapter.</span></h1><p>Completing Google sign-in…</p></div></main>;
}
