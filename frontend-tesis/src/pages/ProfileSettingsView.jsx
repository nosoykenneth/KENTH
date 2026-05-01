import React, { useState, useEffect, useRef } from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';

export default function ProfileSettingsView() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  // Estado para la previsualización visual de la foto
  const [avatarPreview, setAvatarPreview] = useState('https://i.pravatar.cc/150?img=5'); // Fallback inicial
  const fileInputRef = useRef(null);
  
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    email: '',
    city: '',
    country: '',
    description: '',
    pictureData: '' // Aquí guardaremos la imagen en Base64 para enviarla
  });

  const token = localStorage.getItem('moodle_token');

  // Cargar datos actuales desde Moodle al entrar a la página
  useEffect(() => {
    // 1. Cargar la foto actual desde el localStorage para que sea instantáneo
    let currentPic = localStorage.getItem('moodle_userpictureurl');
    if (currentPic) {
      // Si la URL de Moodle no tiene el token, se lo agregamos para evitar el error de acceso denegado (403)
      if (!currentPic.includes('token=')) {
        currentPic += currentPic.includes('?') ? `&token=${token}` : `?token=${token}`;
      }
      setAvatarPreview(currentPic);
    }

    // 2. Traer el resto de los datos del PHP
    fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_profile.php?token=${token}&action=get`)
      .then(res => res.json())
      .then(res => {
        if (res.success) {
          setFormData(prev => ({...prev, ...res.data}));
          if (res.data.pictureurl) {
            let picUrl = res.data.pictureurl;
            if (!picUrl.includes('token=')) {
              picUrl += picUrl.includes('?') ? `&token=${token}` : `?token=${token}`;
            }
            setAvatarPreview(picUrl);
            localStorage.setItem('moodle_userpictureurl', picUrl);
            window.dispatchEvent(new Event('perfilActualizado')); 
          }
        }
        setLoading(false);
      });
  }, [token]);

  // Manejar el cambio de imagen
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validación básica (opcional, pero recomendada)
      if (file.size > 5 * 1024 * 1024) { // 5MB
        setMessage({ type: 'error', text: 'La imagen es demasiado grande. Máximo 5MB.' });
        return;
      }

      // 1. Mostrar la previsualización al usuario instantáneamente
      const objectUrl = URL.createObjectURL(file);
      setAvatarPreview(objectUrl);

      // 2. Convertir a Base64 para enviarlo en el JSON
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData(prev => ({ ...prev, pictureData: reader.result }));
      };
      reader.readAsDataURL(file);
    }
  };

  const removePhoto = () => {
  setAvatarPreview(null);
  setFormData(prev => ({ 
    ...prev, 
    pictureData: '', 
    deletePicture: true 
  }));
};

  // Manejar el envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ type: '', text: '' });

    try {
      const response = await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_profile.php?token=${token}&action=update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const res = await response.json();

      if (res.success) {
        setMessage({ type: 'success', text: '¡Perfil sincronizado con éxito!' });
        
        // Actualizar el nombre en el header
        localStorage.setItem('moodle_userfullname', res.newfullname);
        
        // Si el PHP devolvió la nueva URL de la imagen, la actualizamos en el header
        if (res.newpictureurl) {
          localStorage.setItem('moodle_userpictureurl', res.newpictureurl);
        }
        
        // Disparamos el evento para que el Navbar se entere del cambio (Nombre y Foto)
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

        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-[#1e1e20] p-6 md:p-10 rounded-[2rem] border border-kenth-surface/20 shadow-[0_20px_50px_rgba(0,0,0,0.3)]">
          
          {/* SECCIÓN DE LA FOTO (Ocupa 2 columnas al principio) */}
          <div className="md:col-span-2 flex flex-col items-center justify-center mb-4">
            <div className="relative group cursor-pointer" onClick={() => fileInputRef.current.click()}>
              {/* Brillo de fondo */}
              <div className="absolute -inset-1 bg-gradient-to-r from-kenth-brightred to-kenth-red rounded-full blur opacity-25 group-hover:opacity-60 transition duration-500"></div>
              
              {/* Avatar */}
              <div className="relative w-32 h-32 rounded-full bg-[#2D2D30] border-4 border-kenth-surface/50 overflow-hidden shadow-2xl">
                <img src={avatarPreview} alt="Tu Avatar" className="w-full h-full object-cover" />
                
                {/* Overlay Oscuro on Hover */}
                <div className="absolute inset-0 bg-black/60 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                </div>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-4 uppercase tracking-widest font-bold">Clic para cambiar foto</p>
            
            {/* Input de archivo invisible */}
            <input 
              type="file" 
              ref={fileInputRef}
              onChange={handleImageChange}
              accept="image/png, image/jpeg, image/jpg" 
              className="hidden" 
            />
          </div>

          {/* EL RESTO DE TUS CAMPOS NORMALES */}
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