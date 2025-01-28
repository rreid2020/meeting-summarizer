// frontend/src/pages/Dashboard.js
import { useState, useEffect } from 'react';
import MeetingSummarizer from '../components/MeetingSummarizer';
import RecentMeetings from '../components/RecentMeetings';

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
      <MeetingSummarizer />
      <RecentMeetings />
    </div>
  );
}