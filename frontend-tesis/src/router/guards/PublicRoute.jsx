import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { hasMoodleSession } from '../../shared/utils/moodleToken';

const PublicRoute = () => {
  // Solo se considera autenticado si el token es valido. Asi un valor basura
  // (p. ej. "null") no rebota al usuario fuera del login y le impide recuperarse.
  if (hasMoodleSession()) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
};

export default PublicRoute;
