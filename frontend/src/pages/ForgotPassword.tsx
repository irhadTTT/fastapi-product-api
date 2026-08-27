import { useState } from "react";
import type { SubmitEvent } from "react";
import { useNavigate } from "react-router-dom";
import { forgotPassword } from "../api/auth";

function ForgotPassword() {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    function handleSubmit(event: SubmitEvent) {
        event.preventDefault();

        setMessage("");
        setError("");
        setLoading(true);

        forgotPassword({ email })
            .then((data) => {
                setMessage(data.message);
                setEmail("");
            })
            .catch((error) => setError(
                error instanceof Error
                    ? error.message
                    : "Something went wrong."
            ))
            .finally(() => setLoading(false));
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4">
            <form
                onSubmit={handleSubmit}
                className="w-full max-w-md rounded-xl bg-white p-8 shadow"
            >
                <h1 className="text-2xl font-bold text-slate-900">
                    Forgot Password
                </h1>

                <p className="mt-2 text-sm text-slate-500">
                    Enter your email address and we will send you a link
                    to reset your password.
                </p>

                <div className="mt-6">
                    <label className="block text-sm font-medium text-slate-700">
                        Email
                    </label>

                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="you@example.com"
                        required
                        className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                    />
                </div>

                {error && (
                    <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
                        {error}
                    </p>
                )}

                {message && (
                    <p className="mt-4 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-600">
                        {message}
                    </p>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    className="mt-6 w-full rounded-lg bg-slate-900 px-4 py-2 font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                >
                    {loading ? "Sending..." : "Send Reset Link"}
                </button>

                <button
                    type="button"
                    onClick={() => navigate("/login")}
                    className="mt-4 w-full text-sm text-slate-500 hover:text-slate-900"
                >
                    Back to Login
                </button>
            </form>
        </div>
    );
}

export default ForgotPassword;