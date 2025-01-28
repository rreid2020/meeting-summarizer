// frontend/src/pages/Dashboard.js
import React from 'react';
import FileUpload from '../components/FileUpload';

function Dashboard() {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-900">Dashboard</h2>
      <FileUpload />
    </div>
  );
}

export default Dashboard;