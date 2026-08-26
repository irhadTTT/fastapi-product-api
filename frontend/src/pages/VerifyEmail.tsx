import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { verifyEmail } from "../api/auth";

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      setError("Invalid verification link.");
      setLoading(false);
      return;
    }

    verifyEmail(token)
      .then(() => {
        setSuccess(true);
      })
      .catch((error) => {
        setError(error instanceof Error ? error.message : "Email verification failed.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [searchParams]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-600">
          Verifying your email...
        </p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md rounded-xl bg-white p-8 text-center shadow-sm">
        {success ? (
          <>
            <h1 className="text-2xl font-semibold text-green-600">
              Email verified!
            </h1>

            <p className="mt-3 text-gray-600">
              Your email has been successfully verified.
            </p>

            <button
              onClick={() => navigate("/login")}
              className="mt-6 rounded-lg bg-blue-600 px-5 py-2 text-sm font-medium text-white hover:bg-blue-700"
            >
              Go to Login
            </button>
          </>
        ) : (
          <>
            <h1 className="text-2xl font-semibold text-red-600">
              Verification failed
            </h1>

            <p className="mt-3 text-gray-600">
              {error}
            </p>

            <button
              onClick={() => navigate("/login")}
              className="mt-6 rounded-lg border border-gray-300 px-5 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Go to Login
            </button>
          </>
        )}
      </div>
    </div>
  );
}