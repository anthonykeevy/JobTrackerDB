import React, { useState } from "react";
import axios from "axios";
import { useSearchParams } from "react-router-dom";

const ResetPassword: React.FC = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") || "";
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setError("");
    if (password !== confirm) {
      setError("Passwords do not match.");
      setLoading(false);
      return;
    }
    try {
      // This endpoint should be implemented in your backend
      await axios.post("/api/v1/auth/reset-password", { token, password });
      setMessage("Your password has been reset! You can now log in.");
    } catch {
      setError("Something went wrong. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-200">
      <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-xl">
        <div className="flex flex-col items-center mb-6">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-2">
            <span className="text-3xl font-bold text-blue-600">JT</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-800 mb-1">Reset Password</h1>
          <p className="text-gray-500 text-sm text-center">
            Enter your new password below.
          </p>
        </div>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="password"
            name="password"
            placeholder="New Password"
            className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
          <input
            type="password"
            name="confirm"
            placeholder="Confirm New Password"
            className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            value={confirm}
            onChange={e => setConfirm(e.target.value)}
            required
          />
          <button
            type="submit"
            className="w-full py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            disabled={loading}
          >
            {loading ? "Resetting..." : "Reset Password"}
          </button>
        </form>
        {message && (
          <div className="mt-4 text-green-600 text-center font-medium">{message}</div>
        )}
        {error && (
          <div className="mt-4 text-red-600 text-center font-medium">{error}</div>
        )}
        <div className="mt-4 text-center text-sm">
          <a href="/login" className="text-blue-600 hover:underline font-medium">
            Back to Login
          </a>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword; 