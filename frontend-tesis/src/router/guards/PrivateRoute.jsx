import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const PrivateRoute = () => {
  const token = localStorage.getItem('moodle_token');
  
  // Si no hay token, redirigir al login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Si hay token, renderizar las rutas hijas (o el layout)
  return <Outlet />;
};

export default PrivateRoute;
