import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';

const PrivateRoute = () => {
  const location = useLocation();
  const token = localStorage.getItem('moodle_token');
  const requiresOnboarding = localStorage.getItem('moodle_requires_onboarding');
  
  // Si no hay token, redirigir al login
  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Si requiere onboarding y NO estamos ya en la página de onboarding, redirigir
  if (requiresOnboarding === '1' && location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />;
  }

  // Si ya completó onboarding y trata de entrar a /onboarding, mandarlo al dashboard
  if (requiresOnboarding === '0' && location.pathname === '/onboarding') {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
};

export default PrivateRoute;

