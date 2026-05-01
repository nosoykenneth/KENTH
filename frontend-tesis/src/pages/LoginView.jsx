import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import logoImg from '../assets/logo-main.png';
import Logo from '../components/ui/Logo';

// IMPORTAMOS TUS FUNCIONES REALES
import { login, getSiteInfo, helperDetermineRole } from '../services/authService';

export default function LoginView() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || '/dashboard';

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // 1. Usamos TU función de login (que ya pasa por el proxy a api_tesis)
      const token = await login(username, password);
      
      // 2. Guardamos el token
      localStorage.setItem('moodle_token', token);

      // 3. Usamos TU función para obtener la info del sitio y del usuario
      const siteInfo = await getSiteInfo(token);
      localStorage.setItem('moodle_userfullname', siteInfo.fullname);
      // ¡NUEVO! Guardamos el ID del usuario para poder pedir sus cursos después
      localStorage.setItem('moodle_userid', siteInfo.userid);
      
      let picUrl = siteInfo.userpictureurl || '';
      if (picUrl && !picUrl.includes('token=')) {
        picUrl += picUrl.includes('?') ? `&token=${token}` : `?token=${token}`;
      }
      localStorage.setItem('moodle_userpictureurl', picUrl);
      
      // 4. Determinamos el rol temporalmente usando tu helper
      const role = helperDetermineRole(username);
      localStorage.setItem('moodle_rol', role);

      // 5. Redirigimos al destino original o al dashboard
      navigate(from, { replace: true });

    } catch (err) {
      // AQUÍ ESTÁ LA MAGIA: Si Moodle se queja, te mostrará su QUEJA EXACTA, no un invento mío.
      setError(`Error del servidor: ${err.message}`);
      
      // Limpiamos rastros si falla
      localStorage.removeItem('moodle_token');
      localStorage.removeItem('moodle_userfullname');
      localStorage.removeItem('moodle_rol');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-kenth-bg flex flex-col justify-center items-center font-sans p-4 relative overflow-hidden animate-kenth-blur">
      
      {/* Luces de fondo estilo estudio */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-kenth-brightred/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-kenth-surface/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="w-full max-w-md z-10">
        
        {/* LOGO */}
        <div className="flex justify-center mb-8 animate-kenth-slide">
          <Link to="/">
            <Logo className="h-12 md:h-16" />
          </Link>
        </div>

        {/* CAJA DE LOGIN */}
        <div className="bg-kenth-card/90 backdrop-blur-xl border border-kenth-border p-8 md:p-10 rounded-[2rem] shadow-[0_20px_50px_rgba(0,0,0,0.1)] animate-kenth-pop">
          
          <h2 className="text-3xl font-black text-kenth-text mb-2 uppercase tracking-tighter italic text-center">
            Bienvenido
          </h2>
          <p className="text-kenth-subtext text-center mb-8 text-sm">
            Inicia sesión para acceder a tu estudio virtual.
          </p>

          {/* MENSAJE DE ERROR REAL */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl mb-6 text-sm font-bold flex items-start gap-3">
              <svg className="w-5 h-5 shrink-0 mt-0.5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-5">
            
            <div className="space-y-2">
              <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">Usuario o Correo</label>
              <input 
                type="text" 
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner placeholder:text-kenth-subtext"
                placeholder="ejemplo@correo.com"
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-center ml-2">
                <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext">Contraseña</label>
                <a href="#" className="text-xs text-kenth-subtext hover:text-kenth-brightred transition-colors">¿Olvidaste tu clave?</a>
              </div>
              <input 
                type="password" 
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner placeholder:text-kenth-subtext"
                placeholder="••••••••"
              />
            </div>

            <div className="pt-4">
              <button 
                type="submit" 
                disabled={loading}
                className="w-full bg-kenth-brightred hover:bg-kenth-text hover:text-kenth-bg text-kenth-bg font-black py-4 rounded-2xl transition-all duration-500 shadow-xl shadow-kenth-brightred/20 uppercase tracking-tighter italic flex justify-center items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed group overflow-hidden relative"
              >
                <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
                <span className="relative z-10 flex items-center gap-2">
                  {loading ? (
                    <>
                      <svg className="animate-spin h-5 w-5 text-kenth-bg group-hover:text-kenth-bg" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                      Entrando...
                    </>
                  ) : (
                    'Ingresar'
                  )}
                </span>
              </button>
            </div>
          </form>

        </div>
        
        {/* Footer del Login */}
        <p className="text-center text-kenth-subtext text-xs mt-8 font-bold tracking-widest uppercase">
          KENTH Academy © {new Date().getFullYear()}
        </p>

      </div>
    </div>
  );
}