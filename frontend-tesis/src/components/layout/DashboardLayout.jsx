import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import logoImg from '../../assets/logo-main.png';
import Logo from '../ui/Logo';
import Notification from '../ui/Notification';
import ThemeToggle from '../ui/ThemeToggle';

const AssistantIcon = ({ isActive }) => {
  return (
    <div className="relative w-6 h-6">
      {/* Capa RGB: El contenedor animado NUNCA cambia su clase para no resetear el timer */}
      <div className={`absolute inset-0 animate-kenth-rgb-hue transition-opacity duration-500 ${isActive ? 'opacity-0' : 'opacity-100'}`}>
        <svg 
          className="w-full h-full" 
          viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="rgb-gradient-static" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#ff0000" />
              <stop offset="100%" stopColor="#00ffff" />
            </linearGradient>
          </defs>
          <path 
            d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.456-2.455l.259-1.036.259 1.036a3.375 3.375 0 002.455 2.456l1.036.259-1.036.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" 
            stroke="url(#rgb-gradient-static)" 
            strokeWidth="1.5" 
            strokeLinecap="round" 
            strokeLinejoin="round"
          />
        </svg>
      </div>

      {/* Capa de Marca: Se muestra cuando SÍ está activo */}
      <svg 
        className={`absolute inset-0 w-6 h-6 transition-opacity duration-500 ${isActive ? 'opacity-100' : 'opacity-0'}`} 
        viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="brand-gradient-flow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" className="brand-stop-1" />
            <stop offset="100%" className="brand-stop-2" />
          </linearGradient>
        </defs>
        <path 
          d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.456-2.455l.259-1.036.259 1.036a3.375 3.375 0 002.455 2.456l1.036.259-1.036.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" 
          stroke="url(#brand-gradient-flow)" 
          strokeWidth="1.5" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        />
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
      className={`
        p-3 rounded-xl flex items-center gap-4 transition-all duration-200 justify-center
        ${sidebarExpandida ? 'lg:justify-start' : 'lg:justify-center'}
        ${isActive 
          ? 'bg-kenth-surface/30 text-kenth-text shadow-inner font-bold' 
          : `text-kenth-subtext hover:bg-kenth-surface/20 hover:text-kenth-text font-semibold`
        }
      `}
    >
      <div className={`w-6 h-6 shrink-0 flex items-center justify-center transition-all duration-500
        ${isRGB ? 'animate-kenth-rgb-hue' : (isActive ? activeColor : '')}`}>
        {typeof icon === 'function' ? icon({ isActive }) : icon}
      </div>

      <span className={`hidden ${sidebarExpandida ? 'lg:block' : 'hidden'} truncate`}>
        {label}
      </span>
    </Link>
  );
};

export default function DashboardLayout({ children, fullWidth = false }) {
  // Estado para la barra lateral (Persistente con localStorage)
  const [sidebarExpandida, setSidebarExpandida] = useState(() => {
    const guardado = localStorage.getItem('sidebar_expandida');
    return guardado !== null ? JSON.parse(guardado) : true;
  });
  
  // Guardar estado en localStorage cada vez que cambie
  useEffect(() => {
    localStorage.setItem('sidebar_expandida', JSON.stringify(sidebarExpandida));
  }, [sidebarExpandida]);
  
  // Estado para el menú desplegable del usuario
  const [menuUsuarioAbierto, setMenuUsuarioAbierto] = useState(false);

  // Estados dinámicos para el usuario (Nombre y Foto)
  const [userName, setUserName] = useState(() => localStorage.getItem('moodle_userfullname') || 'Usuario');
  const [userAvatar, setUserAvatar] = useState(() => {
    let picUrl = localStorage.getItem('moodle_userpictureurl') || 'https://i.pravatar.cc/150?img=5';
    const token = localStorage.getItem('moodle_token');
    if (picUrl && token && !picUrl.includes('token=') && picUrl.includes('http')) {
      picUrl += picUrl.includes('?') ? `&token=${token}` : `?token=${token}`;
    }
    return picUrl;
  });
  const [userRole, setUserRole] = useState(() => localStorage.getItem('moodle_rol') || 'student');
  
  useEffect(() => {
    const cargarDatosUsuario = () => {
      const nombre = localStorage.getItem('moodle_userfullname');

      if (nombre) setUserName(nombre);
      


      let picUrl = localStorage.getItem('moodle_userpictureurl');
      const token = localStorage.getItem('moodle_token');
      
      // Magia: Moodle requiere el token en la URL de la imagen para dejarte verla desde React
      if (picUrl && token && !picUrl.includes('token=')) {
        picUrl += picUrl.includes('?') ? `&token=${token}` : `?token=${token}`;
      }
      
      if (picUrl) setUserAvatar(picUrl);
    };

    cargarDatosUsuario(); // Cargar al montar el componente

    // Escuchar si el perfil se actualiza desde ProfileSettingsView
    window.addEventListener('perfilActualizado', cargarDatosUsuario);
    return () => window.removeEventListener('perfilActualizado', cargarDatosUsuario);
  }, []);

  const getInitials = (name) => {
  if (!name) return "K";
  const parts = name.trim().split(' ');
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }
  return parts[0][0].toUpperCase();
};
  
  const handleLogout = (e) => {
    e.preventDefault();
    localStorage.removeItem('moodle_token');
    localStorage.removeItem('moodle_rol');
    localStorage.removeItem('moodle_userfullname');
    localStorage.removeItem('moodle_userid');
    localStorage.removeItem('moodle_userpictureurl');
    window.location.href = '/';
  };

  const location = useLocation();

  // Efecto para contraer el sidebar automáticamente SOLO si entramos al Tutor
  // y no estaba ya contraído.
  useEffect(() => {
    if (location.pathname === '/dashboard/tutor' && sidebarExpandida) {
      setSidebarExpandida(false);
    }
  }, [location.pathname]);

  return (
    <div className="min-h-screen bg-kenth-bg text-kenth-text flex font-sans transition-colors duration-400">
      
      {/* SIDEBAR DINÁMICO */}
      <aside 
        className={`
          border-r border-kenth-border bg-kenth-bg flex flex-col transition-all duration-300 z-20 shrink-0
          w-20 items-center
          ${sidebarExpandida ? 'lg:w-64 lg:items-start' : 'lg:w-20 lg:items-center'}
        `}
      >
        
        {/* LOGO */}
        <div className={`w-full flex items-center transition-all justify-center p-5 ${sidebarExpandida ? 'lg:p-8 lg:justify-center' : 'lg:p-5 lg:justify-center'}`}>
          <Logo className={`w-auto object-contain transition-all h-10 ${sidebarExpandida ? 'lg:h-14' : 'lg:h-10'}`} />
        </div>

        {/* BOTÓN HAMBURGUESA */}
        <div className={`hidden lg:flex w-full px-4 mb-4 ${sidebarExpandida ? 'justify-center lg:px-6' : 'justify-center'}`}>
           <button 
             onClick={() => setSidebarExpandida(!sidebarExpandida)}
             className="p-2 text-kenth-subtext hover:text-kenth-text bg-kenth-surface/10 hover:bg-kenth-surface/30 rounded-lg transition-colors focus:outline-none"
             title={sidebarExpandida ? "Contraer menú" : "Expandir menú"}
           >
             <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
             </svg>
           </button>
        </div>

        {/* ICONS NAV */}
        <nav className={`flex flex-col gap-2 w-full px-4 mt-2 lg:mt-0 ${sidebarExpandida ? 'lg:px-6' : ''}`}>
          <NavItem 
            to="/dashboard" 
            label="Dashboard" 
            sidebarExpandida={sidebarExpandida}
            icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>} 
          />
          
          {/* Nota: Mi Ruta y Dashboard comparten URL por ahora, ambos se verán activos si la URL es /dashboard */}
          <NavItem 
            to="/dashboard" 
            label="Mi Ruta" 
            sidebarExpandida={sidebarExpandida}
            icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 14l9-5-9-5-9 5 9 5z" /><path strokeLinecap="round" strokeLinejoin="round" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" /><path strokeLinecap="round" strokeLinejoin="round" d="M12 14v6" /></svg>} 
          />

          <NavItem 
            to="/dashboard/tutor" 
            label="Tutor KENTH" 
            isRGB={true}
            sidebarExpandida={sidebarExpandida}
            icon={(props) => <AssistantIcon {...props} />} 
          />
          
          {(userRole === 'admin' || userRole === 'teacher') && (
            <>
              <NavItem 
                to="/dashboard/admin/knowledge" 
                label="Gestor IA" 
                sidebarExpandida={sidebarExpandida}
                icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>} 
              />
              <NavItem 
                to="/dashboard/admin/catalog" 
                label="Precios" 
                sidebarExpandida={sidebarExpandida}
                icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>} 
              />
            </>
          )}


          <NavItem 
            to="/dashboard/profile" 
            label="Ajustes" 
            sidebarExpandida={sidebarExpandida}
            icon={<svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>} 
          />
        </nav>
        
        {/* BOTÓN SALIR */}
        <div className="mt-auto p-4 w-full">
          <button onClick={handleLogout} className={`w-full flex items-center gap-3 rounded-xl text-kenth-brightred hover:bg-kenth-surface/20 transition group cursor-pointer justify-center ${sidebarExpandida ? 'lg:px-4 py-3 lg:justify-start' : 'p-3 lg:justify-center'}`}>
            <svg className="w-6 h-6 shrink-0 text-kenth-brightred group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
            <span className={`font-bold hidden ${sidebarExpandida ? 'lg:block' : 'hidden'}`}>Salir</span>
          </button>
        </div>
      </aside>

      {/* ÁREA PRINCIPAL */}
      <main className="flex-1 flex flex-col min-w-0 h-screen">
        
        <header className="h-20 shrink-0 flex justify-between items-center px-6 lg:px-10 border-b border-kenth-border relative z-30 bg-kenth-bg/80 backdrop-blur-md">
          <div></div> 
          
          <div className="flex items-center gap-6 ml-auto">
            
            {/* USER AVATAR + DROPDOWN MENU */}
            <div className="relative">
              <div 
                onClick={() => setMenuUsuarioAbierto(!menuUsuarioAbierto)}
                className="flex items-center gap-3 cursor-pointer hover:bg-kenth-surface/20 px-3 py-1.5 rounded-full transition"
              >
                <div className="w-8 h-8 rounded-full bg-kenth-surface overflow-hidden border-2 border-kenth-surface/50">
                  <img src={userAvatar} alt="user avatar" className="w-full h-full object-cover" />
                </div>
                <span className="font-semibold text-sm text-kenth-text">
                  {userName}
                </span>
                <svg className={`w-4 h-4 text-kenth-subtext transition-transform duration-300 ${menuUsuarioAbierto ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                </svg>
              </div>

              {/* El Menú Desplegable Flotante */}
              {menuUsuarioAbierto && (
                <>
                  <div 
                    className="fixed inset-0 z-40" 
                    onClick={() => setMenuUsuarioAbierto(false)}
                  ></div>
                  
                  <div className="absolute right-0 mt-2 w-48 bg-kenth-card border border-kenth-border rounded-xl shadow-[0_15px_40px_rgba(0,0,0,0.2)] z-50 py-2 animate-kenth-pop">
                    <Link 
                      to="/dashboard/profile" 
                      onClick={() => setMenuUsuarioAbierto(false)}
                      className="w-full text-left px-4 py-2.5 text-sm text-kenth-subtext hover:bg-kenth-surface/10 hover:text-kenth-text flex items-center gap-3 transition"
                    >
                      <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                      Editar Perfil
                    </Link>

                    <div className="h-px bg-kenth-border my-1"></div>
                    
                    <button 
                      onClick={handleLogout} 
                      className="w-full text-left px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 flex items-center gap-3 transition"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Cerrar Sesión
                    </button>
                  </div>
                </>
              )}
            </div>
            
            <ThemeToggle />

            {/* Search Bar */}
            <div className="relative hidden sm:block">
              <input type="text" placeholder="Buscar" className="bg-kenth-surface/10 border border-kenth-border rounded-full py-2 pl-4 pr-10 text-sm text-kenth-text focus:outline-none focus:border-kenth-brightred w-64 transition" />
              <svg className="w-4 h-4 text-kenth-subtext absolute right-4 top-1/2 transform -translate-y-1/2" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
          </div>
        </header>

        {/* Notificaciones Globales */}
        <Notification />

        {/* CONTENIDO DEL DASHBOARD */}
        <div className={`w-full flex-1 overflow-y-auto ${fullWidth ? 'p-0' : 'p-6 lg:p-12'}`}>
          <div className={`${fullWidth ? 'w-full h-full' : 'max-w-[1200px] mx-auto w-full'}`}>
            <AnimatePresence mode="wait">
              <motion.div
                key={location.pathname}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.25, ease: "easeOut" }}
                className={fullWidth ? 'h-full w-full' : ''}
              >
                {children}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>

      </main>
    </div>
  );
} 