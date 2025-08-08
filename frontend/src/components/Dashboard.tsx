import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const Dashboard: React.FC = () => {
  const { userSession, logout } = useAuth();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="w-full max-w-2xl p-8 bg-white rounded-xl shadow-lg">
        {/* Header with user info and logout */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold mb-2 text-gray-900">Welcome to JobTrackerDB!</h1>
            {userSession && (
              <p className="text-gray-600">Logged in as: {userSession.email}</p>
            )}
          </div>
          <button
            onClick={logout}
            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
          >
            Logout
          </button>
        </div>
        
        <div className="grid gap-4 md:grid-cols-2">
          {/* Profile Builder Card */}
          <Link 
            to="/profile-builder" 
            className="group p-6 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg text-white hover:from-blue-600 hover:to-indigo-700 transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
          >
            <div className="flex items-center mb-3">
              <div className="w-8 h-8 bg-white bg-opacity-20 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h2 className="text-xl font-semibold">Build Your Profile</h2>
            </div>
            <p className="text-blue-100 group-hover:text-white transition-colors">
              Create your comprehensive career profile with goals, experience, and skills.
            </p>
            <div className="mt-4 flex items-center text-sm text-blue-100 group-hover:text-white">
              <span>Get started</span>
              <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </Link>

          {/* Test Component Card */}
          <Link 
            to="/test" 
            className="group p-6 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg text-white hover:from-green-600 hover:to-emerald-700 transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
          >
            <div className="flex items-center mb-3">
              <div className="w-8 h-8 bg-white bg-opacity-20 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 className="text-xl font-semibold">System Test</h2>
            </div>
            <p className="text-green-100 group-hover:text-white transition-colors">
              Verify that all frontend components are working correctly.
            </p>
            <div className="mt-4 flex items-center text-sm text-green-100 group-hover:text-white">
              <span>Run test</span>
              <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </Link>
        </div>

        <div className="mt-8 text-center">
          <p className="text-gray-500 text-sm">
            More features coming soon! This is your career management command center.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;