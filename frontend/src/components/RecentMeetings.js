import React from 'react';

function RecentMeetings() {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Recent Meetings</h2>
      <div className="space-y-4">
        <p className="text-gray-500">No recent meetings found.</p>
      </div>
    </div>
  );
}

export default RecentMeetings; 