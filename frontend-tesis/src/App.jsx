import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Importación de las páginas
import LandingPage from './pages/LandingPage';
// Asumo que tienes una página de login y un catálogo general. Si no, puedes comentar estas líneas por ahora
// import LoginView from './pages/LoginView'; 
// import DashboardCatalog from './pages/DashboardCatalog'; 
import CourseContentView from './pages/CourseContentView';
import ProfileSettingsView from './pages/ProfileSettingsView';
import LoginView from './pages/LoginView';
import DashboardCatalog from './pages/DashboardCatalog';
import AdminKnowledgeView from './pages/admin/AdminKnowledgeView';
import TutorView from './pages/TutorView';
import CourseSettingsView from './pages/CourseSettingsView';

// Componente para proteger las rutas del Dashboard (Solo usuarios logueados)
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('moodle_token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        
        {/* Rutas Públicas */}
        <Route path="/" element={<LandingPage />} />
        
        
          <Route path="/login" element={<LoginView />} /> 
        

        {/* Rutas Protegidas del Dashboard */}
        
        {/* Catálogo de cursos principal */}
        <Route path="/dashboard" element={<ProtectedRoute><DashboardCatalog /></ProtectedRoute>} />
        
        {/* Vista interna de un curso específico (La pesada con H5P) */}
        <Route 
          path="/dashboard/course/:id" 
          element={
            <ProtectedRoute>
              <CourseContentView />
            </ProtectedRoute>
          } 
        />
        
        {/* Vista de ajustes de curso */}
        <Route 
          path="/dashboard/course/:id/settings" 
          element={
            <ProtectedRoute>
              <CourseSettingsView />
            </ProtectedRoute>
          } 
        />

        {/* Vista de ajustes de perfil */}
        <Route 
          path="/dashboard/profile" 
          element={
            <ProtectedRoute>
              <ProfileSettingsView />
            </ProtectedRoute>
          } 
        />

        {/* Vista del Tutor IA */}
        <Route 
          path="/dashboard/tutor" 
          element={
            <ProtectedRoute>
              <TutorView />
            </ProtectedRoute>
          } 
        />

        {/* Vista Admin del RAG */}
        <Route 
          path="/dashboard/admin/knowledge" 
          element={
            <ProtectedRoute>
              <AdminKnowledgeView />
            </ProtectedRoute>
          } 
        />

        {/* Ruta comodín (404) que redirige al inicio */}
        <Route path="*" element={<Navigate to="/" replace />} />

      </Routes>
    </Router>
  );
}

export default App;