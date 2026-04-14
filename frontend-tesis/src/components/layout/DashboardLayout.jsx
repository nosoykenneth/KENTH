import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import logoImg from '../../assets/logo-main.png';

export default function DashboardLayout({ children }) {
  // Estado para la barra lateral (abierta por defecto en PC)
  const [sidebarExpandida, setSidebarExpandida] = useState(true);
  
  // Estado para el menú desplegable del usuario (cerrado por defecto)
  const [menuUsuarioAbierto, setMenuUsuarioAbierto] = useState(false);
  
  const handleLogout = (e) => {
    e.preventDefault();
    localStorage.removeItem('moodle_token');
    localStorage.removeItem('moodle_rol');
    window.location.href = '/';
  };

  return (
    <div className="min-h-screen bg-kenth-bg text-white flex font-sans">
      
      {/* SIDEBAR DINÁMICO */}
      <aside 
        className={`
          border-r border-kenth-surface/30 bg-kenth-bg flex flex-col transition-all duration-300 z-20 shrink-0
          w-20 items-center
          ${sidebarExpandida ? 'lg:w-64 lg:items-start' : 'lg:w-20 lg:items-center'}
        `}
      >
        
        {/* LOGO */}
        <div className={`w-full flex items-center transition-all justify-center p-5 ${sidebarExpandida ? 'lg:p-8 lg:justify-center' : 'lg:p-5 lg:justify-center'}`}>
          <img 
            src={logoImg} 
            alt="KENTH Logo" 
            className={`w-auto object-contain transition-all h-10 ${sidebarExpandida ? 'lg:h-14' : 'lg:h-10'}`} 
          />
        </div>

        {/* BOTÓN HAMBURGUESA (Alineado perfectamente con los iconos) */}
        <div className={`hidden lg:flex w-full px-4 mb-4 ${sidebarExpandida ? 'justify-center lg:px-6' : 'justify-center'}`}>
           <button 
             onClick={() => setSidebarExpandida(!sidebarExpandida)}
             className="p-2 text-gray-400 hover:text-white bg-kenth-surface/10 hover:bg-kenth-surface/30 rounded-lg transition-colors focus:outline-none"
             title={sidebarExpandida ? "Contraer menú" : "Expandir menú"}
           >
             <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
             </svg>
           </button>
        </div>

        {/* ICONS NAV */}
        <nav className={`flex flex-col gap-4 w-full px-4 mt-2 lg:mt-0 ${sidebarExpandida ? 'lg:px-6' : ''}`}>
          <Link to="/dashboard" className={`p-3 bg-kenth-surface/30 rounded-xl flex items-center gap-4 text-white hover:bg-kenth-surface/50 transition shadow-inner justify-center ${sidebarExpandida ? 'lg:justify-start' : 'lg:justify-center'}`}>
            <svg className="w-6 h-6 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
            <span className={`font-semibold hidden ${sidebarExpandida ? 'lg:block' : 'hidden'}`}>Dashboard</span>
          </Link>
          <a href="#" className={`p-3 rounded-xl flex items-center gap-4 text-gray-400 hover:bg-kenth-surface/30 transition hover:text-white justify-center ${sidebarExpandida ? 'lg:justify-start' : 'lg:justify-center'}`}>
            <svg className="w-6 h-6 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 14l9-5-9-5-9 5 9 5z" /><path strokeLinecap="round" strokeLinejoin="round" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" /><path strokeLinecap="round" strokeLinejoin="round" d="M12 14v6" /></svg>
            <span className={`font-semibold hidden ${sidebarExpandida ? 'lg:block' : 'hidden'}`}>Cursos</span>
          </a>
          <a href="#" className={`p-3 rounded-xl flex items-center gap-4 text-gray-400 hover:bg-kenth-surface/30 transition hover:text-white justify-center ${sidebarExpandida ? 'lg:justify-start' : 'lg:justify-center'}`}>
            <svg className="w-6 h-6 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /><path strokeLinecap="round" strokeLinejoin="round" d="M9 9h1v1H9z" /></svg>
            <span className={`font-semibold hidden ${sidebarExpandida ? 'lg:block' : 'hidden'}`}>Recursos</span>
          </a>
          <a href="#" className={`p-3 rounded-xl flex items-center gap-4 text-gray-400 hover:bg-kenth-surface/30 transition hover:text-white justify-center ${sidebarExpandida ? 'lg:justify-start' : 'lg:justify-center'}`}>
            <svg className="w-6 h-6 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
            <span className={`font-semibold hidden ${sidebarExpandida ? 'lg:block' : 'hidden'}`}>Archivos</span>
          </a>
          <Link to="/dashboard/profile" className={`p-3 rounded-xl flex items-center gap-4 text-gray-400 hover:bg-kenth-surface/30 transition hover:text-white justify-center ${sidebarExpandida ? 'lg:justify-start' : 'lg:justify-center'}`}>
            <svg className="w-6 h-6 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            <span className={`font-semibold hidden ${sidebarExpandida ? 'lg:block' : 'hidden'}`}>Ajustes</span>
          </Link>
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
        
        {/* TOP NAVBAR (Limpia, sin botón hamburguesa extra) */}
        <header className="h-20 shrink-0 flex justify-between items-center px-6 lg:px-10 border-b border-kenth-surface/30 relative z-30">
          
          <div></div> {/* Espaciador para mantener el buscador y el avatar a la derecha */}
          
          <div className="flex items-center gap-6 ml-auto">
            
            {/* USER AVATAR + DROPDOWN MENU */}
            <div className="relative">
              <div 
                onClick={() => setMenuUsuarioAbierto(!menuUsuarioAbierto)}
                className="flex items-center gap-3 cursor-pointer hover:bg-kenth-surface/20 px-3 py-1.5 rounded-full transition"
              >
                <div className="w-8 h-8 rounded-full bg-kenth-surface overflow-hidden border-2 border-kenth-surface/50">
                  <img src="https://i.pravatar.cc/150?img=5" alt="user avatar" className="w-full h-full object-cover" />
                </div>
                <span className="font-semibold text-sm">
                  {localStorage.getItem('moodle_userfullname') || 'Administrador Usuario'}
                </span>
                <svg className={`w-4 h-4 text-gray-400 transition-transform duration-300 ${menuUsuarioAbierto ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
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
                  
                  <div className="absolute right-0 mt-2 w-48 bg-[#1e1e20] border border-kenth-surface/50 rounded-xl shadow-[0_15px_40px_rgba(0,0,0,0.6)] z-50 py-2 animate-in fade-in zoom-in-95 duration-200">
                    <Link 
                      to="/dashboard/profile" 
                      onClick={() => setMenuUsuarioAbierto(false)}
                      className="w-full text-left px-4 py-2.5 text-sm text-gray-300 hover:bg-white/5 hover:text-white flex items-center gap-3 transition"
                    >
                      <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                      Editar Perfil
                    </Link>

                    <div className="h-px bg-kenth-surface/30 my-1"></div>
                    
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
            
            {/* Search Bar */}
            <div className="relative hidden sm:block">
              <input type="text" placeholder="Buscar" className="bg-[#2a2a2d] border border-kenth-surface/30 rounded-full py-2 pl-4 pr-10 text-sm text-white focus:outline-none focus:border-kenth-brightred w-64 transition" />
              <svg className="w-4 h-4 text-gray-400 absolute right-4 top-1/2 transform -translate-y-1/2" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
          </div>
        </header>

        {/* CONTENIDO DEL DASHBOARD */}
        <div className="p-6 lg:p-12 w-full flex-1 overflow-y-auto">
          <div className="max-w-[1200px] mx-auto w-full">
            {children}
          </div>
        </div>

      </main>
    </div>
  );
}