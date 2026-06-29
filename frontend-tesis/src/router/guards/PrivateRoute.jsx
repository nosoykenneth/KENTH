import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { hasMoodleSession } from '../../shared/utils/moodleToken';

const PrivateRoute = ({ onboardingOnly = false }) => {
  const location = useLocation();

  // Fuente unica de verdad: un valor invalido (p. ej. "null") cuenta como SIN sesion.
  const autenticado = hasMoodleSession();
  const requiresOnboarding = localStorage.getItem('moodle_requires_onboarding') === '1';

  // Sin sesion valida => login
  if (!autenticado) {
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
