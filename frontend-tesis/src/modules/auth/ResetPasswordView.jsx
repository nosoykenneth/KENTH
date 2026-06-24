import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import Logo from '../../shared/components/ui/Logo';
import { validateResetToken, confirmPasswordReset } from '../../shared/services/authService';

export default function ResetPasswordView() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token') || '';
  const navigate = useNavigate();

  // 'checking' | 'valid' | 'invalid' | 'done'
  const [status, setStatus] = useState('checking');
  const [emailMasked, setEmailMasked] = useState('');
  const [tokenError, setTokenError] = useState('');

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;

    if (!token) {
      setStatus('invalid');
      setTokenError('No se encontró un token de restablecimiento en el enlace.');
      return;
    }

    (async () => {
      try {
        const data = await validateResetToken(token);
        if (!active) return;
        setEmailMasked(data.email_masked || '');
        setStatus('valid');
      } catch (err) {
        if (!active) return;
        setTokenError(err.message);
        setStatus('invalid');
      }
    })();

    return () => { active = false; };
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Las contraseñas no coinciden.');
      return;
    }
    if (password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres.');
      return;
    }

    setLoading(true);
    try {
      await confirmPasswordReset(token, password);
      setStatus('done');
      // Redirección automática tras unos segundos.
      setTimeout(() => navigate('/login', { replace: true }), 3500);
    } catch (err) {
      setError(err.message);
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

        <div className="bg-kenth-card/90 backdrop-blur-xl border border-kenth-border p-8 md:p-10 rounded-[2rem] shadow-[0_20px_50px_rgba(0,0,0,0.1)] animate-kenth-pop">

          {status === 'checking' && (
            <div className="flex flex-col items-center py-8 gap-4">
              <svg className="animate-spin h-10 w-10 text-kenth-brightred" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              <p className="text-kenth-subtext text-sm font-bold uppercase tracking-widest">Verificando enlace...</p>
            </div>
          )}

          {status === 'invalid' && (
            <>
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 rounded-full bg-red-500/10 border border-red-500/30 flex items-center justify-center">
                  <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                </div>
              </div>
              <h2 className="text-2xl font-black text-kenth-text mb-3 uppercase tracking-tighter italic text-center">
                Enlace no válido
              </h2>
              <p className="text-kenth-subtext text-center mb-8 text-sm leading-relaxed">
                {tokenError}
              </p>
              <Link
                to="/forgot-password"
                className="w-full bg-kenth-brightred hover:bg-kenth-text hover:text-kenth-bg text-kenth-bg font-black py-4 rounded-2xl transition-all duration-500 shadow-xl shadow-kenth-brightred/20 uppercase tracking-tighter italic flex justify-center items-center"
              >
                Solicitar uno nuevo
              </Link>
            </>
          )}

          {status === 'done' && (
            <>
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 rounded-full bg-green-500/10 border border-green-500/30 flex items-center justify-center">
                  <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                </div>
              </div>
              <h2 className="text-2xl font-black text-kenth-text mb-3 uppercase tracking-tighter italic text-center">
                ¡Contraseña actualizada!
              </h2>
              <p className="text-kenth-subtext text-center mb-8 text-sm leading-relaxed">
                Ya puedes iniciar sesión con tu nueva contraseña. Te redirigiremos en un momento...
              </p>
              <Link
                to="/login"
                className="w-full bg-kenth-brightred hover:bg-kenth-text hover:text-kenth-bg text-kenth-bg font-black py-4 rounded-2xl transition-all duration-500 shadow-xl shadow-kenth-brightred/20 uppercase tracking-tighter italic flex justify-center items-center"
              >
                Iniciar sesión
              </Link>
            </>
          )}

          {status === 'valid' && (
            <>
              <h2 className="text-3xl font-black text-kenth-text mb-2 uppercase tracking-tighter italic text-center">
                Nueva contraseña
              </h2>
              <p className="text-kenth-subtext text-center mb-8 text-sm">
                {emailMasked
                  ? <>Crea una contraseña nueva para <span className="text-kenth-text font-bold">{emailMasked}</span>.</>
                  : 'Crea una contraseña nueva y segura para tu cuenta.'}
              </p>

              {error && (
                <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl mb-6 text-sm font-bold flex items-start gap-3">
                  <svg className="w-5 h-5 shrink-0 mt-0.5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                  <span>{error}</span>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">Nueva Contraseña</label>
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner placeholder:text-kenth-subtext"
                    placeholder="••••••••"
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">Confirmar Contraseña</label>
                  <input
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
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
                          <svg className="animate-spin h-5 w-5 text-kenth-bg" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                          Guardando...
                        </>
                      ) : (
                        'Cambiar contraseña'
                      )}
                    </span>
                  </button>
                </div>
              </form>
            </>
          )}
        </div>

        {/* Footer */}
        <p className="text-center text-kenth-subtext text-xs mt-8 font-bold tracking-widest uppercase">
          KENTH Academy © {new Date().getFullYear()}
        </p>
      </div>
    </div>
  );
}
