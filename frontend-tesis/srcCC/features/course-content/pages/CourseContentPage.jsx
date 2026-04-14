import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { getCourseContents } from '../../services/courseService';
import MoodleRenderer from '../../components/ui/MoodleRenderer';

const HERRAMIENTAS_MOODLE = [
  { id: 'quiz', nombre: 'Cuestionario', icono: '✅', color: 'text-orange-400', bg: 'bg-orange-400/10', border: 'border-orange-400/20' },
  { id: 'hvp', nombre: 'H5P Interactivo', icono: '✨', color: 'text-indigo-400', bg: 'bg-indigo-400/10', border: 'border-indigo-400/20' },
  { id: 'page', nombre: 'Página', icono: '📄', color: 'text-emerald-400', bg: 'bg-emerald-400/10', border: 'border-emerald-400/20' },
  { id: 'label', nombre: 'Área de texto', icono: 'T', color: 'text-emerald-400', bg: 'bg-emerald-400/10', border: 'border-emerald-400/20' },
  { id: 'resource', nombre: 'Archivo', icono: '💾', color: 'text-teal-400', bg: 'bg-teal-400/10', border: 'border-teal-400/20' },
];

export default function CourseContentView() {
  const { id } = useParams();
  const [secciones, setSecciones] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  
  const [visorActivo, setVisorActivo] = useState(null);
  const [chooserAbierto, setChooserAbierto] = useState(false);
  const [studioAbierto, setStudioAbierto] = useState(false);
  const [herramientaAvanzada, setHerramientaAvanzada] = useState('');
  
  // Guardamos la sección donde el profe hizo click en el "+"
  const [seccionDestinoId, setSeccionDestinoId] = useState(1); 

  const [esProfesor, setEsProfesor] = useState(false);
  // ESTADOS PARA MENÚ CONTEXTUAL Y DRAG AVANZADO
  const [menuActivo, setMenuActivo] = useState(null); 
  const [draggedMod, setDraggedMod] = useState(null);
  const [dropIndicator, setDropIndicator] = useState(null); // { id, position: 'top'|'bottom' }

  // ESTADOS PARA EDICIÓN DE SECCIÓN
  const [editandoSeccionId, setEditandoSeccionId] = useState(null);
  const [nuevoNombreSeccion, setNuevoNombreSeccion] = useState('');

  useEffect(() => {
    const verificarPermisos = async () => {
      const token = localStorage.getItem('moodle_token');
      if (!token || !id) return;
      try {
        const respuesta = await fetch(`/moodle_api/tesis_role.php?token=${token}&courseid=${id}`);
        const data = await respuesta.json();
        setEsProfesor(data.esProfesor);
      } catch (error) { setEsProfesor(false); }
    };
    verificarPermisos();
  }, [id]);

  useEffect(() => {
    const cerrarMenu = () => setMenuActivo(null);
    if (menuActivo) document.addEventListener('click', cerrarMenu);
    return () => document.removeEventListener('click', cerrarMenu);
  }, [menuActivo]);

  useEffect(() => {
    const handleMoodleMessage = (event) => {
      if (event.data === 'moodle_studio_done') {
        setStudioAbierto(false);
        fetchContenido();
      }
      if (event.data === 'moodle_view_done') {
        setVisorActivo(null);
      }
    };
    window.addEventListener('message', handleMoodleMessage);
    return () => window.removeEventListener('message', handleMoodleMessage);
  }, []);

  const fetchContenido = async () => {
    const token = localStorage.getItem('moodle_token');
    try {
      const datos = await getCourseContents(token, id);
      setSecciones(datos);
      setError('');
    } catch (err) { setError(err.message); } 
    finally { setCargando(false); }
  };

  useEffect(() => { if (id) fetchContenido(); }, [id]);

  // === ACCIONES OPTIMISTAS DE MENÚ ===
  const ejecutarAccion = async (action, cmid, secIdx) => {
    const token = localStorage.getItem('moodle_token');
    setMenuActivo(null);

    const nuevasSecciones = [...secciones];
    const modIdx = nuevasSecciones[secIdx].modules.findIndex(m => m.id === cmid);
    
    if (action === 'hide') nuevasSecciones[secIdx].modules[modIdx].visible = 0;
    if (action === 'show') nuevasSecciones[secIdx].modules[modIdx].visible = 1;
    if (action === 'delete') nuevasSecciones[secIdx].modules.splice(modIdx, 1);
    
    setSecciones(nuevasSecciones);

    try {
      await fetch(`/moodle_api/tesis_actions.php?token=${token}&action=${action}&cmid=${cmid}`);
      if (action === 'duplicate') fetchContenido();
    } catch (e) {
      console.error('Error en background', e);
      fetchContenido();
    }
  };

  const abrirEdicion = (mod) => {
    setHerramientaAvanzada('__edit__');
    setMenuActivo(null);
    window.__kenth_edit_cmid = mod.id;
    setStudioAbierto(true);
  };

  // === RENOMBRAR SECCIÓN (TEMA) ===
  const guardarNombreSeccion = async (sectionId, secIdx) => {
    if (!nuevoNombreSeccion.trim()) {
      setEditandoSeccionId(null);
      return;
    }
    
    // 1. Actualización visual instantánea (Optimista)
    const nuevasSecciones = [...secciones];
    nuevasSecciones[secIdx].name = nuevoNombreSeccion;
    setSecciones(nuevasSecciones);
    setEditandoSeccionId(null);

    // 2. Envío silencioso a Moodle
    const token = localStorage.getItem('moodle_token');
    try {
      await fetch(`/moodle_api/tesis_actions.php?token=${token}&action=rename_section&sectionid=${sectionId}&name=${encodeURIComponent(nuevoNombreSeccion)}`);
    } catch (e) {
      console.error('Error al renombrar la sección:', e);
      fetchContenido(); // Revertir si falla
    }
  };

  // === DRAG & DROP DE ALTA PRECISIÓN ===
  const handleDragStart = (e, mod, seccionIdx) => {
    setDraggedMod({ mod, seccionIdx });
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e, targetModId) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';

    // MAGIA DE COORDENADAS: Calculamos si el ratón está arriba o abajo
    const rect = e.currentTarget.getBoundingClientRect();
    const mouseY = e.clientY - rect.top; 
    const position = mouseY < rect.height / 2 ? 'top' : 'bottom';

    setDropIndicator({ id: targetModId, position });
  };

  const handleDrop = async (e, targetMod, targetSeccionIdx) => {
    e.preventDefault();

    if (!draggedMod || !dropIndicator) {
      setDropIndicator(null);
      return;
    }

    const sourceSecIdx = draggedMod.seccionIdx;
    const sourceMod = draggedMod.mod;
    const position = dropIndicator.position;

    if (targetMod && sourceMod.id === targetMod.id) {
      setDropIndicator(null);
      setDraggedMod(null);
      return;
    }

    // 1. ACTUALIZACIÓN INSTANTÁNEA VISUAL
    const nuevasSecciones = [...secciones];
    nuevasSecciones[sourceSecIdx].modules = nuevasSecciones[sourceSecIdx].modules.filter(m => m.id !== sourceMod.id);
    
    if (!nuevasSecciones[targetSeccionIdx].modules) nuevasSecciones[targetSeccionIdx].modules = [];

    let beforeCmId = 0;

    if (targetMod) {
        let targetModIdx = nuevasSecciones[targetSeccionIdx].modules.findIndex(m => m.id === targetMod.id);

        if (position === 'bottom') {
           targetModIdx += 1;
        }

        nuevasSecciones[targetSeccionIdx].modules.splice(targetModIdx, 0, sourceMod);

        const modBelow = nuevasSecciones[targetSeccionIdx].modules[targetModIdx + 1];
        beforeCmId = modBelow ? modBelow.id : 0;
    } else {
        nuevasSecciones[targetSeccionIdx].modules.push(sourceMod);
    }

    setSecciones(nuevasSecciones);
    setDropIndicator(null);
    setDraggedMod(null);

    // 2. COMUNICACIÓN SILENCIOSA CON MOODLE
    const token = localStorage.getItem('moodle_token');
    const targetSectionId = nuevasSecciones[targetSeccionIdx].id;
    const paramBefore = beforeCmId ? `&beforecmid=${beforeCmId}` : '';

    try {
      await fetch(`/moodle_api/tesis_actions.php?token=${token}&action=move&cmid=${sourceMod.id}&targetsection=${targetSectionId}${paramBefore}`);
    } catch (e) {
      console.error('Error al mover en Moodle:', e);
      fetchContenido();
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6 relative">

        {/* HEADER DE NAVEGACION */}
        <div>
          <Link to="/dashboard" className="text-kenth-brightred hover:text-white flex items-center gap-2 mb-4 transition font-bold text-sm tracking-widest uppercase">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
            Volver al Catálogo
          </Link>
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
            <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-white uppercase drop-shadow">
              Vista del Curso <span className="text-kenth-red">#{id}</span>
            </h1>
          </div>
          <div className="h-px bg-kenth-surface/30 w-full mb-6"></div>
        </div>

        {cargando && (
          <div className="bg-[#2D2D30] rounded-[2rem] p-12 border border-kenth-surface/20 flex justify-center items-center">
             <svg className="animate-spin h-10 w-10 text-kenth-brightred" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          </div>
        )}

        {error && (
          <div className="bg-red-900/20 border-l-4 border-kenth-brightred p-6 rounded-r-xl">
             <p className="text-red-200 font-bold font-sans">Ha ocurrido un problema: {error}</p>
          </div>
        )}

        {/* RENDERIZADO DE CONTENIDOS DEL CURSO */}
        {!cargando && !error && secciones.length > 0 && (
          <div className="flex flex-col gap-6">
             {secciones.map((seccion, secIdx) => {
                
                // Saber si alguna de las actividades de este tema tiene el menú abierto
                const tieneMenuAbierto = seccion.modules?.some(m => m.id === menuActivo);

                return (
                  <div 
                    key={seccion.id} 
                    // 1. FIX Z-INDEX DEL TEMA: Si tiene el menú abierto, elevamos todo el tema.
                    // 2. Quitamos el "overflow-hidden" para que los menús puedan escapar de la caja.
                    className={`bg-[#1e1e20] rounded-[1rem] p-6 border border-kenth-surface/20 relative transition-all duration-300 ${tieneMenuAbierto ? 'z-40 shadow-2xl' : 'z-10'}`}
                  >
                     
                     {/* Fondo decorativo sutil encapsulado para que no manche afuera */}
                     <div className="absolute inset-0 overflow-hidden rounded-[1rem] pointer-events-none">
                        <div className="absolute -top-10 -right-10 w-32 h-32 bg-white/5 rounded-full blur-[50px]"></div>
                     </div>

                     {/* === TÍTULO DE LA SECCIÓN CON EDICIÓN INLINE === */}
                     <div className="relative z-10 flex items-center gap-3 mb-2 group/titulo">
                       {editandoSeccionId === seccion.id ? (
                          <div className="flex items-center gap-2 w-full max-w-md animate-in fade-in zoom-in-95 duration-200">
                             <input 
                               type="text" 
                               autoFocus
                               value={nuevoNombreSeccion}
                               onChange={(e) => setNuevoNombreSeccion(e.target.value)}
                               onKeyDown={(e) => {
                                 if (e.key === 'Enter') guardarNombreSeccion(seccion.id, secIdx);
                                 if (e.key === 'Escape') setEditandoSeccionId(null);
                               }}
                               className="flex-1 bg-[#2D2D30] text-white font-bold text-xl border-b-2 border-kenth-brightred px-2 py-1 outline-none focus:bg-[#1A1A1D] transition-colors"
                             />
                             <button onClick={() => guardarNombreSeccion(seccion.id, secIdx)} className="bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500 hover:text-white p-2 rounded-lg transition" title="Guardar (Enter)">
                               <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                             </button>
                             <button onClick={() => setEditandoSeccionId(null)} className="bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white p-2 rounded-lg transition" title="Cancelar (Esc)">
                               <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                             </button>
                          </div>
                       ) : (
                          <>
                             <h2 className="text-2xl font-bold text-white">{seccion.name || `Tema ${seccion.section}`}</h2>
                             
                             {esProfesor && (
                               <button 
                                 onClick={() => {
                                   setEditandoSeccionId(seccion.id);
                                   setNuevoNombreSeccion(seccion.name || `Tema ${seccion.section}`);
                                 }}
                                 className="text-gray-500 hover:text-kenth-brightred opacity-0 group-hover/titulo:opacity-100 transition-all p-1"
                                 title="Editar título"
                               >
                                 <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                               </button>
                             )}
                          </>
                       )}
                     </div>
                     {seccion.summary && <div className="text-gray-400 text-sm mb-4 relative z-10" dangerouslySetInnerHTML={{__html: seccion.summary}}></div>}
                     
                     <div className="flex flex-col gap-1 mt-4 relative z-10">

                        {/* 1. BOTÓN SIEMPRE VISIBLE AL INICIO (Para secciones vacías o con contenido) */}
                        {esProfesor && (
                          <div className="flex justify-center py-2 group/insert">
                            <button 
                              onClick={() => { setSeccionDestinoId(seccion.section); setChooserAbierto(true); }}
                              className="w-10 h-10 rounded-full border-2 border-dashed border-gray-700 hover:border-kenth-brightred text-gray-500 hover:text-kenth-brightred flex items-center justify-center transition-all opacity-30 group-hover/insert:opacity-100 hover:!opacity-100 hover:scale-110 bg-[#1e1e20]"
                              title="Agregar recurso al inicio"
                            >
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" /></svg>
                            </button>
                          </div>
                        )}

                        {seccion.modules && seccion.modules.length > 0 ? (
                           seccion.modules.map((mod, modIdx) => (
                              <React.Fragment key={mod.id}>
                                
                                <div 
                                  draggable={esProfesor}
                                  onDragStart={esProfesor ? (e) => handleDragStart(e, mod, secIdx) : undefined}
                                  onDragOver={esProfesor ? (e) => handleDragOver(e, mod.id) : undefined}
                                  onDragLeave={() => setDropIndicator(null)}
                                  onDrop={esProfesor ? (e) => handleDrop(e, mod, secIdx) : undefined}
                                  onDragEnd={() => { setDraggedMod(null); setDropIndicator(null); }}
                                  className={`
                                    bg-[#2D2D30] p-4 rounded-lg flex items-center gap-4 border transition-all duration-200 group/card relative
                                    ${mod.url ? 'cursor-pointer hover:border-kenth-brightred/50 hover:-translate-y-0.5 shadow-md' : 'border-transparent'}
                                    ${mod.visible === 0 ? 'opacity-40 grayscale' : ''}
                                    ${draggedMod?.mod.id === mod.id ? 'opacity-20 scale-[0.98]' : ''}
                                    ${menuActivo === mod.id ? 'z-[60] ring-1 ring-kenth-surface' : 'z-10 hover:z-20'}
                                  `}
                                >
                                   {/* ==== LÍNEAS NEÓN INDICADORAS DE DROP ==== */}
                                   {dropIndicator?.id === mod.id && dropIndicator.position === 'top' && (
                                     <div className="absolute top-[-2px] left-0 w-full h-[3px] bg-indigo-500 rounded-full shadow-[0_0_10px_#6366f1] z-50 pointer-events-none"></div>
                                   )}
                                   {dropIndicator?.id === mod.id && dropIndicator.position === 'bottom' && (
                                     <div className="absolute bottom-[-2px] left-0 w-full h-[3px] bg-indigo-500 rounded-full shadow-[0_0_10px_#6366f1] z-50 pointer-events-none"></div>
                                   )}
                                   {esProfesor && (
                                     <div className="cursor-grab active:cursor-grabbing text-gray-600 hover:text-gray-300 transition opacity-0 group-hover/card:opacity-100 flex-shrink-0" title="Arrastrar para mover">
                                       <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><circle cx="9" cy="5" r="1.5"/><circle cx="15" cy="5" r="1.5"/><circle cx="9" cy="12" r="1.5"/><circle cx="15" cy="12" r="1.5"/><circle cx="9" cy="19" r="1.5"/><circle cx="15" cy="19" r="1.5"/></svg>
                                     </div>
                                   )}

                                   <div className="flex items-center gap-4 flex-1 min-w-0" onClick={() => mod.url && setVisorActivo(mod)}>
                                     <img src={mod.modicon} alt={mod.modname} className={`w-8 h-8 rounded flex-shrink-0 ${mod.visible===0 ? 'opacity-50':''}`} />
                                     <div className="flex flex-col flex-1 min-w-0">
                                        <span className={`font-semibold text-white transition truncate ${mod.url && 'group-hover/card:text-kenth-brightred'} ${mod.visible===0 ? 'line-through text-gray-400':''}`}>
                                          {mod.name} {mod.visible === 0 && <span className="text-xs text-red-500 ml-2 no-underline tracking-widest">(Oculto a estudiantes)</span>}
                                        </span>
                                        <span className="text-[10px] text-gray-500 uppercase tracking-widest font-bold">{mod.modplural}</span>
                                     </div>
                                   </div>

                                   {/* === MENÚ DE 3 PUNTOS (Solo profes) === */}
                                   {esProfesor && (
                                     <div className="relative flex-shrink-0">
                                       <button 
                                         onClick={(e) => { e.stopPropagation(); setMenuActivo(menuActivo === mod.id ? null : mod.id); }}
                                         className={`p-2 rounded-lg transition ${menuActivo === mod.id ? 'text-white bg-white/10' : 'text-gray-500 hover:text-white hover:bg-white/10 opacity-0 group-hover/card:opacity-100'}`}
                                       >
                                         <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>
                                       </button>

                                       {menuActivo === mod.id && (
                                         <div 
                                           onClick={(e) => e.stopPropagation()}
                                           className="absolute right-0 top-12 w-48 bg-[#1e1e20] border border-kenth-surface/50 rounded-xl shadow-[0_15px_40px_rgba(0,0,0,0.6)] z-[70] py-2 animate-in fade-in zoom-in-95 duration-200"
                                         >
                                           <button onClick={() => abrirEdicion(mod)} className="w-full text-left px-4 py-2.5 text-sm text-gray-300 hover:bg-white/5 hover:text-white flex items-center gap-3 transition">
                                             <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                                             Editar ajustes
                                           </button>
                                           <button onClick={() => ejecutarAccion(mod.visible !== 0 ? 'hide' : 'show', mod.id, secIdx)} className="w-full text-left px-4 py-2.5 text-sm text-gray-300 hover:bg-white/5 hover:text-white flex items-center gap-3 transition">
                                             <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d={mod.visible !== 0 ? "M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.879L21 21" : "M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"} /></svg>
                                             {mod.visible !== 0 ? 'Ocultar' : 'Mostrar'}
                                           </button>
                                           <button onClick={() => ejecutarAccion('duplicate', mod.id, secIdx)} className="w-full text-left px-4 py-2.5 text-sm text-gray-300 hover:bg-white/5 hover:text-white flex items-center gap-3 transition">
                                             <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                                             Duplicar
                                           </button>
                                           <div className="h-px bg-kenth-surface/30 my-1"></div>
                                           <button onClick={() => { if(window.confirm('¿Eliminar recurso permanentemente?')) ejecutarAccion('delete', mod.id, secIdx); }} className="w-full text-left px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 flex items-center gap-3 transition">
                                             <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                                             Borrar
                                           </button>
                                         </div>
                                       )}
                                     </div>
                                   )}
                                </div>

                                {/* 2. BOTÓN "+" ENTRE RECURSOS (Solo si no es el último) */}
                                {esProfesor && modIdx < seccion.modules.length - 1 && (
                                  <div className="flex justify-center py-1 group/insert">
                                    <button 
                                      onClick={() => { setSeccionDestinoId(seccion.section); setChooserAbierto(true); }}
                                      className="w-8 h-8 rounded-full border-2 border-dashed border-gray-800 hover:border-kenth-brightred text-gray-700 hover:text-kenth-brightred flex items-center justify-center transition-all opacity-0 group-hover/insert:opacity-100 hover:!opacity-100 hover:scale-110"
                                    >
                                      <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" /></svg>
                                    </button>
                                  </div>
                                )}
                              </React.Fragment>
                           ))
                        ) : (
                           /* 3. VISTA PARA SECCIÓN TOTALMENTE VACÍA */
                           <div 
                              onDragOver={esProfesor ? (e) => { e.preventDefault(); setDropIndicator({ id: `empty-${seccion.id}`, position: 'top' }); } : undefined}
                              onDrop={esProfesor ? (e) => handleDrop(e, null, secIdx) : undefined}
                              onDragLeave={() => setDropIndicator(null)}
                              className={`
                                text-gray-500 text-sm italic py-10 text-center border-2 border-dashed rounded-xl transition-all duration-300 flex flex-col items-center gap-3
                                ${dropIndicator?.id === `empty-${seccion.id}` ? 'border-indigo-500 bg-indigo-500/5 text-indigo-300' : 'border-gray-700/30 bg-transparent'}
                              `}
                           >
                             <span>Este tema no tiene contenido aún.</span>
                             {esProfesor && (
                               <button 
                                 onClick={() => { setSeccionDestinoId(seccion.section); setChooserAbierto(true); }}
                                 className="bg-kenth-brightred/10 text-kenth-brightred px-4 py-2 rounded-lg text-xs font-bold uppercase border border-kenth-brightred/20 hover:bg-kenth-brightred hover:text-white transition-all"
                               >
                                 + Crear primer recurso
                               </button>
                             )}
                           </div>
                        )}
                     </div>
                  </div>
                );
             })}
          </div>
        )}
      </div>

      {esProfesor && chooserAbierto && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm animate-in fade-in duration-200">
           <div className="bg-[#1e1e20] w-full max-w-4xl rounded-2xl flex flex-col border border-kenth-surface/50 overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)]">
              <div className="p-6 border-b border-kenth-surface/30 flex justify-between items-center bg-[#2D2D30]">
                 <h2 className="text-xl font-bold text-white uppercase tracking-wider">Añadir recurso (Tema {seccionDestinoId})</h2>
                 <button onClick={() => setChooserAbierto(false)} className="text-gray-400 hover:text-white bg-white/5 p-2 rounded-lg transition">
                   <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                 </button>
              </div>
              <div className="p-6 max-h-[70vh] overflow-y-auto">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {HERRAMIENTAS_MOODLE.map((herramienta) => (
                    <button 
                      key={herramienta.id}
                      onClick={() => {
                        setHerramientaAvanzada(herramienta.id);
                        setChooserAbierto(false);
                        setStudioAbierto(true);
                      }}
                      className="group flex flex-col items-center justify-center p-6 bg-[#2D2D30] border border-kenth-surface/30 hover:border-kenth-brightred rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_10px_20px_rgba(225,29,72,0.15)]"
                    >
                      <div className={`w-14 h-14 rounded-full ${herramienta.bg} ${herramienta.color} border ${herramienta.border} flex items-center justify-center text-2xl mb-3 transition-transform group-hover:scale-110`}>{herramienta.icono}</div>
                      <span className="text-sm font-semibold text-gray-300 group-hover:text-white">{herramienta.nombre}</span>
                    </button>
                  ))}
                </div>
              </div>
           </div>
        </div>
      )}

      {esProfesor && studioAbierto && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/95 p-2 md:p-6 backdrop-blur-md animate-in fade-in duration-300">
           <div className="bg-[#1e1e20] w-full h-full max-w-[1400px] max-h-[900px] rounded-2xl flex flex-col border border-indigo-500/30 overflow-hidden shadow-[0_0_80px_rgba(79,70,229,0.2)]">
               <div className="p-4 flex justify-between items-center border-b border-indigo-500/30 bg-gradient-to-r from-[#1e1e20] to-indigo-900/20">
                  <div className="flex items-center gap-3">
                    <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                    <h2 className="text-white font-bold text-lg tracking-wider uppercase">Moodle Studio</h2>
                    <span className="bg-indigo-600 text-white text-[10px] uppercase font-bold py-1 px-2 rounded-full">{herramientaAvanzada === '__edit__' ? 'Editando' : 'Creando'}</span>
                  </div>
                  <button onClick={() => { setStudioAbierto(false); window.__kenth_edit_cmid = null; fetchContenido(); }} className="text-gray-400 hover:text-white bg-red-500/10 hover:bg-red-500/80 px-4 py-2 rounded-lg transition font-bold text-xs tracking-widest uppercase flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg> Cerrar
                  </button>
               </div>
               <div className="flex-1 w-full bg-[#1e1e20] relative">
                   <iframe 
                     name="moodle_studio_iframe"
                     src={
                       herramientaAvanzada === '__edit__' 
                         ? `/moodle_api/tesis_studio.php?token=${localStorage.getItem('moodle_token')}&courseid=${id}&modname=__edit__&cmid=${window.__kenth_edit_cmid || 0}`
                         // Pasamos el ID de la sección para que Moodle lo cree ahí directamente
                         : `/moodle_api/tesis_studio.php?token=${localStorage.getItem('moodle_token')}&courseid=${id}&modname=${herramientaAvanzada}&section=${seccionDestinoId}`
                     }
                     className="w-full h-full absolute inset-0 border-none"
                     allow="fullscreen *; geolocation *; microphone *; camera *; midi *; encrypted-media *; autoplay *"
                   />
               </div>
           </div>
        </div>
      )}

      {visorActivo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 md:p-10 backdrop-blur-sm animate-in fade-in duration-200">
           <div className="bg-[#1e1e20] w-full h-full max-w-6xl rounded-2xl flex flex-col border border-kenth-surface/50 overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)]">
               <div className="p-4 flex justify-between items-center border-b border-kenth-surface/30 bg-[#2D2D30]">
                  <div className="flex items-center gap-3">
                    <img src={visorActivo.modicon} alt="icon" className="w-6 h-6"/>
                    <h2 className="text-white font-bold text-lg">{visorActivo.name}</h2>
                  </div>
                  <button onClick={() => setVisorActivo(null)} className="text-gray-400 hover:text-white bg-red-500/10 hover:bg-red-500/80 px-4 py-2 rounded-lg transition font-bold text-sm tracking-widest uppercase flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg> Cerrar Visor
                  </button>
               </div>
               <div
  className={`flex-1 w-full bg-[#1e1e20] relative ${
    ['h5pactivity', 'hvp'].includes(visorActivo?.modname)
      ? 'p-0 overflow-hidden min-h-0'
      : 'p-4 md:p-8 overflow-y-auto min-h-0'
  }`}
>
  <MoodleRenderer modulo={visorActivo} />
</div>
           </div>
        </div>
      )}
    </DashboardLayout>
  );
}