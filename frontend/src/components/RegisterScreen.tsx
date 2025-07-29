import React, { useState } from "react";
import axios from "axios";

const RegisterScreen: React.FC = () => {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);
    try {
      const response = await axios.post("/api/v1/users", {
        name: form.name,
        email: form.email,
        password: form.password,
      });
      setSuccess(true);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          "Registration failed. Please try again or use another method."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-200">
      <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-xl">
        {/* Logo or App Name */}
        <div className="flex flex-col items-center mb-6">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-2">
            <span className="text-3xl font-bold text-blue-600">JT</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-800 mb-1">Create your account</h1>
          <p className="text-gray-500 text-sm">Start organizing your job search today</p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            value={form.name}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            value={form.email}
            onChange={handleChange}
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
          <button
            type="submit"
            className="w-full py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            disabled={loading}
          >
            {loading ? "Registering..." : "Register"}
          </button>
        </form>

        <div className="mt-4 text-center text-sm">
          Already have an account?{" "}
          <a href="/login" className="text-blue-600 hover:underline font-medium">
            Log in
          </a>
        </div>

        {success && (
          <div className="mt-4 text-green-600 text-center font-medium">
            Registration successful! You can now log in.
          </div>
        )}
        {error && (
          <div className="mt-4 text-red-600 text-center font-medium">{error}</div>
        )}
      </div>
    </div>
  );
};

export default RegisterScreen; 