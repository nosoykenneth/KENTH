import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { completeOnboarding } from '../../shared/services/authService';
import Logo from '../../shared/components/ui/Logo';

export default function OnboardingWizard() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Form State
  const [formData, setFormData] = useState({
    firstname: localStorage.getItem('moodle_userfullname')?.split(' ')[0] || '',
    lastname: localStorage.getItem('moodle_userfullname')?.split(' ').slice(1).join(' ') || '',
    pictureData: '',
    password: '',
    confirmPassword: ''
  });

  const [photoPreview, setPhotoPreview] = useState(null);
  const fileInputRef = React.useRef(null);

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Preview inmediato con ObjectURL (como en ProfileSettings)
      const objectUrl = URL.createObjectURL(file);
      setPhotoPreview(objectUrl);

      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData(prev => ({ ...prev, pictureData: reader.result }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFinish = async () => {
    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }
    if (formData.password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    setLoading(true);
    setError('');
    const token = localStorage.getItem('moodle_token');

    try {
      const res = await completeOnboarding(token, formData);

      localStorage.setItem('moodle_requires_onboarding', '0');
      localStorage.setItem('moodle_userfullname', `${formData.firstname} ${formData.lastname}`);

      if (res?.newpictureurl) {
        localStorage.setItem('moodle_userpictureurl', res.newpictureurl);
        window.dispatchEvent(new Event('perfilActualizado'));
      }

      navigate('/dashboard', { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const steps = [
    {
      id: 1,
      title: "Tu Identidad",
      subtitle: "Confirma cómo aparecerás en tu certificado y en la comunidad.",
      content: (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-[10px] font-black uppercase tracking-widest text-indigo-400/60 ml-2">Nombre</label>
              <input
                type="text"
                value={formData.firstname}
                onChange={(e) => setFormData({ ...formData, firstname: e.target.value })}
                className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-indigo-500 transition-all text-white font-bold"
              />
            </div>
            <div className="space-y-2">
              <label className="text-[10px] font-black uppercase tracking-widest text-indigo-400/60 ml-2">Apellido</label>
              <input
                type="text"
                value={formData.lastname}
                onChange={(e) => setFormData({ ...formData, lastname: e.target.value })}
                className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-indigo-500 transition-all text-white font-bold"
              />
            </div>
          </div>
        </div>
      )
    },
    {
      id: 2,
      title: "Foto de Perfil",
      subtitle: "Una imagen ayuda a tus tutores y compañeros a reconocerte.",
      content: (
        <div className="flex flex-col items-center space-y-6">
          <div
            className="relative group cursor-pointer"
            onClick={() => fileInputRef.current.click()}
          >
            <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full blur opacity-25 group-hover:opacity-60 transition duration-500"></div>
            <div className="relative w-32 h-32 rounded-full border-4 border-white/10 overflow-hidden bg-white/5 flex items-center justify-center shadow-[0_0_40px_rgba(79,70,229,0.2)]">
              {photoPreview ? (
                <img src={photoPreview} alt="Preview" className="w-full h-full object-cover" />
              ) : (
                <svg className="w-12 h-12 text-white/20" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>
              )}

              <div className="absolute inset-0 bg-indigo-600/60 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              </div>
            </div>
          </div>
          <input
            type="file"
            ref={fileInputRef}
            className="hidden"
            onChange={handlePhotoChange}
            accept="image/png, image/jpeg, image/jpg"
          />
          <p className="text-xs text-white/40 font-black uppercase tracking-widest">Haz clic en el círculo para subir foto</p>
        </div>
      )
    },
    {
      id: 3,
      title: "Seguridad",
      subtitle: "Crea una contraseña nueva y segura para tu cuenta.",
      content: (
        <div className="space-y-4">
          <div className="space-y-2">
            <label className="text-[10px] font-black uppercase tracking-widest text-indigo-400/60 ml-2">Nueva Contraseña</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              placeholder="••••••••"
              className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-indigo-500 transition-all text-white font-bold"
            />
          </div>
          <div className="space-y-2">
            <label className="text-[10px] font-black uppercase tracking-widest text-indigo-400/60 ml-2">Confirmar Contraseña</label>
            <input
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
              placeholder="••••••••"
              className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-indigo-500 transition-all text-white font-bold"
            />
          </div>
        </div>
      )
    }
  ];

  return (
    <div className="min-h-screen bg-[#050505] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Luces de fondo */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="absolute -top-24 -left-24 w-96 h-96 bg-indigo-600/10 rounded-full blur-[120px]"></div>
        <div className="absolute -bottom-24 -right-24 w-96 h-96 bg-indigo-900/10 rounded-full blur-[120px]"></div>
      </div>

      <div className="w-full max-w-xl z-10">
        <div className="flex justify-center mb-12">
          <Logo className="h-10 opacity-80" />
        </div>

        <div className="bg-[#0f0f0f] border border-white/5 rounded-[2.5rem] p-8 md:p-12 shadow-2xl relative">

          {/* Progress Bar */}
          <div className="flex gap-2 mb-12">
            {[1, 2, 3].map((s) => (
              <div key={s} className={`h-1 flex-1 rounded-full transition-all duration-500 ${s <= step ? 'bg-indigo-500 shadow-[0_0_10px_rgba(79,70,229,0.5)]' : 'bg-white/5'}`}></div>
            ))}
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={step}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.4, ease: "easeOut" }}
            >
              <header className="mb-10">
                <span className="text-[10px] font-black uppercase tracking-[0.3em] text-indigo-400 mb-2 block">Paso {step} de 3</span>
                <h2 className="text-4xl font-black text-white uppercase tracking-tighter italic">{steps[step - 1].title}</h2>
                <p className="text-white/40 mt-2 font-medium">{steps[step - 1].subtitle}</p>
              </header>

              {steps[step - 1].content}

              {error && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-6 bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-2xl text-xs font-bold flex items-center gap-3"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                  {error}
                </motion.div>
              )}

              <footer className="mt-12 flex justify-between items-center gap-4">
                {step > 1 ? (
                  <button
                    onClick={() => setStep(step - 1)}
                    className="text-white/40 hover:text-white font-bold text-xs uppercase tracking-widest transition-colors px-6 py-4"
                  >
                    Anterior
                  </button>
                ) : <div />}

                <button
                  onClick={step === 3 ? handleFinish : () => setStep(step + 1)}
                  disabled={loading}
                  className="bg-white text-black hover:bg-indigo-500 hover:text-white px-10 py-5 rounded-2xl font-black text-xs uppercase tracking-widest transition-all shadow-xl active:scale-95 disabled:opacity-50 flex items-center gap-3 group"
                >
                  {loading ? (
                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                  ) : step === 3 ? 'Finalizar' : 'Continuar'}
                  <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                </button>
              </footer>
            </motion.div>
          </AnimatePresence>

        </div>

        <p className="text-center text-white/10 text-[10px] font-black uppercase tracking-[0.4em] mt-12">
          KENTH Studio • Configuración Inicial
        </p>
      </div>
    </div>
  );
}
