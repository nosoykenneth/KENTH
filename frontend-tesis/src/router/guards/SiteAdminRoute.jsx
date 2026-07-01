import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useSitePermissions } from '../../shared/services/permissions';

/**
 * Guard de rutas de ADMINISTRACIÓN DE SITIO (Gestor IA / Precios).
 *
 * Gatea por capability real (esTecnicoRAG = is_siteadmin), no por
 * localStorage.moodle_rol. Es solo UX: la barrera real de estas vistas vive en
 * el backend (require_rag_admin). Mientras resuelve, no renderiza nada para
 * evitar un parpadeo de contenido admin a usuarios sin permiso.
 */
export default function SiteAdminRoute() {
  const { perms, loading } = useSitePermissions();
  if (loading) return null;
  return perms.esTecnicoRAG ? <Outlet /> : <Navigate to="/dashboard" replace />;
}
