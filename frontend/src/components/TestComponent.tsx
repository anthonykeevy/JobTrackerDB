import React from 'react';

const TestComponent: React.FC = () => {
  return (
    <div className="min-h-screen bg-blue-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          🎉 Frontend is Working!
        </h1>
        <p className="text-gray-600">
          This is a test component to verify the setup is working correctly.
        </p>
        <div className="mt-4 p-4 bg-green-50 rounded-lg">
          <h2 className="text-lg font-semibold text-green-800 mb-2">Status Check:</h2>
          <ul className="text-sm text-green-700 space-y-1">
            <li>✅ React is working</li>
            <li>✅ TypeScript is working</li>
            <li>✅ Tailwind CSS is working</li>
            <li>✅ Component rendering is working</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TestComponent;