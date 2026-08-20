import { useState } from "react";
import type { SubmitEvent } from "react";
import { login } from "../api/auth";
import { saveTokens } from "../auth/authStorage";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();

    setError("");

    try {
      const data = await login({
        username,
        password,
      });

      saveTokens(
        data.access_token,
        data.refresh_token
      );

      navigate("/dashboard");
    } catch (error) {
      console.error(error);
      setError("Login failed");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-xl bg-white p-8 shadow"
      >
        <h1 className="text-2xl font-bold text-slate-900">
          Login
        </h1>

        <div className="mt-6">
          <label className="block text-sm font-medium text-slate-700">
            Username
          </label>

          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2"
          />
        </div>

        <div className="mt-4">
          <label className="block text-sm font-medium text-slate-700">
            Password
          </label>

          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2"
          />
        </div>

        {error && (
          <p className="mt-4 text-sm text-red-600">
            {error}
          </p>
        )}

        <button
          type="submit"
          className="mt-6 w-full rounded-lg bg-slate-900 px-4 py-2 text-white hover:bg-slate-800"
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;