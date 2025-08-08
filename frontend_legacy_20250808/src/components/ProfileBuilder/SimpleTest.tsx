import React from 'react';

const SimpleTest: React.FC = () => {
  return (
    <div className="min-h-screen bg-blue-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Simple Profile Builder Test
        </h1>
        <p className="text-gray-600">
          This is a simple test without complex imports to check if the issue is with dependencies.
        </p>
      </div>
    </div>
  );
};

export default SimpleTest;