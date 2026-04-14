import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { login, getSiteInfo } from '@/features/auth/services/authService';
import { logoMain } from '@/shared/assets';
import { setMoodleToken, setMoodleUserProfile } from '@/shared/lib/moodleSession';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorEnvio, setErrorEnvio] = useState('');
  const [cargando, setCargando] = useState(false);
  const navigate = useNavigate();

  const manejarLogin = async (e) => {
    e.preventDefault();
    setErrorEnvio('');
    setCargando(true);

    try {
      // 1. Iniciar sesión y obtener token
      const token = await login(username, password);
      setMoodleToken(token);

      // 2. Obtener información de usuario cruzando el token
      try {
        const infoData = await getSiteInfo(token);
        if (infoData.userid) {
          setMoodleUserProfile({
            userId: infoData.userid,
            fullName: infoData.fullname,
          });
        }
      } catch (err) {
        console.warn("No se pudo obtener el perfil del site:", err.message);
      }

      // 3. Redirigir al panel principal
      navigate('/dashboard');

    } catch (error) {
       console.error("Fallo de acceso:", error);
       setErrorEnvio(error.message || "No se pudo conectar con el servidor Moodle.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="min-h-screen bg-kenth-bg flex flex-col font-sans">
      <header className="flex justify-start p-6 absolute top-0 w-full z-10 w-auto object-contain">
        <Link to="/">
          <img src={logoMain} alt="KENTH Logo" className="h-10 md:h-12 w-auto object-contain" />
        </Link>
      </header>

      <main className="flex-grow flex items-center justify-center p-4">
        <div className="bg-[#2D2D30] rounded-[2rem] p-8 md:p-12 w-full max-w-md border border-kenth-surface/20 shadow-2xl relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-64 h-64 bg-kenth-brightred/10 rounded-full blur-[100px] pointer-events-none"></div>

          <div className="relative z-10 text-center mb-8">
            <h1 className="text-3xl font-extrabold text-white tracking-widest uppercase mb-2">Ingresar</h1>
            <p className="text-gray-400 text-sm font-light">Accede al panel mediante tus credenciales de Moodle</p>
          </div>

          <form onSubmit={manejarLogin} className="flex flex-col gap-6 relative z-10">
            <div>
              <label className="text-xs font-semibold text-gray-400 mb-2 block uppercase tracking-wider">Usuario / Username</label>
              <input 
                type="text" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Ej: admin"
                required
                className="w-full bg-[#1e1e20] text-white border border-kenth-surface/30 rounded-xl p-4 focus:outline-none focus:border-kenth-brightred transition shadow-inner font-light"
              />
            </div>
            
            <div>
              <label className="text-xs font-semibold text-gray-400 mb-2 block uppercase tracking-wider">Contraseña / Password</label>
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full bg-[#1e1e20] text-white border border-kenth-surface/30 rounded-xl p-4 focus:outline-none focus:border-kenth-brightred transition shadow-inner font-light"
              />
            </div>

            <button 
              type="submit" 
              disabled={cargando}
              className="bg-kenth-brightred hover:bg-kenth-red text-white py-4 rounded-xl font-bold transition flex items-center justify-center gap-2 disabled:opacity-50 mt-2 shadow-lg w-full uppercase tracking-widest text-sm"
            >
              {cargando ? (
                <span className="flex items-center gap-2">
                   <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24">
                     <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                     <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                   </svg>
                   Conectando a Moodle...
                </span>
              ) : (
                'Iniciar Sesión'
              )}
            </button>
            
            {errorEnvio && (
              <div className="mt-2 p-4 bg-red-900/20 border-l-4 border-kenth-brightred rounded-r-lg text-red-200">
                <p className="font-semibold text-sm">⛔ {errorEnvio}</p>
              </div>
            )}
            
          </form>
        </div>
      </main>
    </div>
  );
}
