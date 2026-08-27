import { useState } from "react";
import type { SubmitEvent } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { resetPassword } from "../api/auth";

function ResetPassword() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    const token = searchParams.get("token");

    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    function handleSubmit(event: SubmitEvent) {
        event.preventDefault();

        setMessage("");
        setError("");

        if (!token) {
            setError("Invalid or missing reset token.");
            return;
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);

        resetPassword({
            token,
            new_password: password,
        })
            .then((data) => {
                setMessage(data.message);
                setPassword("");
                setConfirmPassword("");
            })
            .catch((error) =>
                setError(
                    error instanceof Error
                        ? error.message
                        : "Something went wrong."
                )
            )
            .finally(() => setLoading(false));
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4">
            <form
                onSubmit={handleSubmit}
                className="w-full max-w-md rounded-xl bg-white p-8 shadow"
            >
                <h1 className="text-2xl font-bold text-slate-900">
                    Reset Password
                </h1>

                <p className="mt-2 text-sm text-slate-500">
                    Enter your new password below.
                </p>

                <div className="mt-6">
                    <label className="block text-sm font-medium text-slate-700">
                        New Password
                    </label>

                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                    />
                </div>

                <div className="mt-4">
                    <label className="block text-sm font-medium text-slate-700">
                        Confirm Password
                    </label>

                    <input
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
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
                    {loading ? "Resetting..." : "Reset Password"}
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

export default ResetPassword;