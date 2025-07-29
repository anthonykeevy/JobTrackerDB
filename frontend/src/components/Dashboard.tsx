import React from "react";

const Dashboard: React.FC = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
    <div className="w-full max-w-md p-8 bg-white rounded shadow">
      <h1 className="text-2xl font-bold mb-2 text-center">Dashboard</h1>
      <p className="text-center text-gray-600">Welcome! You are now logged in.</p>
    </div>
  </div>
);

export default Dashboard;