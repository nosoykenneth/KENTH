import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Layouts y Guards
import MarketingLayout from '../layouts/MarketingLayout';
import AcademyLayout from '../layouts/AcademyLayout';
import PrivateRoute from './guards/PrivateRoute';
import PublicRoute from './guards/PublicRoute';

// Marketing & Catalog
import LandingPage from '../modules/marketing/LandingPage';
import PublicCoursesView from '../modules/catalog/PublicCoursesView';
import PricingView from '../modules/catalog/PricingView';

// Auth
import LoginView from '../modules/auth/LoginView';

// Checkout
import CheckoutView from '../modules/checkout/CheckoutView';
import CheckoutSuccessView from '../modules/checkout/CheckoutSuccessView';

// Academy
import DashboardCatalog from '../modules/academy/DashboardCatalog';
import CourseContentView from '../modules/academy/CourseContentView';
import ProfileSettingsView from '../modules/academy/ProfileSettingsView';
import TutorView from '../modules/academy/TutorView';
import CourseSettingsView from '../modules/academy/CourseSettingsView';

// Admin
import AdminCommercialView from '../modules/admin/AdminCommercialView';
import AdminKnowledgeView from '../modules/admin/AdminKnowledgeView';

// Onboarding
import OnboardingWizard from '../modules/onboarding/OnboardingWizard';

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* GRUPO PÚBLICO (MarketingLayout) */}
        <Route element={<MarketingLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/courses" element={<PublicCoursesView />} />
          <Route path="/pricing" element={<PricingView />} />
          
          {/* SÓLO PARA GUESTS: Si ya está logueado, /login redirige a /dashboard */}
          <Route element={<PublicRoute />}>
            <Route path="/login" element={<LoginView />} />
          </Route>

          {/* Rutas Híbridas: Checkout accesible para todos */}
          <Route path="/checkout/:courseId" element={<CheckoutView />} />
          <Route path="/checkout-success" element={<CheckoutSuccessView />} />
        </Route>

        {/* RUTA DE ONBOARDING: Protegida pero fuera del AcademyLayout para ser FullScreen */}
        <Route element={<PrivateRoute />}>
           <Route path="/onboarding" element={<OnboardingWizard />} />
        </Route>


        {/* GRUPO PRIVADO (Protegido por PrivateRoute + AcademyLayout) */}
        <Route element={<PrivateRoute />}>
          <Route path="/dashboard" element={<AcademyLayout />}>
            <Route index element={<DashboardCatalog />} />
            <Route path="course/:courseId" element={<CourseContentView />} />
            <Route path="profile" element={<ProfileSettingsView />} />
            <Route path="tutor" element={<TutorView />} />
            
            {/* Rutas de Administración */}
            <Route path="admin/catalog" element={<AdminCommercialView />} />
            <Route path="admin/knowledge" element={<AdminKnowledgeView />} />
            
            {/* Nota: CourseSettingsView parece ser para editar cursos, va en admin o academy */}
            <Route path="settings/:courseId" element={<CourseSettingsView />} />
          </Route>
        </Route>

        {/* Fallback 404 - Redirigir a inicio */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
