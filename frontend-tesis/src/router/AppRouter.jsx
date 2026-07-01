import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Layouts y Guards
import MarketingLayout from '../layouts/MarketingLayout';
import AcademyLayout from '../layouts/AcademyLayout';
import PrivateRoute from './guards/PrivateRoute';
import PublicRoute from './guards/PublicRoute';
import SiteAdminRoute from './guards/SiteAdminRoute';

// Marketing & Catalog
import LandingPage from '../modules/marketing/LandingPage';
import PublicCoursesView from '../modules/catalog/PublicCoursesView';
import PricingView from '../modules/catalog/PricingView';

// Auth
import LoginView from '../modules/auth/LoginView';
import ForgotPasswordView from '../modules/auth/ForgotPasswordView';
import ResetPasswordView from '../modules/auth/ResetPasswordView';

// Checkout
import CheckoutView from '../modules/checkout/CheckoutView';
import CheckoutSuccessView from '../modules/checkout/CheckoutSuccessView';

// Academy
import DashboardCatalog from '../modules/academy/DashboardCatalog';
import CourseContentView from '../modules/academy/CourseContentView';
import ProfileSettingsView from '../modules/academy/ProfileSettingsView';
import CourseSettingsView from '../modules/academy/CourseSettingsView';
import CourseAuthoringView from '../modules/academy/CourseAuthoringView';

// Admin
import AdminCommercialView from '../modules/admin/AdminCommercialView';
import AdminKnowledgeView from '../modules/admin/AdminKnowledgeView';

// Onboarding
import OnboardingWizard from '../modules/onboarding/OnboardingWizard';

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MarketingLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/courses" element={<PublicCoursesView />} />
          <Route path="/pricing" element={<PricingView />} />

          <Route element={<PublicRoute />}>
            <Route path="/login" element={<LoginView />} />
            <Route path="/forgot-password" element={<ForgotPasswordView />} />
          </Route>

          {/* Restablecer contraseña: accesible aunque el usuario llegue desde el correo
              (no se envuelve en PublicRoute para que también funcione si hay sesión activa). */}
          <Route path="/reset-password" element={<ResetPasswordView />} />

          <Route path="/checkout/:courseId" element={<CheckoutView />} />
          <Route path="/checkout-success" element={<CheckoutSuccessView />} />
        </Route>

        {/* Onboarding: solo si realmente lo necesita */}
        <Route element={<PrivateRoute onboardingOnly={true} />}>
          <Route path="/onboarding" element={<OnboardingWizard />} />
        </Route>

        {/* Rutas privadas normales */}
        <Route element={<PrivateRoute />}>
          <Route path="/dashboard" element={<AcademyLayout />}>
            <Route index element={<DashboardCatalog />} />
            <Route path="course/:courseId" element={<CourseContentView />} />
            <Route path="profile" element={<ProfileSettingsView />} />
            <Route path="tutor" element={<Navigate to="/dashboard" replace />} />
            {/* Alias legacy: vistas de depuracion del tutor retiradas. */}
            <Route path="debug-tutor" element={<Navigate to="/dashboard" replace />} />
            <Route path="pilot" element={<Navigate to="/dashboard" replace />} />
            {/* Admin de SITIO: gateado por capability real (siteadmin). */}
            <Route element={<SiteAdminRoute />}>
              <Route path="admin/catalog" element={<AdminCommercialView />} />
              <Route path="admin/knowledge" element={<AdminKnowledgeView />} />
            </Route>
            <Route path="settings/:courseId" element={<CourseSettingsView />} />
            <Route path="course/:courseId/gestion" element={<CourseAuthoringView />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
