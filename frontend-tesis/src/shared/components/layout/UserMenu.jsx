import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function UserMenu({ isCompact = false }) {
  const navigate = useNavigate();
  const [menuUsuarioAbierto, setMenuUsuarioAbierto] = useState(false);
  const [userName, setUserName] = useState(() => localStorage.getItem('moodle_userfullname') || 'Usuario');
  const [userAvatar, setUserAvatar] = useState(() => {
    let picUrl = localStorage.getItem('moodle_userpictureurl') || 'https://i.pravatar.cc/150?img=5';
    const token = localStorage.getItem('moodle_token');
    if (picUrl && token && !picUrl.includes('token=') && picUrl.includes('http')) {
      picUrl += picUrl.includes('?') ? `&token=${token}` : `?token=${token}`;
    }
    return picUrl;
  });

  useEffect(() => {
    const cargarDatosUsuario = () => {
      const nombre = localStorage.getItem('moodle_userfullname');
      if (nombre) setUserName(nombre);
      let picUrl = localStorage.getItem('moodle_userpictureurl');
      const token = localStorage.getItem('moodle_token');
      if (picUrl && token && !picUrl.includes('token=')) {
        picUrl += picUrl.includes('?') ? `&token=${token}` : `?token=${token}`;
      }
      if (picUrl) setUserAvatar(picUrl);
    };
    cargarDatosUsuario();
    window.addEventListener('perfilActualizado', cargarDatosUsuario);
    return () => window.removeEventListener('perfilActualizado', cargarDatosUsuario);
  }, []);

  const handleLogout = (e) => {
    e.preventDefault();
    localStorage.removeItem('moodle_token');
    localStorage.removeItem('moodle_rol');
    localStorage.removeItem('moodle_userfullname');
    localStorage.removeItem('moodle_userid');
    localStorage.removeItem('moodle_userpictureurl');
    window.location.href = '/';
  };

  return (
    <div className="relative">
      <div 
        onClick={() => setMenuUsuarioAbierto(!menuUsuarioAbierto)} 
        className={`flex items-center gap-3 cursor-pointer hover:bg-kenth-surface/20 px-3 py-1.5 rounded-full transition ${isCompact ? 'md:px-2' : ''}`}
      >
        <div className="w-8 h-8 rounded-full bg-kenth-surface overflow-hidden border-2 border-kenth-surface/50 shrink-0">
          <img src={userAvatar} alt="user avatar" className="w-full h-full object-cover" />
        </div>
        {!isCompact && (
          <>
            <span className="font-bold text-sm text-kenth-text hidden md:block whitespace-nowrap uppercase tracking-tighter italic">
              {userName}
            </span>
            <svg className={`w-4 h-4 text-kenth-subtext transition-transform duration-300 hidden md:block ${menuUsuarioAbierto ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </>
        )}
      </div>

      {menuUsuarioAbierto && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setMenuUsuarioAbierto(false)}></div>
          <div className="absolute right-0 mt-2 w-56 bg-kenth-card border border-kenth-border rounded-xl shadow-[0_20px_50px_rgba(0,0,0,0.3)] z-50 py-2 animate-kenth-pop overflow-hidden">
            <div className="px-4 py-3 border-b border-kenth-border mb-1 bg-kenth-surface/5">
               <p className="text-[10px] uppercase tracking-widest font-black text-kenth-brightred mb-1">Sesión iniciada</p>
               <p className="text-xs font-bold text-kenth-text truncate">{userName}</p>
            </div>
            <Link to="/dashboard/profile" onClick={() => setMenuUsuarioAbierto(false)} className="w-full text-left px-4 py-3 text-sm text-kenth-subtext hover:bg-kenth-surface/10 hover:text-kenth-text flex items-center gap-3 transition">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
              Ajustes de Perfil
            </Link>
            <div className="h-px bg-kenth-border my-1"></div>
            <button onClick={handleLogout} className="w-full text-left px-4 py-3 text-sm text-red-500 hover:bg-red-500/10 hover:text-red-400 flex items-center gap-3 transition font-black uppercase tracking-tighter italic">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
              Cerrar Sesión
            </button>
          </div>
        </>
      )}
    </div>
  );
}
