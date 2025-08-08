import React, { useState } from "react";
import axios from "axios";

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setError("");
    try {
      // This endpoint should be implemented in your backend
      await axios.post("/api/v1/auth/forgot-password", { email });
      setMessage("If an account with that email exists, a reset link has been sent.");
    } catch (err: any) {
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
          <h1 className="text-2xl font-bold text-gray-800 mb-1">Forgot Password?</h1>
          <p className="text-gray-500 text-sm text-center">
            Enter your email address and we’ll send you a link to reset your password.
          </p>
        </div>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="email"
            name="email"
            placeholder="Email"
            className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
          <button
            type="submit"
            className="w-full py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            disabled={loading}
          >
            {loading ? "Sending..." : "Send Reset Link"}
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

export default ForgotPassword; 