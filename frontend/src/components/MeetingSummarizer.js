import React from 'react';
import FileUpload from './FileUpload';

function MeetingSummarizer() {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Upload Meeting Recording</h2>
      <FileUpload />
    </div>
  );
}

export default MeetingSummarizer; 