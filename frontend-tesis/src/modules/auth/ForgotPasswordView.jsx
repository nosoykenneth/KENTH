import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Logo from '../../shared/components/ui/Logo';
import { requestPasswordReset } from '../../shared/services/authService';

export default function ForgotPasswordView() {
  const [identifier, setIdentifier] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [sent, setSent] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await requestPasswordReset(identifier.trim());
      setMessage(data.message || 'Si la cuenta existe, te enviamos un correo con instrucciones.');
      setSent(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-kenth-bg flex flex-col justify-center items-center font-sans p-4 relative overflow-hidden animate-kenth-blur">

      {/* BOTÓN REGRESAR */}
      <button
        onClick={() => navigate('/login')}
        className="absolute top-6 left-6 md:top-10 md:left-10 flex items-center gap-2 text-kenth-subtext hover:text-kenth-text transition-all font-bold text-xs md:text-sm uppercase tracking-[0.2em] group z-20"
      >
        <div className="w-8 h-8 rounded-full border border-kenth-border flex items-center justify-center group-hover:border-kenth-brightred group-hover:bg-kenth-brightred/10 transition-all">
          <svg className="w-4 h-4 transition-transform group-hover:-translate-x-0.5" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" /></svg>
        </div>
        <span className="hidden sm:inline">Iniciar sesión</span>
      </button>

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

        {/* CAJA */}
        <div className="bg-kenth-card/90 backdrop-blur-xl border border-kenth-border p-8 md:p-10 rounded-[2rem] shadow-[0_20px_50px_rgba(0,0,0,0.1)] animate-kenth-pop">

          {sent ? (
            <>
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 rounded-full bg-kenth-brightred/10 border border-kenth-brightred/30 flex items-center justify-center">
                  <svg className="w-8 h-8 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                </div>
              </div>
              <h2 className="text-2xl font-black text-kenth-text mb-3 uppercase tracking-tighter italic text-center">
                Revisa tu correo
              </h2>
              <p className="text-kenth-subtext text-center mb-8 text-sm leading-relaxed">
                {message}
              </p>
              <Link
                to="/login"
                className="w-full bg-kenth-brightred hover:bg-kenth-text hover:text-kenth-bg text-kenth-bg font-black py-4 rounded-2xl transition-all duration-500 shadow-xl shadow-kenth-brightred/20 uppercase tracking-tighter italic flex justify-center items-center"
              >
                Volver a iniciar sesión
              </Link>
            </>
          ) : (
            <>
              <h2 className="text-3xl font-black text-kenth-text mb-2 uppercase tracking-tighter italic text-center">
                ¿Olvidaste tu clave?
              </h2>
              <p className="text-kenth-subtext text-center mb-8 text-sm">
                Ingresa tu correo o usuario y te enviaremos un enlace para crear una nueva contraseña.
              </p>

              {error && (
                <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl mb-6 text-sm font-bold flex items-start gap-3">
                  <svg className="w-5 h-5 shrink-0 mt-0.5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                  <span>{error}</span>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">Usuario o Correo</label>
                  <input
                    type="text"
                    required
                    value={identifier}
                    onChange={(e) => setIdentifier(e.target.value)}
                    className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner placeholder:text-kenth-subtext"
                    placeholder="ejemplo@correo.com"
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
                          Enviando...
                        </>
                      ) : (
                        'Enviar enlace'
                      )}
                    </span>
                  </button>
                </div>
              </form>

              <p className="text-center mt-6 text-sm">
                <Link to="/login" className="text-kenth-subtext hover:text-kenth-brightred transition-colors font-bold">
                  Volver a iniciar sesión
                </Link>
              </p>
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
