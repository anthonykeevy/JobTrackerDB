// React import removed as it's not needed in modern React
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import RegisterScreen from "./components/RegisterScreen";
import LoginScreen from "./components/LoginScreen";
import Dashboard from "./components/Dashboard";
import ForgotPassword from "./components/ForgotPassword";
import ResetPassword from "./components/ResetPassword";
import ProfileBuilder from "./components/ProfileBuilder";
import TestComponent from "./components/TestComponent";
import SimpleTest from "./components/ProfileBuilder/SimpleTest";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/register" element={<RegisterScreen />} />
        <Route path="/login" element={<LoginScreen />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        
        {/* Protected Routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        <Route path="/profile-builder" element={
          <ProtectedRoute>
            <ProfileBuilder />
          </ProtectedRoute>
        } />
        <Route path="/simple-test" element={
          <ProtectedRoute>
            <SimpleTest />
          </ProtectedRoute>
        } />
        <Route path="/test" element={
          <ProtectedRoute>
            <TestComponent />
          </ProtectedRoute>
        } />
        
        {/* Default redirect */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
