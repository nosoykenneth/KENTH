import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import { getCourseSettings, updateCourseSettings, getMyCourses, getCategories } from '../services/courseService';
import { showNotification } from '../components/ui/Notification';

export default function CourseSettingsView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const token = localStorage.getItem('moodle_token');
  const userId = localStorage.getItem('moodle_userid');

  const [formData, setFormData] = useState({
    fullname: '',
    shortname: '',
    summary: '',
    visible: 1,
    imageData: null, // Base64
    currentImageUrl: '',
    pos_y: 50,
    category: 1
  });
  const [categories, setCategories] = useState([]);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showReposition, setShowReposition] = useState(false);

  const fileInputRef = useRef(null);
  const dragRef = useRef({ isDragging: false, startY: 0, startPos: 50 });

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const [data, misCursos, allCats] = await Promise.all([
          getCourseSettings(token, id),
          userId ? getMyCourses(token, userId) : Promise.resolve([]),
          getCategories(token)
        ]);

        // Buscar la imagen real que ve el catálogo
        const cursoActual = misCursos.find(c => c.id == id);
        const imagenReal = cursoActual?.courseimage || data.courseimage;

        setCategories(allCats);
        setFormData({
          fullname: data.fullname,
          shortname: data.shortname,
          summary: data.summary || '',
          visible: data.visible,
          category: data.category || 1,
          imageData: null,
          currentImageUrl: imagenReal,
          pos_y: data.pos_y || 50,
          categoryname: cursoActual?.categoryname || 'CURSO'
        });
      } catch (err) {
        showNotification('error', 'No se pudieron cargar los ajustes.');
      } finally {
        setLoading(false);
      }
    };
    fetchSettings();
  }, [id, token, userId]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 1024 * 1024 * 1024) {
        showNotification('error', 'La imagen es demasiado grande. Máximo 1GB.');
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        // Comprimir la imagen antes de enviarla
        const img = new Image();
        img.src = reader.result;
        img.onload = () => {
          const canvas = document.createElement('canvas');
          let width = img.width;
          let height = img.height;

          // Redimensionar si es muy grande (max 1920px ancho)
          const MAX_WIDTH = 1920;
          if (width > MAX_WIDTH) {
            height = Math.round(height * (MAX_WIDTH / width));
            width = MAX_WIDTH;
          }

          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);

          // Comprimir a JPEG con 80% de calidad
          const compressedBase64 = canvas.toDataURL('image/jpeg', 0.8);
          setFormData(prev => ({ ...prev, imageData: compressedBase64 }));
          setShowReposition(true); // Abrir el reposicionador al subir imagen
        };
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    setSaving(true);

    try {
      await updateCourseSettings(token, id, {
        fullname: formData.fullname,
        shortname: formData.shortname,
        summary: formData.summary,
        visible: formData.visible,
        category: formData.category,
        imageData: formData.imageData,
        pos_y: formData.pos_y
      });
      showNotification('success', '¡Ajustes guardados correctamente!');

      // EL TRUCO OPTIMISTA: 
      // Pasamos la previsualización a la imagen oficial y quitamos la etiqueta "Nueva"
      if (formData.imageData) {
        setFormData(prev => ({
          ...prev,
          currentImageUrl: prev.imageData, // Base64 se vuelve la imagen actual
          imageData: null // Limpiamos el buffer temporal
        }));
      }
    } catch (err) {
      showNotification('error', err.message);
    } finally {
      setSaving(false);
    }
  };

  // Lógica de arrastre para reposicionar
  const handleMouseDown = (e) => {
    dragRef.current.isDragging = true;
    dragRef.current.startY = e.clientY;
    dragRef.current.startPos = formData.pos_y;
  };

  const handleMouseMove = (e) => {
    if (!dragRef.current.isDragging) return;
    const deltaY = e.clientY - dragRef.current.startY;
    // Sensibilidad del arrastre (puedes ajustar el divisor)
    let newPos = dragRef.current.startPos + (deltaY / 2);
    // Limitar entre 0 y 100
    newPos = Math.max(0, Math.min(100, newPos));
    setFormData(prev => ({ ...prev, pos_y: Math.round(newPos) }));
  };

  const handleMouseUp = () => {
    dragRef.current.isDragging = false;
  };

  useEffect(() => {
    if (showReposition) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
    }
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [showReposition]);

  const getProcessedImageUrl = () => {
    if (formData.imageData) return formData.imageData;
    if (!formData.currentImageUrl) return '';

    let url = formData.currentImageUrl;

    // IMPORTANTE: Si la URL es la imagen optimista (Base64), no le pegamos el token
    if (url.startsWith('data:image')) {
      return url;
    }

    if (!url.includes('token=')) {
      url += url.includes('?') ? `&token=${token}` : `?token=${token}`;
    }
    return url;
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-kenth-brightred"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">

        {/* Cabecera */}
        <div className="flex items-center justify-between mb-10">
          <div>
            <h1 className="text-4xl font-black text-white uppercase tracking-tight">Ajustes del Curso</h1>
            <p className="text-gray-400 font-medium">Personaliza la apariencia y metadatos de tu curso.</p>
          </div>
          <button
            onClick={() => navigate(`/dashboard/course/${id}`)}
            className="text-gray-400 hover:text-white transition flex items-center gap-2 font-bold text-sm uppercase tracking-widest"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
            Volver
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-8">

          {/* SECCIÓN 1: GENERAL */}
          <div className="bg-kenth-surface/20 rounded-3xl p-8 border border-kenth-surface/30">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
              <span className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center text-blue-400 text-sm font-black">01</span>
              Información General
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex flex-col gap-2">
                <label className="text-xs font-black text-gray-500 uppercase tracking-widest ml-1">Nombre Completo</label>
                <input
                  type="text"
                  name="fullname"
                  value={formData.fullname}
                  onChange={handleInputChange}
                  className="bg-black/40 border border-kenth-surface/50 rounded-xl p-3 text-white focus:outline-none focus:border-kenth-brightred transition shadow-inner"
                  required
                />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xs font-black text-gray-500 uppercase tracking-widest ml-1">Nombre Corto</label>
                <input
                  type="text"
                  name="shortname"
                  value={formData.shortname}
                  onChange={handleInputChange}
                  className="bg-black/40 border border-kenth-surface/50 rounded-xl p-3 text-white focus:outline-none focus:border-kenth-brightred transition shadow-inner"
                  required
                />
              </div>
            </div>

            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex flex-col gap-2">
                <label className="text-xs font-black text-gray-500 uppercase tracking-widest ml-1">Visibilidad</label>
                <select
                  name="visible"
                  value={formData.visible}
                  onChange={handleInputChange}
                  className="bg-black/40 border border-kenth-surface/50 rounded-xl p-3 text-white focus:outline-none focus:border-kenth-brightred transition shadow-inner"
                >
                  <option value={1} className="bg-kenth-bg">Mostrar curso</option>
                  <option value={0} className="bg-kenth-bg">Ocultar curso</option>
                </select>
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xs font-black text-gray-500 uppercase tracking-widest ml-1">Categoría</label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleInputChange}
                  className="bg-black/40 border border-kenth-surface/50 rounded-xl p-3 text-white focus:outline-none focus:border-kenth-brightred transition shadow-inner"
                >
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.id} className="bg-kenth-bg">
                      {cat.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* SECCIÓN 2: APARIENCIA */}
          <div className="bg-kenth-surface/20 rounded-3xl p-8 border border-kenth-surface/30">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
              <span className="w-8 h-8 bg-kenth-brightred/20 rounded-lg flex items-center justify-center text-kenth-brightred text-sm font-black">02</span>
              Imagen de Portada
            </h2>

            <div className="flex flex-col md:flex-row gap-8 items-center">
              <div
                className="group w-full md:w-64 h-40 rounded-2xl overflow-hidden border border-kenth-surface/50 bg-transparent relative shadow-2xl cursor-pointer"
                onClick={() => getProcessedImageUrl() && setShowReposition(true)}
              >
                {getProcessedImageUrl() ? (
                  <>
                    <img
                      src={getProcessedImageUrl()}
                      alt="Full View"
                      className="w-full h-full object-contain"
                    />
                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <span className="text-[10px] font-black uppercase tracking-widest bg-white text-black px-3 py-1 rounded-full">Ajustar Recorte</span>
                    </div>
                  </>
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-600 text-xs text-center p-4 italic">No hay imagen configurada</div>
                )}
                {formData.imageData && (
                  <div className="absolute top-2 right-2 bg-kenth-brightred text-white text-[8px] font-bold px-2 py-1 rounded-full uppercase tracking-tighter">Nueva</div>
                )}
              </div>

              <div className="flex-1 w-full text-center md:text-left">
                <p className="text-gray-400 text-sm mb-4">La imagen se estirará para cubrir la tarjeta del curso. Haz clic en la miniatura para ajustar la posición vertical.</p>
                <div className="flex flex-wrap gap-4 justify-center md:justify-start">
                  <button
                    type="button"
                    onClick={() => fileInputRef.current.click()}
                    className="bg-kenth-surface/40 hover:bg-kenth-surface/60 text-white px-6 py-3 rounded-xl font-bold text-xs uppercase tracking-widest transition flex items-center gap-2 border border-kenth-surface/50 shadow-lg"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                    Subir Nueva Foto
                  </button>
                  {getProcessedImageUrl() && (
                    <button
                      type="button"
                      onClick={() => setShowReposition(true)}
                      className="bg-white/5 hover:bg-white/10 text-white px-6 py-3 rounded-xl font-bold text-xs uppercase tracking-widest transition flex items-center gap-2 border border-white/10"
                    >
                      Ajustar Posición
                    </button>
                  )}
                </div>
                <input type="file" ref={fileInputRef} onChange={handleImageUpload} accept="image/*" className="hidden" />
              </div>
            </div>
          </div>

          {/* SECCIÓN 3: DESCRIPCIÓN */}
          <div className="bg-kenth-surface/20 rounded-3xl p-8 border border-kenth-surface/30">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
              <span className="w-8 h-8 bg-emerald-500/20 rounded-lg flex items-center justify-center text-emerald-400 text-sm font-black">03</span>
              Descripción del Curso
            </h2>
            <textarea
              name="summary"
              value={formData.summary}
              onChange={handleInputChange}
              className="w-full bg-black/40 border border-kenth-surface/50 rounded-2xl p-4 text-white focus:outline-none focus:border-kenth-brightred transition shadow-inner min-h-[150px] font-light text-sm"
              placeholder="Describe de qué trata el curso..."
            />
          </div>

          {/* BOTÓN GUARDAR */}
          <div className="flex justify-end mt-4">
            <button
              type="submit"
              disabled={saving}
              className="bg-kenth-brightred hover:bg-red-600 text-white px-12 py-4 rounded-2xl font-black text-sm uppercase tracking-widest transition shadow-[0_10px_30px_rgba(225,28,64,0.3)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3 active:scale-95"
            >
              {saving ? (
                <>
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                  Guardando...
                </>
              ) : 'Guardar Todos los Cambios'}
            </button>
          </div>

        </form>

        {/* MODAL DE REPOSICIONAMIENTO */}
        {showReposition && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-8 bg-black/90 backdrop-blur-sm animate-in fade-in duration-300">
            {/* 1. Modal extra ancho (max-w-7xl) para igualar el aspecto de "Billboard" del Dashboard */}
            <div className="w-full max-w-7xl bg-kenth-bg border border-kenth-surface/50 rounded-[3rem] overflow-hidden shadow-[0_25px_80px_rgba(0,0,0,0.8)]">

              <div className="p-6 md:p-8 border-b border-kenth-surface/30 flex justify-between items-center">
                <div>
                  <h3 className="text-2xl font-black text-white uppercase tracking-tighter">Ajustar Posición</h3>
                  <p className="text-gray-400 text-sm">Arrastra la imagen hacia arriba o abajo para encuadrarla.</p>
                </div>
                <button onClick={() => setShowReposition(false)} className="p-2 hover:bg-white/10 rounded-full transition">
                  <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>

              <div className="p-6 md:p-10 flex flex-col items-center">
                {/* Previsualización EXACTA de la CourseCard */}
                <div
                  className="group relative w-full h-64 md:h-80 rounded-[2rem] overflow-hidden border border-kenth-surface/30 cursor-ns-resize shadow-2xl select-none"
                  onMouseDown={handleMouseDown}
                >
                  {/* Imagen de Fondo */}
                  <img
                    src={getProcessedImageUrl()}
                    alt="Reposition Preview"
                    style={{ objectPosition: `center ${formData.pos_y}%` }}
                    className="absolute inset-0 w-full h-full object-cover pointer-events-none transition-none"
                  />

                  {/* Overlay Oscuro Gradual (Idéntico a CourseCard) */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent pointer-events-none" />

                  {/* Contenido de la Tarjeta */}
                  <div className="absolute inset-0 p-8 flex flex-col justify-end pointer-events-none">

                    {/* 2. Aplicamos opacity-40 a los textos para que se vean como "marca de agua" de previsualización */}
                    <div className="opacity-40">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="bg-kenth-brightred text-white text-[10px] font-black px-3 py-1 rounded-full tracking-widest uppercase shadow-lg">
                          {formData.categoryname}
                        </span>
                        {formData.visible == 0 && (
                          <span className="bg-yellow-500 text-black text-[10px] font-black px-3 py-1 rounded-full tracking-widest uppercase">
                            Oculto
                          </span>
                        )}
                      </div>

                      <h2 className="text-3xl md:text-5xl font-black text-white uppercase tracking-tight drop-shadow-2xl">
                        {formData.fullname || 'NOMBRE DEL CURSO'}
                      </h2>

                      {formData.shortname && (
                        <p className="text-gray-300 text-sm md:text-lg font-medium italic mt-2 opacity-80">
                          {formData.shortname}
                        </p>
                      )}
                    </div>

                    {/* 3. EL TRUCO DEL ENCUADRE: El botón fantasma que empuja el texto hacia arriba exactamente igual que en el Dashboard */}
                    <div className="mt-6 flex items-center gap-4 opacity-0 pointer-events-none">
                      <button className="bg-white text-black px-8 py-3 rounded-full font-black text-xs tracking-widest uppercase flex items-center gap-3">
                        ENTRAR AL CURSO
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                      </button>
                    </div>

                  </div>

                  {/* Decoración: Gradiente en el borde inferior (Transparente para previsualización) */}
                  <div className="absolute bottom-0 left-0 w-full h-1.5 bg-gradient-to-r from-transparent via-kenth-brightred to-transparent opacity-20 pointer-events-none" />

                  {/* Indicadores visuales de arrastre */}
                  <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 flex justify-between px-6 opacity-30 pointer-events-none">
                    <svg className="w-10 h-10 text-white animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7l4-4m0 0l4 4m-4-4v18" /></svg>
                    <svg className="w-10 h-10 text-white animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 17l-4 4m0 0l-4-4m4 4V3" /></svg>
                  </div>
                </div>

                <div className="w-full mt-8 flex items-center gap-6">
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={formData.pos_y}
                    onChange={(e) => setFormData(prev => ({ ...prev, pos_y: parseInt(e.target.value) }))}
                    className="flex-1 h-2 bg-kenth-surface/50 rounded-lg appearance-none cursor-pointer accent-kenth-brightred"
                  />
                  <span className="text-white font-black w-12 text-right">{formData.pos_y}%</span>
                </div>

                <button
                  onClick={() => setShowReposition(false)}
                  className="mt-10 bg-white text-black px-12 py-4 rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-kenth-brightred hover:text-white transition shadow-xl"
                >
                  Confirmar Encuadre
                </button>
              </div>

            </div>
          </div>
        )}

      </div>
    </DashboardLayout>
  );
}
