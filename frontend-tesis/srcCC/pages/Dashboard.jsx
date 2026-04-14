import React from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';
import DashboardHome from './dashboard/DashboardHome';

export default function Dashboard() {
  return (
    <DashboardLayout>
       <DashboardHome />
    </DashboardLayout>
  );
}