import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';

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

  // Cargar datos actuales
  useEffect(() => {
    fetch(`/moodle_api/tesis_profile.php?token=${token}&action=get`)
      .then(res => res.json())
      .then(res => {
        if (res.success) setFormData(res.data);
        setLoading(false);
      });
  }, [token]);

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
        // Actualizar el nombre en el header
        localStorage.setItem('moodle_userfullname', res.newfullname);
      } else {
        setMessage({ type: 'error', text: res.error });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Error de conexión' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <DashboardLayout><div className="text-white">Cargando perfil...</div></DashboardLayout>;

  return (
    <DashboardLayout>
      <div className="max-w-4xl">
        <h1 className="text-4xl font-extrabold text-white mb-2 uppercase tracking-tighter italic">
          Ajustes de <span className="text-kenth-brightred">Perfil</span>
        </h1>
        <p className="text-gray-400 mb-8 font-medium">Gestiona tu identidad en la plataforma de mezcla y masterización.</p>

        {message.text && (
          <div className={`p-4 rounded-xl mb-6 font-bold ${message.type === 'success' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-red-500/20 text-red-400 border border-red-500/30'}`}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-[#1e1e20] p-8 rounded-[2rem] border border-kenth-surface/20 shadow-2xl">
          
          <div className="space-y-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Nombre</label>
            <input 
              type="text" 
              className="w-full bg-[#2D2D30] border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all"
              value={formData.firstname}
              onChange={(e) => setFormData({...formData, firstname: e.target.value})}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Apellido</label>
            <input 
              type="text" 
              className="w-full bg-[#2D2D30] border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all"
              value={formData.lastname}
              onChange={(e) => setFormData({...formData, lastname: e.target.value})}
              required
            />
          </div>

          <div className="space-y-2 md:col-span-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Correo Electrónico</label>
            <input 
              type="email" 
              className="w-full bg-[#2D2D30] border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Ciudad</label>
            <input 
              type="text" 
              className="w-full bg-[#2D2D30] border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all"
              value={formData.city}
              onChange={(e) => setFormData({...formData, city: e.target.value})}
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">País (Código ISO: EC, ES, US...)</label>
            <input 
              type="text" 
              maxLength="2"
              className="w-full bg-[#2D2D30] border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all uppercase"
              value={formData.country}
              onChange={(e) => setFormData({...formData, country: e.target.value})}
            />
          </div>

          <div className="space-y-2 md:col-span-2">
            <label className="text-xs font-black uppercase tracking-widest text-gray-500 ml-2">Biografía / Experiencia Musical</label>
            <textarea 
              rows="4"
              className="w-full bg-[#2D2D30] border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all resize-none"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
            />
          </div>

          <div className="md:col-span-2 pt-4">
            <button 
              type="submit" 
              disabled={saving}
              className="w-full bg-kenth-brightred hover:bg-white hover:text-kenth-bg text-white font-black py-4 rounded-2xl transition-all duration-500 shadow-xl shadow-kenth-brightred/20 uppercase tracking-tighter italic flex justify-center items-center gap-3"
            >
              {saving ? 'Sincronizando...' : 'Guardar Cambios'}
            </button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  );
}