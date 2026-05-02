import React, { useState, useEffect } from 'react';
import { Link, useLocation, useOutlet, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Logo from '../shared/components/ui/Logo';
import Notification from '../shared/components/ui/Notification';
import ThemeToggle from '../shared/components/ui/ThemeToggle';
import UserMenu from '../shared/components/layout/UserMenu';

const AssistantIcon = ({ isActive }) => {
  return (
    <div className="relative w-6 h-6">
      <div className={`absolute inset-0 animate-kenth-rgb-hue transition-opacity duration-500 ${isActive ? 'opacity-0' : 'opacity-100'}`}>
        <svg className="w-full h-full" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="rgb-gradient-static" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#ff0000" />
              <stop offset="100%" stopColor="#00ffff" />
            </linearGradient>
          </defs>
          <path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.456-2.455l.259-1.036.259 1.036a3.375 3.375 0 002.455 2.456l1.036.259-1.036.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" stroke="url(#rgb-gradient-static)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
      <svg className={`absolute inset-0 w-6 h-6 transition-opacity duration-500 ${isActive ? 'opacity-100' : 'opacity-0'}`} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="brand-gradient-flow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" className="brand-stop-1" />
            <stop offset="100%" className="brand-stop-2" />
          </linearGradient>
        </defs>
        <path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.456-2.455l.259-1.036.259 1.036a3.375 3.375 0 002.455 2.456l1.036.259-1.036.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" stroke="url(#brand-gradient-flow)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </div>
  );
};

const NavItem = ({ to, icon, label, activeColor = "text-kenth-brightred", isRGB = false, sidebarExpandida }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Link 
      to={to} 
      className={`p-3 rounded-xl flex items-center gap-4 transition-all duration-200 justify-center ${sidebarExpandida ? 'lg:justify-start' : 'lg:justify-center'} ${isActive ? 'bg-kenth-surface/30 text-kenth-text shadow-inner font-bold' : `text-kenth-subtext hover:bg-kenth-surface/20 hover:text-kenth-text font-semibold`}`}
    >
      <div className={`w-6 h-6 shrink-0 flex items-center justify-center transition-all duration-500 ${isRGB ? 'animate-kenth-rgb-hue' : (isActive ? activeColor : '')}`}>
        {typeof icon === 'function' ? icon({ isActive }) : icon}
      </div>
      <span className={`hidden ${sidebarExpandida ? 'lg:block' : 'hidden'} truncate`}>{label}</span>
    </Link>
  );
};

export default function AcademyLayout() {
  const location = useLocation();
  const outlet = useOutlet();
  const navigate = useNavigate();

  const [sidebarExpandida, setSidebarExpandida] = useState(() => {
    const guardado = localStorage.getItem('sidebar_expandida');
    return guardado !== null ? JSON.parse(guardado) : true;
  });
  
  useEffect(() => {
    localStorage.setItem('sidebar_expandida', JSON.stringify(sidebarExpandida));
  }, [sidebarExpandida]);
  
  const [userRole, setUserRole] = useState(() => localStorage.getItem('moodle_rol') || 'student');
  
  useEffect(() => {
    if (location.pathname === '/dashboard/tutor' && sidebarExpandida) {
      setSidebarExpandida(false);
    }
    const contentArea = document.getElementById('main-content-area');
    if (contentArea) contentArea.scrollTo(0, 0);
  }, [location.pathname]);

  return (
    <div className="min-h-screen bg-kenth-bg text-kenth-text flex font-sans">
      <aside className={`border-r border-kenth-border bg-kenth-bg flex flex-col transition-all duration-300 z-20 shrink-0 w-20 items-center ${sidebarExpandida ? 'lg:w-64 lg:items-start' : 'lg:w-20 lg:items-center'}`}>
        <div className={`w-full flex items-center transition-all justify-center p-5 ${sidebarExpandida ? 'lg:p-8 lg:justify-center' : 'lg:p-5 lg:justify-center'}`}>
          <Logo className={`w-auto object-contain transition-all h-10 ${sidebarExpandida ? 'lg:h-14' : 'lg:h-10'}`} />
        </div>
        <div className={`hidden lg:flex w-full px-4 mb-4 ${sidebarExpandida ? 'justify-center lg:px-6' : 'justify-center'}`}>
           <button onClick={() => setSidebarExpandida(!sidebarExpandida)} className="p-2 text-kenth-subtext hover:text-kenth-text bg-kenth-surface/10 hover:bg-kenth-surface/30 rounded-lg transition-colors focus:outline-none">
             <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" /></svg>
           </button>
        </div>
        <nav className={`flex flex-col gap-2 w-full px-4 mt-2 lg:mt-0 ${sidebarExpandida ? 'lg:px-6' : ''}`}>
          <NavItem to="/dashboard" label="Dashboard" sidebarExpandida={sidebarExpandida} icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>} />
          <NavItem to="/dashboard/tutor" label="Tutor KENTH" isRGB={true} sidebarExpandida={sidebarExpandida} icon={(props) => <AssistantIcon {...props} />} />
          {(userRole === 'admin' || userRole === 'teacher') && (
            <>
              <NavItem to="/dashboard/admin/knowledge" label="Gestor IA" sidebarExpandida={sidebarExpandida} icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>} />
              <NavItem to="/dashboard/admin/catalog" label="Precios" sidebarExpandida={sidebarExpandida} icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>} />
            </>
          )}
          <NavItem to="/dashboard/profile" label="Ajustes" sidebarExpandida={sidebarExpandida} icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>} />
        </nav>
        <div className="mt-auto p-4 w-full">
          <button 
            onClick={() => navigate('/')} 
            className={`w-full flex items-center gap-3 rounded-xl text-white hover:bg-kenth-surface/20 transition group cursor-pointer justify-center ${sidebarExpandida ? 'lg:px-4 py-3 lg:justify-start' : 'p-3 lg:justify-center'}`}
          >
            <svg className="w-6 h-6 shrink-0 text-white group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
            <span className={`font-bold hidden ${sidebarExpandida ? 'lg:block' : 'hidden'}`}>Regresar</span>
          </button>
        </div>
      </aside>
      <main className="flex-1 flex flex-col min-w-0 h-screen">
        <header className="h-20 shrink-0 flex justify-between items-center px-6 lg:px-10 border-b border-kenth-border relative z-30 bg-kenth-bg/80 backdrop-blur-md">
          <div /> 
          <div className="flex items-center gap-6 ml-auto">
            <UserMenu />
            <ThemeToggle />
            <div className="relative hidden sm:block">
              <input type="text" placeholder="Buscar" className="bg-kenth-surface/10 border border-kenth-border rounded-full py-2 pl-4 pr-10 text-sm text-kenth-text focus:outline-none focus:border-kenth-brightred w-64 transition" />
              <svg className="w-4 h-4 text-kenth-subtext absolute right-4 top-1/2 transform -translate-y-1/2" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
          </div>
        </header>
        <Notification />
        <div id="main-content-area" className="w-full flex-1 overflow-y-auto scroll-smooth">
          <div className="w-full h-full">
            <AnimatePresence mode="wait">
              <motion.div
                key={location.pathname}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.25, ease: "easeOut" }}
                className="w-full h-full"
              >
                {outlet}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </main>
    </div>
  );
}
