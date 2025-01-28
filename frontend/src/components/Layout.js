// frontend/src/components/Layout.js
import { Fragment } from 'react';
import { Outlet } from 'react-router-dom';
import { Disclosure, Menu } from '@headlessui/react';

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Disclosure as="nav" className="bg-white shadow-sm">
        {/* Navigation content */}
      </Disclosure>
      <main className="py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}