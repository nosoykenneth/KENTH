import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';

const PrivateRoute = ({ onboardingOnly = false }) => {
  const location = useLocation();

  const token = localStorage.getItem('moodle_token');
  const requiresOnboarding = localStorage.getItem('moodle_requires_onboarding') === '1';

  // Sin token => login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Ruta exclusiva para onboarding
  if (onboardingOnly) {
    return requiresOnboarding
      ? <Outlet />
      : <Navigate to="/dashboard" replace />;
  }

  // Rutas privadas normales
  if (requiresOnboarding && location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />;
  }

  return <Outlet />;
};

export default PrivateRoute;