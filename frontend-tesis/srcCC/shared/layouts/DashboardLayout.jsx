import { useEffect, useState } from 'react';
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import { logoMain } from '@/shared/assets';
import {
  mainDashboardNavigation,
  secondaryDashboardNavigation,
} from '@/shared/config/dashboardNavigation';
import {
  clearMoodleSession,
  getMoodleFullName,
  subscribeToMoodleSession,
} from '@/shared/lib/moodleSession';
import { getUserInitials } from '@/shared/lib/userDisplay';

function SidebarLink({ item, isExpanded }) {
  const baseClassName =
    'w-full rounded-2xl border px-3 py-3 transition-all duration-300 flex items-center gap-4';

  if (item.to) {
    return (
      <NavLink
        to={item.to}
        className={({ isActive }) =>
          `${baseClassName} ${
            isActive
              ? 'bg-kenth-surface/35 border-kenth-brightred/40 text-white shadow-inner'
              : 'border-transparent text-gray-400 hover:bg-kenth-surface/20 hover:text-white'
          } ${isExpanded ? 'lg:justify-start' : 'lg:justify-center'} justify-center`
        }
      >
        <svg className="w-6 h-6 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
          {item.iconPaths.map((iconPath) => (
            <path key={iconPath} strokeLinecap="round" strokeLinejoin="round" d={iconPath} />
          ))}
        </svg>
        <span className={`hidden ${isExpanded ? 'lg:block' : 'hidden'}`}>
          <span className="block font-semibold">{item.label}</span>
          <span className="block text-[11px] uppercase tracking-[0.2em] text-gray-500">
            {item.subtitle}
          </span>
        </span>
      </NavLink>
    );
  }

  return (
    <button
      type="button"
      disabled
      className={`${baseClassName} border-dashed border-kenth-surface/20 text-gray-500 cursor-not-allowed ${
        isExpanded ? 'lg:justify-start' : 'lg:justify-center'
      } justify-center`}
    >
      <svg className="w-6 h-6 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
        {item.iconPaths.map((iconPath) => (
          <path key={iconPath} strokeLinecap="round" strokeLinejoin="round" d={iconPath} />
        ))}
      </svg>
      <span className={`hidden ${isExpanded ? 'lg:block' : 'hidden'}`}>
        <span className="block font-semibold">{item.label}</span>
        <span className="block text-[11px] uppercase tracking-[0.2em] text-gray-500">
          {item.subtitle}
        </span>
      </span>
    </button>
  );
}

export default function DashboardLayout({ children }) {
  const navigate = useNavigate();
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(true);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [fullName, setFullName] = useState(getMoodleFullName() || 'Usuario');

  useEffect(() => {
    return subscribeToMoodleSession(() => {
      setFullName(getMoodleFullName() || 'Usuario');
    });
  }, []);

  const handleLogout = () => {
    clearMoodleSession();
    navigate('/');
  };

  const pageContent = children ?? <Outlet />;
  const userInitials = getUserInitials(fullName);

  return (
    <div className="min-h-screen bg-kenth-bg text-white flex font-sans">
      <aside
        className={`border-r border-kenth-surface/20 bg-black/20 backdrop-blur-md flex flex-col transition-all duration-300 z-20 shrink-0 w-20 items-center ${
          isSidebarExpanded ? 'lg:w-72 lg:items-start' : 'lg:w-24 lg:items-center'
        }`}
      >
        <div className="w-full p-5 lg:p-6">
          <Link
            to="/dashboard"
            className={`w-full flex items-center gap-4 rounded-3xl border border-kenth-surface/20 bg-white/3 px-3 py-4 transition-all ${
              isSidebarExpanded ? 'justify-start' : 'justify-center'
            }`}
          >
            <img
              src={logoMain}
              alt="KENTH logo"
              className={`w-auto object-contain transition-all ${isSidebarExpanded ? 'h-12' : 'h-10'}`}
            />
            <div className={`hidden ${isSidebarExpanded ? 'lg:block' : 'hidden'}`}>
              <p className="text-xs uppercase tracking-[0.35em] text-kenth-brightred font-black">
                Frontend
              </p>
              <p className="text-sm text-gray-300">Arquitectura modular</p>
            </div>
          </Link>
        </div>

        <div className={`hidden lg:flex w-full px-5 ${isSidebarExpanded ? 'justify-end' : 'justify-center'}`}>
          <button
            type="button"
            onClick={() => setIsSidebarExpanded((currentValue) => !currentValue)}
            className="p-2 text-gray-400 hover:text-white bg-kenth-surface/10 hover:bg-kenth-surface/30 rounded-xl transition-colors"
            title={isSidebarExpanded ? 'Contraer menu' : 'Expandir menu'}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        <nav className="w-full px-4 lg:px-5 mt-6 flex flex-col gap-3">
          {mainDashboardNavigation.map((item) => (
            <SidebarLink key={item.label} item={item} isExpanded={isSidebarExpanded} />
          ))}
        </nav>

        <div className={`w-full px-4 lg:px-5 mt-8 ${isSidebarExpanded ? 'lg:block' : 'hidden lg:block'}`}>
          <p className={`hidden ${isSidebarExpanded ? 'lg:block' : 'hidden'} text-[11px] uppercase tracking-[0.35em] text-gray-500 px-2 mb-3`}>
            Escalable
          </p>
          <div className="flex flex-col gap-3">
            {secondaryDashboardNavigation.map((item) => (
              <SidebarLink key={item.label} item={item} isExpanded={isSidebarExpanded} />
            ))}
          </div>
        </div>

        <div className="mt-auto w-full p-4 lg:p-5">
          <button
            type="button"
            onClick={handleLogout}
            className={`w-full flex items-center gap-3 rounded-2xl border border-kenth-brightred/20 text-kenth-brightred hover:bg-kenth-brightred/10 transition group ${
              isSidebarExpanded ? 'lg:px-4 py-3 lg:justify-start' : 'p-3 lg:justify-center'
            } justify-center`}
          >
            <svg className="w-6 h-6 shrink-0 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span className={`font-bold hidden ${isSidebarExpanded ? 'lg:block' : 'hidden'}`}>Salir</span>
          </button>
        </div>
      </aside>

      <main className="flex-1 flex flex-col min-w-0 h-screen">
        <header className="h-20 shrink-0 flex justify-between items-center px-6 lg:px-10 border-b border-kenth-surface/20 bg-kenth-bg/80 backdrop-blur-md relative z-30">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-gray-500 font-black">Workspace</p>
            <p className="text-sm text-gray-300">Clases listas para crecer por modulo</p>
          </div>

          <div className="flex items-center gap-6 ml-auto">
            <div className="relative hidden sm:block">
              <input
                type="text"
                placeholder="Buscar dentro del panel"
                className="bg-[#2a2a2d] border border-kenth-surface/30 rounded-full py-2 pl-4 pr-10 text-sm text-white focus:outline-none focus:border-kenth-brightred w-72 transition"
              />
              <svg className="w-4 h-4 text-gray-400 absolute right-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>

            <div className="relative">
              <button
                type="button"
                onClick={() => setIsUserMenuOpen((currentValue) => !currentValue)}
                className="flex items-center gap-3 hover:bg-kenth-surface/20 px-3 py-2 rounded-full transition"
              >
                <div className="w-9 h-9 rounded-full bg-kenth-brightred/20 border border-kenth-brightred/30 flex items-center justify-center text-sm font-black text-kenth-brightred">
                  {userInitials}
                </div>
                <div className="hidden sm:block text-left">
                  <p className="font-semibold text-sm">{fullName}</p>
                  <p className="text-[11px] uppercase tracking-[0.25em] text-gray-500">Moodle</p>
                </div>
                <svg className={`w-4 h-4 text-gray-400 transition-transform duration-300 ${isUserMenuOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {isUserMenuOpen && (
                <>
                  <button
                    type="button"
                    className="fixed inset-0 z-40"
                    onClick={() => setIsUserMenuOpen(false)}
                  />

                  <div className="absolute right-0 mt-2 w-56 bg-[#1e1e20] border border-kenth-surface/50 rounded-2xl shadow-[0_15px_40px_rgba(0,0,0,0.6)] z-50 py-2">
                    <Link
                      to="/dashboard/profile"
                      onClick={() => setIsUserMenuOpen(false)}
                      className="w-full text-left px-4 py-3 text-sm text-gray-300 hover:bg-white/5 hover:text-white flex items-center gap-3 transition"
                    >
                      <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                      Editar perfil
                    </Link>

                    <div className="h-px bg-kenth-surface/30 my-1" />

                    <button
                      type="button"
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-3 text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 flex items-center gap-3 transition"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Cerrar sesion
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </header>

        <div className="p-6 lg:p-10 w-full flex-1 overflow-y-auto">
          <div className="max-w-[1240px] mx-auto w-full">{pageContent}</div>
        </div>
      </main>
    </div>
  );
}
