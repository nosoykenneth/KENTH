import React, { useState, useEffect } from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';

export default function ProfileSettingsView() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    email: '',
    city: '',
    country: '',
    description: ''
  });

  const token = localStorage.getItem('moodle_token');

  // Cargar datos actuales desde Moodle al entrar a la página
  useEffect(() => {
    fetch(`/moodle_api/tesis_profile.php?token=${token}&action=get`)
      .then(res => res.json())
      .then(res => {
        if (res.success) setFormData(res.data);
        setLoading(false);
      });
  }, [token]);

  // Manejar el envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ type: '', text: '' });

    try {
      const response = await fetch(`/moodle_api/tesis_profile.php?token=${token}&action=update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const res = await response.json();

      if (res.success) {
        setMessage({ type: 'success', text: '¡Perfil sincronizado con éxito!' });
        // Actualizar el nombre en el header (para que el Navbar refleje el cambio al instante)
        localStorage.setItem('moodle_userfullname', res.newfullname);
        
        // Disparamos un evento personalizado para que el Navbar se entere del cambio (opcional, pero buena práctica)
        window.dispatchEvent(new Event('perfilActualizado')); 
      } else {
        setMessage({ type: 'error', text: res.error || 'Hubo un error al guardar' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Error de conexión con el servidor' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center h-64">
           <svg className="animate-spin h-10 w-10 text-kenth-brightred" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-2 uppercase tracking-tighter italic">
          Ajustes de <span className="text-kenth-brightred">Perfil</span>
        </h1>
        <p className="text-gray-400 mb-8 font-medium">Gestiona tu identidad en la plataforma de mezcla y masterización.</p>

        {/* Mensaje de éxito o error */}
        {message.text && (
          <div className={`p-4 rounded-xl mb-6 font-bold flex items-center gap-3 animate-in fade-in ${message.type === 'success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-red-500/10 text-red-400 border border-red-500/30'}`}>
            {message.type === 'success' ? (
               <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
            ) : (
               <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            )}
            {message.text}
          </div>
        )}

        {/* Formulario de Edición */}
        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-[#1e1e20] p-6 md:p-10 rounded-[2rem] border border-kenth-surface/20 shadow-[0_20px_50px_rgba(0,0,0,0.3)]">
          
          <div className="space-y-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Nombre</label>
            <input 
              type="text" 
              className="w-full bg-[#2D2D30] text-white border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner"
              value={formData.firstname}
              onChange={(e) => setFormData({...formData, firstname: e.target.value})}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Apellido</label>
            <input 
              type="text" 
              className="w-full bg-[#2D2D30] text-white border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner"
              value={formData.lastname}
              onChange={(e) => setFormData({...formData, lastname: e.target.value})}
              required
            />
          </div>

          <div className="space-y-2 md:col-span-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Correo Electrónico</label>
            <input 
              type="email" 
              className="w-full bg-[#2D2D30] text-white border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Ciudad</label>
            <input 
              type="text" 
              className="w-full bg-[#2D2D30] text-white border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner"
              value={formData.city}
              onChange={(e) => setFormData({...formData, city: e.target.value})}
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">País (Código ISO: EC, ES, US...)</label>
            <input 
              type="text" 
              maxLength="2"
              className="w-full bg-[#2D2D30] text-white border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all uppercase shadow-inner placeholder:text-gray-600"
              placeholder="Ej: EC"
              value={formData.country}
              onChange={(e) => setFormData({...formData, country: e.target.value})}
            />
          </div>

          <div className="space-y-2 md:col-span-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Biografía / Experiencia Musical</label>
            <textarea 
              rows="5"
              className="w-full bg-[#2D2D30] text-white border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all resize-none shadow-inner leading-relaxed"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
            />
          </div>

          <div className="md:col-span-2 pt-4">
            <button 
              type="submit" 
              disabled={saving}
              className="w-full bg-kenth-brightred hover:bg-white hover:text-kenth-bg text-white font-black py-4 md:py-5 rounded-2xl transition-all duration-500 shadow-xl shadow-kenth-brightred/20 uppercase tracking-tighter italic flex justify-center items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed group overflow-hidden relative"
            >
              {/* Brillo al pasar el mouse */}
              <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
              
              <span className="relative z-10 flex items-center gap-2">
                {saving ? (
                   <>
                    <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    Sincronizando...
                   </>
                ) : (
                  'Guardar Cambios'
                )}
              </span>
            </button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  );
}