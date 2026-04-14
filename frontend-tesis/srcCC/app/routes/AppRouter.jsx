import { BrowserRouter, Route, Routes } from 'react-router-dom';
import LoginPage from '@/features/auth/pages/LoginPage';
import CourseContentPage from '@/features/course-content/pages/CourseContentPage';
import CoursesDashboardPage from '@/features/courses/pages/CoursesDashboardPage';
import LandingPage from '@/features/landing/pages/LandingPage';
import ProfileSettingsPage from '@/features/profile/pages/ProfileSettingsPage';
import DashboardLayout from '@/shared/layouts/DashboardLayout';

function NotFoundPage() {
  return (
    <div className="min-h-screen bg-kenth-bg text-white flex items-center justify-center px-6">
      <div className="max-w-lg text-center">
        <p className="text-kenth-brightred text-xs font-black uppercase tracking-[0.35em] mb-4">
          Navegacion
        </p>
        <h1 className="text-4xl md:text-5xl font-black uppercase tracking-tight mb-4">
          Ruta no encontrada
        </h1>
        <p className="text-gray-400">
          La pantalla que buscas ya no existe o cambio de lugar dentro del frontend.
        </p>
      </div>
    </div>
  );
}

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />

        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<CoursesDashboardPage />} />
          <Route path="course/:id" element={<CourseContentPage />} />
          <Route path="profile" element={<ProfileSettingsPage />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}
