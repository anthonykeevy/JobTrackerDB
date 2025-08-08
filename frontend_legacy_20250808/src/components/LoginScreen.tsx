import React, { useState } from "react";
import axios from "axios";

const LoginScreen: React.FC = () => {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);

    try {
      const response = await axios.post("/api/v1/auth/login", {
        email: form.email,
        password: form.password,
      });
      
      // Store user session data
      const userSession = {
        userId: response.data.user_id || 1, // Default to user 1 for testing
        profileId: response.data.profile_id || 1, // Default to profile 1 for testing
        email: form.email,
        loginTime: new Date().toISOString()
      };
      
      localStorage.setItem('userSession', JSON.stringify(userSession));
      console.log('✅ User session stored:', userSession);
      
      setSuccess(true);
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1000);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
        "Login failed. Please check your credentials and try again."
      );
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
          <h1 className="text-2xl font-bold text-gray-800 mb-1">Sign in to JobTrackerDB</h1>
          <p className="text-gray-500 text-sm">Organize your job search with ease</p>
        </div>
        {/* Google Login removed for now */}
        <div className="flex items-center my-4">
          <div className="flex-grow border-t border-gray-200"></div>
          <span className="mx-2 text-gray-400 text-sm">or sign in with email</span>
          <div className="flex-grow border-t border-gray-200"></div>
        </div>
        <form onSubmit={handleEmailLogin} className="flex flex-col gap-4">
          <input
            type="email"
            name="email"
            placeholder="Email"
            className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            value={form.email}
            onChange={handleChange}
            autoFocus
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            value={form.password}
            onChange={handleChange}
            required
          />
          <div className="flex items-center justify-between text-sm">
            <label className="flex items-center gap-2">
              <input type="checkbox" name="remember" className="accent-blue-600" />
              Remember Me
            </label>
            <a href="/forgot-password" className="text-blue-600 hover:underline">
              Forgot Password?
            </a>
          </div>
          <button
            type="submit"
            className="w-full py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
        <div className="mt-4 text-center text-sm">
          Don’t have an account?{" "}
          <a href="/register" className="text-blue-600 hover:underline font-medium">
            Register
          </a>
        </div>
        {success && (
          <div className="mt-4 text-green-600 text-center font-medium">
            Login successful! Redirecting to dashboard...
          </div>
        )}
        {error && (
          <div className="mt-4 text-red-600 text-center font-medium">{error}</div>
        )}
      </div>
    </div>
  );
};

export default LoginScreen;
