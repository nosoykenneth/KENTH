import React, { useState, useEffect, useRef } from 'react';
import { showNotification } from '../../shared/components/ui/Notification';
import PageContainer from '../../shared/components/layout/PageContainer';
import AvatarCropper from '../../shared/components/ui/AvatarCropper';

const getProfileCropSourceKey = () => {
  const userId = localStorage.getItem('moodle_userid') || 'current';
  return `moodle_profile_crop_source_${userId}`;
};

const getProfileCropStateKey = () => {
  const userId = localStorage.getItem('moodle_userid') || 'current';
  return `moodle_profile_crop_state_${userId}`;
};

const readStoredCropState = () => {
  try {
    return JSON.parse(localStorage.getItem(getProfileCropStateKey()) || 'null');
  } catch {
    return null;
  }
};

const persistCropState = (cropState) => {
  if (!cropState?.areaPercentages) return;
  localStorage.setItem(getProfileCropStateKey(), JSON.stringify(cropState));
};

const toMoodleProxyUrl = (url) => {
  if (!url || url.startsWith('data:image')) return url;
  return url.replace(/^https?:\/\/localhost\//, '/api/lms/');
};

const prepareMoodleImageUrl = (url, token) => {
  const proxyUrl = toMoodleProxyUrl(url);
  if (!proxyUrl || proxyUrl.startsWith('data:image') || proxyUrl.includes('token=')) {
    return proxyUrl;
  }

  return proxyUrl + (proxyUrl.includes('?') ? `&token=${token}` : `?token=${token}`);
};

const bustImageCache = (url) => {
  if (!url || url.startsWith('data:image')) return url;
  return url + (url.includes('?') ? '&' : '?') + `_crop=${Date.now()}`;
};

export default function ProfileSettingsView() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  
  const [avatarPreview, setAvatarPreview] = useState('https://i.pravatar.cc/150?img=5');
  const [cropSourceImage, setCropSourceImage] = useState(null);
  const [imageToCrop, setImageToCrop] = useState(null);
  const [cropperInitialState, setCropperInitialState] = useState(null);
  const [profileCropState, setProfileCropState] = useState(() => readStoredCropState());
  const [pendingOriginalImage, setPendingOriginalImage] = useState('');
  const fileInputRef = useRef(null);
  
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    email: '',
    city: '',
    country: '',
    description: '',
    pictureData: ''
  });

  const token = localStorage.getItem('moodle_token');

  useEffect(() => {
    const cropSourceKey = getProfileCropSourceKey();
    const storedCropSource = prepareMoodleImageUrl(localStorage.getItem(cropSourceKey), token);
    if (storedCropSource) {
      setCropSourceImage(storedCropSource);
      localStorage.setItem(cropSourceKey, storedCropSource);
    }

    let currentPic = prepareMoodleImageUrl(localStorage.getItem('moodle_userpictureurl'), token);
    if (currentPic) {
      setAvatarPreview(currentPic);
    }

    fetch(`/api/lms/proyecto_curso/api_persistente/tesis_profile.php?token=${token}&action=get`)
      .then(res => res.json())
      .then(res => {
        if (res.success) {
          // Sanitizamos los datos para evitar nulls que rompan los inputs controlados
          const sanitizedData = {};
          Object.keys(res.data).forEach(key => {
            sanitizedData[key] = res.data[key] === null ? '' : res.data[key];
          });
          
          setFormData(prev => ({...prev, ...sanitizedData}));

          if (res.data.picturecropstate) {
            setProfileCropState(res.data.picturecropstate);
            persistCropState(res.data.picturecropstate);
          }
          
          if (res.data.originalpictureurl) {
            const editableUrl = prepareMoodleImageUrl(res.data.originalpictureurl, token);
            setCropSourceImage(editableUrl);
            localStorage.setItem(cropSourceKey, editableUrl);
          }

          if (res.data.pictureurl) {
            const picUrl = prepareMoodleImageUrl(res.data.pictureurl, token);
            setAvatarPreview(picUrl);
            localStorage.setItem('moodle_userpictureurl', picUrl);
            window.dispatchEvent(new Event('perfilActualizado')); 
          }
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Error al cargar perfil:", err);
        setLoading(false);
      });
  }, [token]);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 1024 * 1024 * 1024) {
        showNotification('error', 'La imagen es demasiado grande. Máximo 1GB.');
        e.target.value = '';
        return;
      }

      const reader = new FileReader();
      reader.onload = () => {
        setPendingOriginalImage(reader.result);
        setCropperInitialState(null);
        setImageToCrop(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCropComplete = (croppedImage, cropState) => {
    if (pendingOriginalImage) {
      setCropSourceImage(pendingOriginalImage);
      try {
        localStorage.setItem(getProfileCropSourceKey(), pendingOriginalImage);
      } catch (err) {
        console.warn('No se pudo persistir la imagen original para recorte:', err);
      }
    }

    if (cropState?.areaPercentages) {
      setProfileCropState(cropState);
      persistCropState(cropState);
      setFormData(prev => ({ ...prev, pictureCropState: cropState }));
    }

    setAvatarPreview(croppedImage);
    setFormData(prev => ({ ...prev, pictureData: croppedImage }));
    setImageToCrop(null);
    setCropperInitialState(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleCropCancel = () => {
    if (pendingOriginalImage) {
      setPendingOriginalImage('');
    }
    setImageToCrop(null);
    setCropperInitialState(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleEditCurrentCrop = () => {
    if (!cropSourceImage) {
      showNotification('error', 'No se pudo preparar la imagen actual para recorte.');
      return;
    }

    setCropperInitialState(profileCropState);
    setImageToCrop(bustImageCache(cropSourceImage));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      const payload = {
        ...formData,
        ...(profileCropState ? { pictureCropState: profileCropState } : {}),
        ...(pendingOriginalImage ? { pictureOriginalData: pendingOriginalImage } : {}),
      };

      const response = await fetch(`/api/lms/proyecto_curso/api_persistente/tesis_profile.php?token=${token}&action=update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const res = await response.json();

      if (res.success) {
        showNotification('success', '¡Perfil sincronizado con éxito!');
        localStorage.setItem('moodle_userfullname', res.newfullname);
        if (res.newpictureurl) {
          localStorage.setItem('moodle_userpictureurl', prepareMoodleImageUrl(res.newpictureurl, token));
        }
        if (res.originalpictureurl) {
          const editableUrl = prepareMoodleImageUrl(res.originalpictureurl, token);
          setCropSourceImage(editableUrl);
          localStorage.setItem(getProfileCropSourceKey(), editableUrl);
        }
        if (res.picturecropstate) {
          setProfileCropState(res.picturecropstate);
          persistCropState(res.picturecropstate);
        }
        setPendingOriginalImage('');
        window.dispatchEvent(new Event('perfilActualizado')); 
      } else {
        showNotification('error', res.error || 'Hubo un error al guardar');
      }
    } catch (err) {
      showNotification('error', 'Error de conexión con el servidor');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <PageContainer className="flex justify-center items-center">
         <svg className="animate-spin h-10 w-10 text-kenth-brightred" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
      </PageContainer>
    );
  }

  return (
    <>
      <PageContainer className="max-w-4xl">
      <h1 className="text-4xl md:text-5xl font-extrabold text-kenth-text mb-2 uppercase tracking-tighter italic">
        Ajustes de <span className="text-kenth-brightred">Perfil</span>
      </h1>
      <p className="text-kenth-subtext mb-8 font-medium">Gestiona tu identidad en la plataforma de mezcla y masterización.</p>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-kenth-card p-6 md:p-10 rounded-[2rem] border border-kenth-border shadow-[0_20px_50px_rgba(0,0,0,0.1)]">
        <div className="md:col-span-2 flex flex-col items-center justify-center mb-4">
          <div className="relative group cursor-pointer" onClick={() => fileInputRef.current.click()}>
            <div className="absolute -inset-1 bg-gradient-to-r from-kenth-brightred to-kenth-red rounded-full blur opacity-25 group-hover:opacity-60 transition duration-500"></div>
            <div className="relative w-32 h-32 rounded-full bg-kenth-surface/20 border-4 border-kenth-border overflow-hidden shadow-2xl">
              <img src={avatarPreview} alt="Tu Avatar" className="w-full h-full object-cover" />
              <div className="absolute inset-0 bg-kenth-bg/60 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              </div>
            </div>
          </div>
          <div className="mt-4 flex flex-wrap items-center justify-center gap-3">
            <button
              type="button"
              onClick={() => fileInputRef.current.click()}
              className="px-4 py-2 rounded-xl bg-kenth-surface/10 text-kenth-subtext hover:text-kenth-text hover:bg-kenth-surface/20 border border-kenth-border transition-all text-[10px] uppercase tracking-widest font-black"
            >
              Cambiar foto
            </button>

            <button
              type="button"
              onClick={handleEditCurrentCrop}
              className="px-4 py-2 rounded-xl bg-kenth-brightred/10 text-kenth-brightred hover:bg-kenth-brightred hover:text-white border border-kenth-brightred/20 transition-all text-[10px] uppercase tracking-widest font-black"
            >
              Editar recorte
            </button>
          </div>
          <input type="file" ref={fileInputRef} onChange={handleImageChange} accept="image/png, image/jpeg, image/jpg" className="hidden" />
        </div>

        <div className="space-y-2">
          <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">Nombre</label>
          <input type="text" className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner" value={formData.firstname || ''} onChange={(e) => setFormData(prev => ({...prev, firstname: e.target.value}))} required />
        </div>
        <div className="space-y-2">
          <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">Apellido</label>
          <input type="text" className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner" value={formData.lastname || ''} onChange={(e) => setFormData(prev => ({...prev, lastname: e.target.value}))} required />
        </div>
        <div className="space-y-2 md:col-span-2">
          <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">Correo Electrónico</label>
          <input type="email" className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner" value={formData.email || ''} onChange={(e) => setFormData(prev => ({...prev, email: e.target.value}))} required />
        </div>
        <div className="space-y-2">
          <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">Ciudad</label>
          <input type="text" className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all shadow-inner" value={formData.city || ''} onChange={(e) => setFormData(prev => ({...prev, city: e.target.value}))} />
        </div>
        <div className="space-y-2">
          <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">País (Código ISO: EC, ES, US...)</label>
          <input type="text" maxLength="2" className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all uppercase shadow-inner placeholder:text-kenth-subtext" placeholder="Ej: EC" value={formData.country || ''} onChange={(e) => setFormData(prev => ({...prev, country: e.target.value}))} />
        </div>
        <div className="space-y-2 md:col-span-2">
          <label className="text-xs font-black uppercase tracking-widest text-kenth-subtext ml-2">Biografía / Experiencia Musical</label>
          <textarea rows="5" className="w-full bg-kenth-surface/10 text-kenth-text border border-transparent focus:border-kenth-brightred p-4 rounded-2xl outline-none transition-all resize-none shadow-inner leading-relaxed" value={formData.description || ''} onChange={(e) => setFormData(prev => ({...prev, description: e.target.value}))} />
        </div>
        <div className="md:col-span-2 pt-4">
          <button type="submit" disabled={saving} className="w-full bg-kenth-brightred hover:bg-kenth-text hover:text-kenth-bg text-kenth-bg font-black py-4 md:py-5 rounded-2xl transition-all duration-500 shadow-xl shadow-kenth-brightred/20 uppercase tracking-tighter italic flex justify-center items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed group overflow-hidden relative">
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
      </PageContainer>

      {imageToCrop && (
        <AvatarCropper
          image={imageToCrop}
          onCropComplete={handleCropComplete}
          onCancel={handleCropCancel}
          variant="brand"
          initialCropState={cropperInitialState}
        />
      )}
    </>
  );
}
