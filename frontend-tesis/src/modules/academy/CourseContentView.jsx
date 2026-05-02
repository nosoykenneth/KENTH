import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getCourseContents, getMyCourses } from '../../shared/services/courseService';
import MoodleRenderer from '../../shared/components/ui/MoodleRenderer';
import PageContainer from '../../shared/components/layout/PageContainer';

const HERRAMIENTAS_MOODLE = [
  { id: 'quiz', nombre: 'Cuestionario', icono: '✅', color: 'text-orange-400', bg: 'bg-orange-400/10', border: 'border-orange-400/20' },
  { id: 'hvp', nombre: 'H5P Interactivo', icono: '✨', color: 'text-indigo-400', bg: 'bg-indigo-400/10', border: 'border-indigo-400/20' },
  { id: 'page', nombre: 'Página', icono: '📄', color: 'text-emerald-400', bg: 'bg-emerald-400/10', border: 'border-emerald-400/20' },
  { id: 'label', nombre: 'Área de texto', icono: 'T', color: 'text-emerald-400', bg: 'bg-emerald-400/10', border: 'border-emerald-400/20' },
  { id: 'resource', nombre: 'Archivo', icono: '💾', color: 'text-teal-400', bg: 'bg-teal-400/10', border: 'border-teal-400/20' },
];

const CourseSkeleton = () => (
  <div className="flex flex-col gap-8 w-full animate-pulse">
    {/* Title Skeleton moved here for better layout synchronization */}
    <div className="h-12 w-2/3 bg-kenth-surface/20 rounded-2xl mb-6"></div>
    
    {[1, 2, 3].map((i) => (
      <div key={i} className="bg-kenth-card rounded-[2rem] p-8 border border-kenth-border flex flex-col gap-6">
        <div className="flex items-center gap-4 mb-2">
          <div className="h-8 w-64 bg-kenth-surface/20 rounded-xl"></div>
          <div className="h-6 w-6 bg-kenth-surface/10 rounded-full"></div>
        </div>
        <div className="h-4 w-3/4 bg-kenth-surface/10 rounded-lg max-w-2xl mb-2"></div>
        
        <div className="flex flex-col gap-3">
          {[1, 2, 3, 4].map((j) => (
            <div key={j} className="bg-kenth-surface/5 p-5 rounded-2xl flex items-center gap-5 border border-kenth-border/20">
              <div className="w-10 h-10 rounded-xl bg-kenth-surface/20 shrink-0"></div>
              <div className="flex flex-col gap-2.5 flex-1">
                <div className="h-4 w-1/3 bg-kenth-surface/20 rounded-md"></div>
                <div className="h-3 w-1/5 bg-kenth-surface/10 rounded-md"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    ))}
  </div>
);

export default function CourseContentView() {
  const { courseId: id } = useParams();
  const navigate = useNavigate();
  const [secciones, setSecciones] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  const [courseName, setCourseName] = useState('');

  const [visorActivo, setVisorActivo] = useState(null);
  const [chooserAbierto, setChooserAbierto] = useState(false);
  const [studioAbierto, setStudioAbierto] = useState(false);
  const [herramientaAvanzada, setHerramientaAvanzada] = useState('');
  const [studioCargando, setStudioCargando] = useState(true);

  const [seccionDestinoId, setSeccionDestinoId] = useState(1);
  const [esProfesor, setEsProfesor] = useState(false);

  const [menuActivo, setMenuActivo] = useState(null);
  const [draggedMod, setDraggedMod] = useState(null);
  const [dropIndicator, setDropIndicator] = useState(null);

  const [editandoSeccionId, setEditandoSeccionId] = useState(null);
  const [nuevoNombreSeccion, setNuevoNombreSeccion] = useState('');
  const [seccionEnMovimientoId, setSeccionEnMovimientoId] = useState(null);
  const [menuSeccionActivo, setMenuSeccionActivo] = useState(null);
  const [editandoSummaryId, setEditandoSummaryId] = useState(null);
  const [nuevoSummarySeccion, setNuevoSummarySeccion] = useState('');
  const [participantesAbierto, setParticipantesAbierto] = useState(false);
  const [listaParticipantes, setListaParticipantes] = useState([]);
  const [busquedaParticipante, setBusquedaParticipante] = useState('');
  const [cargandoParticipantes, setCargandoParticipantes] = useState(false);

  useEffect(() => {
    const verificarPermisos = async () => {
      const token = localStorage.getItem('moodle_token');
      if (!token || !id) return;
      try {
        const respuesta = await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_role.php?token=${encodeURIComponent(token)}&courseid=${encodeURIComponent(id)}`);
        const data = await respuesta.json();
        setEsProfesor(data.esProfesor);
      } catch (error) { setEsProfesor(false); }
    };
    verificarPermisos();
  }, [id]);

  useEffect(() => {
    const cerrarMenu = () => {
      setMenuActivo(null);
      setMenuSeccionActivo(null);
    };
    if (menuActivo || menuSeccionActivo) document.addEventListener('click', cerrarMenu);
    return () => document.removeEventListener('click', cerrarMenu);
  }, [menuActivo, menuSeccionActivo]);

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
    const userid = localStorage.getItem('moodle_userid');
    
    try {
      const datos = await getCourseContents(token, id);
      setSecciones(datos);
      
      if (userid) {
        const misCursos = await getMyCourses(token, userid);
        const cursoActual = misCursos.find(c => String(c.id) === String(id));
        if (cursoActual) {
          setCourseName(cursoActual.fullname);
        }
      }
      
      setError('');
    } catch (err) { setError(err.message); }
    finally { setCargando(false); }
  };

  useEffect(() => { if (id) fetchContenido(); }, [id]);

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
      await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_actions.php?token=${token}&action=${action}&cmid=${cmid}`);
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

  const guardarNombreSeccion = async (sectionId, secIdx) => {
    if (!nuevoNombreSeccion.trim()) {
      setEditandoSeccionId(null);
      return;
    }

    const nuevasSecciones = [...secciones];
    nuevasSecciones[secIdx].name = nuevoNombreSeccion;
    setSecciones(nuevasSecciones);
    setEditandoSeccionId(null);

    const token = localStorage.getItem('moodle_token');
    try {
      const response = await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_actions.php?token=${token}&action=rename_section&sectionid=${sectionId}&name=${encodeURIComponent(nuevoNombreSeccion)}`);
      const resData = await response.json();
      if (!resData.success) {
        console.error("Error desde Moodle:", resData.error);
        fetchContenido();
      }
    } catch (e) {
      console.error('Error al renombrar la sección:', e);
      fetchContenido();
    }
  };

  const añadirSeccion = async (location) => {
    const token = localStorage.getItem('moodle_token');
    try {
      const response = await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_actions.php?token=${token}&action=add_section&courseid=${encodeURIComponent(id)}&location=${location}`);
      const data = await response.json();
      if (data.success) {
        fetchContenido();
      } else {
        alert("Error al añadir sección: " + data.error);
      }
    } catch (e) {
      console.error("Error en añadirSeccion:", e);
    }
  };

  const moverSeccion = async (sectionId, newPos) => {
    const token = localStorage.getItem('moodle_token');
    setSeccionEnMovimientoId(sectionId);
    try {
      const response = await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_actions.php?token=${token}&action=move_section&sectionid=${sectionId}&newpos=${newPos}`);
      const data = await response.json();
      if (data.success) {
        fetchContenido();
      }
    } catch (e) {
      console.error("Error en moverSeccion:", e);
    } finally {
      setSeccionEnMovimientoId(null);
    }
  };
  
  const borrarSeccion = async (sectionId) => {
    if (!window.confirm("¿Estás seguro de eliminar esta sección y todo su contenido? Esta acción no se puede deshacer.")) return;
    
    const token = localStorage.getItem('moodle_token');
    try {
      const response = await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_actions.php?token=${token}&action=delete_section&sectionid=${sectionId}`);
      const data = await response.json();
      if (data.success) {
        fetchContenido();
      } else {
        alert("Error al borrar sección: " + data.error);
      }
    } catch (e) {
      console.error("Error en borrarSeccion:", e);
    }
  };

  const guardarSummarySeccion = async (sectionId, secIdx) => {
    const nuevasSecciones = [...secciones];
    nuevasSecciones[secIdx].summary = nuevoSummarySeccion;
    setSecciones(nuevasSecciones);
    setEditandoSummaryId(null);

    const token = localStorage.getItem('moodle_token');
    try {
      await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_actions.php?token=${token}&action=update_section_summary&sectionid=${sectionId}&summary=${encodeURIComponent(nuevoSummarySeccion)}`);
    } catch (e) {
      console.error('Error al guardar el resumen:', e);
      fetchContenido();
    }
  };

  const fetchParticipantes = async () => {
    if (!id || id === '0') return;
    setCargandoParticipantes(true);
    const token = localStorage.getItem('moodle_token');
    try {
      const response = await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_enrolments.php?token=${token}&action=list&courseid=${encodeURIComponent(id)}`);
      const data = await response.json();
      console.log("Debug Participantes:", data);
      if (data.success) {
        setListaParticipantes(data.users);
      } else {
        alert("Error al cargar participantes: " + data.error);
      }
    } catch (e) { console.error("Error fetchParticipantes:", e); }
    finally { setCargandoParticipantes(false); }
  };

  const matricularUsuario = async () => {
    if (!busquedaParticipante.trim()) return;
    const token = localStorage.getItem('moodle_token');
    try {
      const response = await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_enrolments.php?token=${token}&action=enrol&courseid=${encodeURIComponent(id)}&email=${encodeURIComponent(busquedaParticipante)}`);
      const data = await response.json();
      if (data.success) {
        setBusquedaParticipante('');
        fetchParticipantes();
      } else {
        alert(data.error);
      }
    } catch (e) { console.error("Error matricularUsuario:", e); }
  };

  const desmatricularUsuario = async (userId) => {
    if (!window.confirm("¿Seguro que quieres desmatricular a este usuario?")) return;
    const token = localStorage.getItem('moodle_token');
    try {
      const response = await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_enrolments.php?token=${token}&action=unenrol&courseid=${encodeURIComponent(id)}&userid=${userId}`);
      const data = await response.json();
      if (data.success) {
        fetchParticipantes();
      } else {
        alert(data.error);
      }
    } catch (e) { console.error("Error desmatricularUsuario:", e); }
  };

  useEffect(() => {
    if (participantesAbierto) fetchParticipantes();
  }, [participantesAbierto]);

  const handleDragStart = (e, mod, seccionIdx) => {
    setDraggedMod({ mod, seccionIdx });
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e, targetModId) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
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

    const nuevasSecciones = [...secciones];
    nuevasSecciones[sourceSecIdx].modules = nuevasSecciones[sourceSecIdx].modules.filter(m => m.id !== sourceMod.id);
    if (!nuevasSecciones[targetSeccionIdx].modules) nuevasSecciones[targetSeccionIdx].modules = [];

    let beforeCmId = 0;
    if (targetMod) {
      let targetModIdx = nuevasSecciones[targetSeccionIdx].modules.findIndex(m => m.id === targetMod.id);
      if (position === 'bottom') targetModIdx += 1;
      nuevasSecciones[targetSeccionIdx].modules.splice(targetModIdx, 0, sourceMod);
      const modBelow = nuevasSecciones[targetSeccionIdx].modules[targetModIdx + 1];
      beforeCmId = modBelow ? modBelow.id : 0;
    } else {
      nuevasSecciones[targetSeccionIdx].modules.push(sourceMod);
    }

    setSecciones(nuevasSecciones);
    setDropIndicator(null);
    setDraggedMod(null);

    const token = localStorage.getItem('moodle_token');
    const targetSectionId = nuevasSecciones[targetSeccionIdx].id;
    const paramBefore = beforeCmId ? `&beforecmid=${beforeCmId}` : '';

    try {
      await fetch(`/moodle_api/proyecto_curso/api_persistente/tesis_actions.php?token=${token}&action=move&cmid=${sourceMod.id}&targetsection=${targetSectionId}${paramBefore}`);
    } catch (e) {
      console.error('Error al mover en Moodle:', e);
      fetchContenido();
    }
  };

  return (
    <PageContainer className="flex flex-col gap-6 relative">
      <div>
        <Link to="/dashboard" className="text-kenth-brightred hover:text-white flex items-center gap-2 mb-4 transition font-bold text-sm tracking-widest uppercase">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
          Volver al Catálogo
        </Link>
        
        {!cargando && (
          <>
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
              <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-kenth-text uppercase drop-shadow">
                {courseName}
              </h1>
              {esProfesor && (
                <div className="flex gap-3">
                  <button 
                    onClick={() => setParticipantesAbierto(true)}
                    className="bg-kenth-surface/10 hover:bg-indigo-500 text-kenth-text border border-kenth-border px-4 py-2 rounded-xl transition flex items-center gap-2 font-bold text-xs uppercase tracking-widest"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                    Participantes
                  </button>
                  <button 
                    onClick={() => navigate(`/dashboard/settings/${id}`)}
                    className="bg-kenth-surface/10 hover:bg-kenth-surface/20 text-kenth-text border border-kenth-border px-4 py-2 rounded-xl transition flex items-center gap-2 font-bold text-xs uppercase tracking-widest"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                    Configuración
                  </button>
                </div>
              )}
            </div>
            <div className="h-px bg-kenth-surface/30 w-full mb-6"></div>
          </>
        )}
      </div>

      {cargando && <CourseSkeleton />}

      {error && (
        <div className="bg-red-900/20 border-l-4 border-kenth-brightred p-6 rounded-r-xl">
          <p className="text-red-200 font-bold font-sans">Ha ocurrido un problema: {error}</p>
        </div>
      )}

      {!cargando && !error && (
        <div className="flex flex-col gap-6">
          {/* Botón para añadir sección al inicio si eres profesor */}
          {esProfesor && (
             <div className="flex justify-center -mb-4 group/addsec">
                <button 
                  onClick={() => añadirSeccion(0)}
                  className="bg-kenth-surface/10 hover:bg-emerald-500 text-kenth-subtext hover:text-white px-4 py-2 rounded-full text-[10px] font-black uppercase tracking-widest transition-all opacity-0 group-hover/addsec:opacity-100 flex items-center gap-2 border border-kenth-border hover:border-emerald-500 shadow-lg"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" /></svg>
                  Insertar sección aquí
                </button>
             </div>
          )}

          {secciones.map((seccion, secIdx) => {
            const tieneMenuAbierto = seccion.modules?.some(m => m.id === menuActivo);

            return (
              <React.Fragment key={seccion.id}>
              <div
                className={`bg-kenth-card rounded-[1rem] p-6 border border-kenth-border relative transition-all duration-300 ${tieneMenuAbierto ? 'z-40 shadow-2xl' : 'z-10'}`}
              >
                <div className="absolute inset-0 overflow-hidden rounded-[1rem] pointer-events-none">
                  <div className="absolute -top-10 -right-10 w-32 h-32 bg-kenth-surface/10 rounded-full blur-[50px]"></div>
                </div>

                {/* Menú de Sección en la Esquina Derecha */}
                {esProfesor && seccion.section > 0 && (
                  <div className="absolute top-6 right-6 z-30">
                    <button
                      onClick={(e) => { e.stopPropagation(); setMenuSeccionActivo(menuSeccionActivo === seccion.id ? null : seccion.id); }}
                      className={`p-2 rounded-xl transition ${menuSeccionActivo === seccion.id ? 'text-kenth-text bg-kenth-surface/20' : 'text-gray-500 hover:text-white hover:bg-kenth-surface/10'}`}
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="5" r="2" /><circle cx="12" cy="12" r="2" /><circle cx="12" cy="19" r="2" /></svg>
                    </button>

                    {menuSeccionActivo === seccion.id && (
                      <div
                        onClick={(e) => e.stopPropagation()}
                        className="absolute right-0 top-full mt-2 w-56 bg-kenth-bg border border-kenth-border rounded-xl shadow-[0_20px_50px_rgba(0,0,0,0.8)] z-[80] py-2 animate-in fade-in zoom-in-95 duration-200"
                      >
                        <div className="px-4 py-2 border-b border-kenth-border mb-1">
                          <p className="text-[10px] font-black text-kenth-subtext uppercase tracking-[0.2em]">Opciones de Tema</p>
                        </div>
                        <button 
                          onClick={() => { 
                            setMenuSeccionActivo(null); 
                            setEditandoSummaryId(seccion.id); 
                            // Limpiar etiquetas HTML para que el usuario edite texto plano
                            const tempDiv = document.createElement("div");
                            tempDiv.innerHTML = seccion.summary || '';
                            setNuevoSummarySeccion(tempDiv.textContent || tempDiv.innerText || ""); 
                          }} 
                          className="w-full text-left px-4 py-2.5 text-sm text-kenth-subtext hover:bg-kenth-surface/10 hover:text-kenth-text flex items-center gap-3 transition"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                          Editar descripción
                        </button>
                        <button 
                          onClick={() => { setMenuSeccionActivo(null); borrarSeccion(seccion.id); }} 
                          className="w-full text-left px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 flex items-center gap-3 transition"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                          Borrar esta sección
                        </button>
                      </div>
                    )}
                  </div>
                )}

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
                        className="flex-1 bg-kenth-surface/10 text-kenth-text font-bold text-xl border-b-2 border-kenth-brightred px-2 py-1 outline-none transition-colors"
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
                      <h2 className="text-2xl font-bold text-kenth-text">{seccion.name || `Tema ${seccion.section}`}</h2>
                      {esProfesor && (
                        <div className="flex items-center gap-1 opacity-0 group-hover/titulo:opacity-100 transition-all">
                          <button
                            onClick={() => {
                              setEditandoSeccionId(seccion.id);
                              setNuevoNombreSeccion(seccion.name || `Tema ${seccion.section}`);
                            }}
                            className="text-gray-500 hover:text-kenth-brightred transition-all p-1"
                            title="Editar título"
                          >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                          </button>

                          <div className="flex gap-0.5 ml-2 border-l border-kenth-border pl-2">
                             <button 
                                disabled={seccion.section <= 1 || seccionEnMovimientoId}
                                onClick={() => moverSeccion(seccion.id, seccion.section - 1)}
                                className="text-kenth-subtext hover:text-white disabled:opacity-20 p-1 transition"
                                title="Subir sección"
                             >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 15l7-7 7 7" /></svg>
                             </button>
                             <button 
                                disabled={secIdx === secciones.length - 1 || seccionEnMovimientoId}
                                onClick={() => moverSeccion(seccion.id, seccion.section + 1)}
                                className="text-kenth-subtext hover:text-white disabled:opacity-20 p-1 transition"
                                title="Bajar sección"
                             >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" /></svg>
                             </button>
                          </div>
                        </div>
                      )}
                    </>
                  )}
                </div>

                {editandoSummaryId === seccion.id ? (
                  <div className="mt-4 animate-in fade-in slide-in-from-top-2 duration-300">
                    <textarea
                      autoFocus
                      value={nuevoSummarySeccion}
                      onChange={(e) => setNuevoSummarySeccion(e.target.value)}
                      placeholder="Escribe una breve descripción para este tema..."
                      className="w-full bg-kenth-surface/5 text-kenth-subtext text-sm p-4 rounded-xl border border-kenth-border focus:border-kenth-brightred outline-none min-h-[100px] transition-all"
                    />
                    <div className="flex justify-end gap-2 mt-2">
                      <button onClick={() => setEditandoSummaryId(null)} className="px-4 py-2 text-xs font-bold text-kenth-subtext hover:text-white transition uppercase">
                        Cancelar
                      </button>
                      <button 
                        onClick={() => guardarSummarySeccion(seccion.id, secIdx)} 
                        className="bg-kenth-brightred text-white px-4 py-2 rounded-lg text-xs font-bold uppercase hover:bg-kenth-brightred/80 transition shadow-lg"
                      >
                        Guardar Descripción
                      </button>
                    </div>
                  </div>
                ) : (
                  seccion.summary && <div className="text-kenth-subtext text-sm mb-4 relative z-10" dangerouslySetInnerHTML={{ __html: seccion.summary }}></div>
                )}

                <div className="flex flex-col gap-1 mt-4 relative z-10">
                  {esProfesor && seccion.modules && seccion.modules.length > 0 && (
                    <div className="flex justify-center py-2 group/insert">
                      <button
                        onClick={() => { setSeccionDestinoId(seccion.section); setChooserAbierto(true); }}
                        className="w-10 h-10 rounded-full border-2 border-dashed border-kenth-border hover:border-kenth-brightred text-kenth-subtext hover:text-kenth-brightred flex items-center justify-center transition-all opacity-30 group-hover/insert:opacity-100 hover:!opacity-100 hover:scale-110 bg-kenth-bg"
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
                                  bg-kenth-surface/5 p-4 rounded-lg flex items-center gap-4 border border-kenth-border/50 transition-all duration-200 group/card relative
                                  ${mod.url ? 'cursor-pointer hover:border-kenth-brightred/50 hover:-translate-y-0.5 shadow-md' : 'border-transparent'}
                                  ${mod.visible === 0 ? 'opacity-40 grayscale' : ''}
                                  ${draggedMod?.mod.id === mod.id ? 'opacity-20 scale-[0.98]' : ''}
                                  ${menuActivo === mod.id ? 'z-[60] ring-1 ring-kenth-surface' : 'z-10 hover:z-20'}
                                `}
                        >
                          {dropIndicator?.id === mod.id && dropIndicator.position === 'top' && (
                            <div className="absolute top-[-2px] left-0 w-full h-[3px] bg-indigo-500 rounded-full shadow-[0_0_10px_#6366f1] z-50 pointer-events-none"></div>
                          )}
                          {dropIndicator?.id === mod.id && dropIndicator.position === 'bottom' && (
                            <div className="absolute bottom-[-2px] left-0 w-full h-[3px] bg-indigo-500 rounded-full shadow-[0_0_10px_#6366f1] z-50 pointer-events-none"></div>
                          )}
                          {esProfesor && (
                            <div className="cursor-grab active:cursor-grabbing text-kenth-subtext hover:text-kenth-text transition opacity-0 group-hover/card:opacity-100 flex-shrink-0" title="Arrastrar para mover">
                              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><circle cx="9" cy="5" r="1.5" /><circle cx="15" cy="5" r="1.5" /><circle cx="9" cy="12" r="1.5" /><circle cx="15" cy="12" r="1.5" /><circle cx="9" cy="19" r="1.5" /><circle cx="15" cy="19" r="1.5" /></svg>
                            </div>
                          )}

                          <div className="flex items-center gap-4 flex-1 min-w-0" onClick={() => mod.url && setVisorActivo(mod)}>
                            <img src={mod.modicon} alt={mod.modname} className={`w-8 h-8 rounded flex-shrink-0 ${mod.visible === 0 ? 'opacity-50' : ''}`} />
                            <div className="flex flex-col flex-1 min-w-0">
                              <span className={`font-semibold text-kenth-text transition truncate ${mod.url && 'group-hover/card:text-kenth-brightred'} ${mod.visible === 0 ? 'line-through text-kenth-subtext' : ''}`}>
                                {mod.name} {mod.visible === 0 && <span className="text-xs text-red-500 ml-2 no-underline tracking-widest">(Oculto a estudiantes)</span>}
                              </span>
                              <span className="text-[10px] text-kenth-subtext uppercase tracking-widest font-bold">{mod.modplural}</span>
                            </div>
                          </div>

                          {esProfesor && (
                            <div className="relative flex-shrink-0">
                              <button
                                onClick={(e) => { e.stopPropagation(); setMenuActivo(menuActivo === mod.id ? null : mod.id); }}
                                className={`p-2 rounded-lg transition ${menuActivo === mod.id ? 'text-kenth-text bg-kenth-surface/20' : 'text-kenth-subtext hover:text-kenth-text hover:bg-kenth-surface/10 opacity-0 group-hover/card:opacity-100'}`}
                              >
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="5" r="2" /><circle cx="12" cy="12" r="2" /><circle cx="12" cy="19" r="2" /></svg>
                              </button>

                              {menuActivo === mod.id && (
                                <div
                                  onClick={(e) => e.stopPropagation()}
                                  className="absolute right-0 top-12 w-48 bg-kenth-card border border-kenth-border rounded-xl shadow-[0_15px_40px_rgba(0,0,0,0.2)] z-[70] py-2 animate-in fade-in zoom-in-95 duration-200"
                                >
                                  <button onClick={() => abrirEdicion(mod)} className="w-full text-left px-4 py-2.5 text-sm text-kenth-subtext hover:bg-kenth-surface/10 hover:text-kenth-text flex items-center gap-3 transition">
                                    <svg className="w-4 h-4 text-kenth-subtext" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                                    Editar ajustes
                                  </button>
                                  <button onClick={() => ejecutarAccion(mod.visible !== 0 ? 'hide' : 'show', mod.id, secIdx)} className="w-full text-left px-4 py-2.5 text-sm text-kenth-subtext hover:bg-kenth-surface/10 hover:text-kenth-text flex items-center gap-3 transition">
                                    <svg className="w-4 h-4 text-kenth-subtext/60" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d={mod.visible !== 0 ? "M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.879L21 21" : "M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268-2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542 7-4.477 0-8.268-2.943-9.542 7-4.477 0-8.268-2.943-9.542-7z"} /></svg>
                                    {mod.visible !== 0 ? 'Ocultar' : 'Mostrar'}
                                  </button>
                                  <button onClick={() => ejecutarAccion('duplicate', mod.id, secIdx)} className="w-full text-left px-4 py-2.5 text-sm text-kenth-subtext hover:bg-kenth-surface/10 hover:text-kenth-text flex items-center gap-3 transition">
                                    <svg className="w-4 h-4 text-kenth-subtext/60" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                                    Duplicar
                                  </button>
                                  <div className="h-px bg-kenth-border my-1"></div>
                                  <button onClick={() => { if (window.confirm('¿Eliminar recurso permanentemente?')) ejecutarAccion('delete', mod.id, secIdx); }} className="w-full text-left px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 flex items-center gap-3 transition">
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                                    Borrar
                                  </button>
                                </div>
                              )}
                            </div>
                          )}
                        </div>

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
                    <div
                      onDragOver={esProfesor ? (e) => { e.preventDefault(); setDropIndicator({ id: `empty-${seccion.id}`, position: 'top' }); } : undefined}
                      onDrop={esProfesor ? (e) => handleDrop(e, null, secIdx) : undefined}
                      onDragLeave={() => setDropIndicator(null)}
                      className={`
                              text-gray-500 text-sm italic py-10 text-center border-2 border-dashed rounded-xl transition-all duration-300 flex flex-col items-center gap-3
                              ${dropIndicator?.id === `empty-${seccion.id}` ? 'border-indigo-500 bg-indigo-500/5 text-indigo-300' : 'border-gray-700/30 bg-transparent'}
                            `}
                    >
                      <span className="text-kenth-subtext">Este tema no tiene contenido aún.</span>
                      {esProfesor && (
                        <button
                          onClick={() => { setSeccionDestinoId(seccion.section); setChooserAbierto(true); }}
                          className="bg-kenth-brightred/10 text-kenth-brightred px-4 py-2 rounded-lg text-xs font-bold uppercase border border-kenth-brightred/20 hover:bg-kenth-brightred hover:text-white transition-all shadow-sm"
                        >
                          + Crear primer recurso
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
              
              {/* Botón para añadir sección después de esta */}
              {esProfesor && (
                 <div className="flex justify-center -my-3 group/addsec z-20 relative">
                    <button 
                      onClick={() => añadirSeccion(seccion.section + 1)}
                      className="bg-kenth-surface/10 hover:bg-emerald-500 text-kenth-subtext hover:text-white px-4 py-2 rounded-full text-[10px] font-black uppercase tracking-widest transition-all opacity-0 group-hover/addsec:opacity-100 flex items-center gap-2 border border-kenth-border hover:border-emerald-500 shadow-lg"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" /></svg>
                      Insertar sección aquí
                    </button>
                 </div>
              )}
              </React.Fragment>
            );
          })}
        </div>
      )}

      {esProfesor && chooserAbierto && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-kenth-card w-full max-w-4xl rounded-2xl flex flex-col border border-kenth-border overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.2)]">
            <div className="p-6 border-b border-kenth-border flex justify-between items-center bg-kenth-surface/5">
              <h2 className="text-xl font-bold text-kenth-text uppercase tracking-wider">Añadir recurso (Tema {seccionDestinoId})</h2>
              <button onClick={() => setChooserAbierto(false)} className="text-kenth-subtext hover:text-kenth-text bg-kenth-surface/10 p-2 rounded-lg transition">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
            <div className="p-6 max-h-[70vh] overflow-y-auto">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {HERRAMIENTAS_MOODLE.map((herramienta) => {
                   const idInvalido = !id || id === '0';
                   return (
                    <button
                     key={herramienta.id}
                     disabled={idInvalido}
                     onClick={() => {
                       if (idInvalido) return;
                       setHerramientaAvanzada(herramientaAvanzada === herramienta.id ? herramienta.id + ' ' : herramienta.id);
                       setChooserAbierto(false);
                       setStudioCargando(true);
                       setStudioAbierto(true);
                     }}
                     className={`group flex flex-col items-center justify-center p-6 bg-kenth-surface/5 border border-kenth-border rounded-xl transition-all duration-300 ${idInvalido ? 'opacity-20 cursor-not-allowed grayscale' : 'hover:border-kenth-brightred hover:-translate-y-1 hover:shadow-[0_10px_20px_rgba(225,29,72,0.1)]'}`}
                   >
                     <div className={`w-14 h-14 rounded-full ${herramienta.bg} ${herramienta.color} border ${herramienta.border} flex items-center justify-center text-2xl mb-3 transition-transform ${!idInvalido && 'group-hover:scale-110'}`}>{herramienta.icono}</div>
                     <span className="text-sm font-semibold text-kenth-subtext group-hover:text-kenth-text">{herramienta.nombre}</span>
                   </button>
                   );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {esProfesor && studioAbierto && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/95 p-2 md:p-6 backdrop-blur-md animate-in fade-in duration-300">
          <div className="bg-kenth-card w-full h-full max-w-[1400px] max-h-[900px] rounded-2xl flex flex-col border border-indigo-500/30 overflow-hidden shadow-[0_0_80px_rgba(79,70,229,0.2)]">
            <div className="p-4 flex justify-between items-center border-b border-indigo-500/30 bg-kenth-bg">
              <div className="flex items-center gap-3">
                <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                <h2 className="text-kenth-text font-bold text-lg tracking-wider uppercase">Moodle Studio</h2>
                <span className="bg-indigo-600 text-white text-[10px] uppercase font-bold py-1 px-2 rounded-full">{herramientaAvanzada === '__edit__' ? 'Editando' : 'Creando'}</span>
              </div>
              <button onClick={() => { setStudioAbierto(false); window.__kenth_edit_cmid = null; fetchContenido(); }} className="text-kenth-subtext hover:text-white bg-red-500/10 hover:bg-red-500 px-4 py-2 rounded-lg transition font-bold text-xs tracking-widest uppercase flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg> Cerrar
              </button>
            </div>
            <div className="flex-1 w-full bg-kenth-bg relative overflow-hidden">
              {studioCargando && (
                <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-kenth-bg text-indigo-400 gap-4 animate-in fade-in duration-300">
                  <svg className="animate-spin h-12 w-12" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span className="font-bold tracking-widest uppercase text-xs animate-pulse">Iniciando entorno Moodle Studio...</span>
                </div>
              )}
              <iframe
                name="moodle_studio_iframe"
                onLoad={() => setStudioCargando(false)}
                src={
                  (() => {
                    if (!id || id === '0') return 'about:blank'; // Evitar course=0 crítico

                    const token = localStorage.getItem('moodle_token');
                    return herramientaAvanzada === '__edit__'
                      ? `/moodle_api/proyecto_curso/api_persistente/tesis_studio.php?token=${token}&courseid=${encodeURIComponent(id)}&modname=__edit__&cmid=${window.__kenth_edit_cmid || 0}`
                      : `/moodle_api/proyecto_curso/api_persistente/tesis_studio.php?token=${token}&courseid=${encodeURIComponent(id)}&modname=${herramientaAvanzada}&section=${seccionDestinoId}`;
                  })()
                }
                className={`w-full h-full absolute inset-0 border-none transition-opacity duration-700 bg-kenth-bg ${studioCargando ? 'opacity-0' : 'opacity-100'}`}
                allow="fullscreen *; geolocation *; microphone *; camera *; midi *; encrypted-media *; autoplay *"
              />
            </div>
          </div>
        </div>
      )}

      {esProfesor && participantesAbierto && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 p-4 backdrop-blur-md animate-in fade-in duration-300">
          <div className="bg-kenth-card w-full max-w-5xl h-[85vh] rounded-3xl flex flex-col border border-kenth-border overflow-hidden shadow-[0_0_100px_rgba(0,0,0,0.5)]">
            <div className="p-6 border-b border-kenth-border flex justify-between items-center bg-kenth-surface/5">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-indigo-500/10 rounded-2xl flex items-center justify-center text-indigo-400 border border-indigo-500/20 shadow-inner">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                </div>
                <div>
                  <h2 className="text-2xl font-black text-kenth-text uppercase tracking-tight">Gestión de Participantes</h2>
                  <p className="text-xs text-kenth-subtext font-bold tracking-widest uppercase">Control de Acceso y Matriculaciones</p>
                </div>
              </div>
              <button onClick={() => setParticipantesAbierto(false)} className="text-kenth-subtext hover:text-white bg-kenth-surface/10 p-3 rounded-2xl transition-all hover:rotate-90">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>

            <div className="p-6 bg-kenth-surface/5 border-b border-kenth-border flex flex-col md:flex-row gap-4 items-center">
              <div className="relative flex-1 w-full">
                <input 
                  type="text" 
                  value={busquedaParticipante}
                  onChange={(e) => setBusquedaParticipante(e.target.value)}
                  placeholder="Matricular por email o nombre de usuario..."
                  className="w-full bg-kenth-bg text-kenth-text border border-kenth-border px-5 py-4 rounded-2xl focus:border-indigo-500 outline-none transition shadow-inner font-medium"
                />
              </div>
              <button 
                onClick={matricularUsuario}
                className="bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-4 rounded-2xl font-black text-xs uppercase tracking-[0.2em] transition-all shadow-[0_10px_20px_rgba(79,70,229,0.3)] active:scale-95 whitespace-nowrap"
              >
                Matricular Usuario
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 custom-scrollbar bg-kenth-bg/50">
              {cargandoParticipantes ? (
                <div className="h-full flex items-center justify-center text-kenth-subtext animate-pulse font-bold tracking-widest uppercase text-xs">Cargando participantes...</div>
              ) : listaParticipantes.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-kenth-subtext gap-4">
                  <svg className="w-16 h-16 opacity-20" fill="none" stroke="currentColor" strokeWidth={1} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                  <span className="font-bold tracking-widest uppercase text-xs">No se encontraron participantes matriculados</span>
                </div>
              ) : (
                <div className="grid grid-cols-1 gap-3">
                  {listaParticipantes.map((user) => (
                    <div key={user.id} className="bg-kenth-card/50 border border-kenth-border/50 p-4 rounded-2xl flex items-center justify-between group hover:border-indigo-500/30 transition-all hover:bg-kenth-card">
                      <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-full bg-kenth-surface/20 border border-kenth-border flex items-center justify-center font-bold text-lg text-indigo-400 shadow-md">
                          {user.fullname.charAt(0)}
                        </div>
                        <div className="flex flex-col">
                          <span className="text-kenth-text font-black tracking-tight">{user.fullname}</span>
                          <span className="text-xs text-kenth-subtext font-medium">{user.email}</span>
                          <div className="flex gap-2 mt-1.5">
                            {user.roles.map((role, idx) => (
                              <span key={idx} className={`text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full border ${user.isAdmin ? 'bg-amber-500/10 text-amber-500 border-amber-500/20' : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'}`}>
                                {role}
                              </span>
                            ))}
                            {user.isAdmin && (
                              <span className="text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-full bg-red-500/10 text-red-500 border border-red-500/20">
                                Site Admin
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      {user.canBeUnenrolled && (
                        <button 
                          onClick={() => desmatricularUsuario(user.id)}
                          className="opacity-0 group-hover:opacity-100 bg-red-500/10 hover:bg-red-500 text-red-500 hover:text-white p-3 rounded-xl transition-all duration-300 font-bold text-[10px] uppercase tracking-widest border border-red-500/20"
                          title="Eliminar del curso"
                        >
                          Desmatricular
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {visorActivo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-2 md:p-10 animate-kenth-blur">
          <div className="bg-kenth-card w-full h-full max-w-6xl rounded-[2.5rem] flex flex-col border border-kenth-border overflow-hidden shadow-[0_0_100px_rgba(0,0,0,0.6)] animate-kenth-pop">
            <div className="p-5 flex justify-between items-center border-b border-kenth-border bg-kenth-surface/5 backdrop-blur-xl relative">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 bg-kenth-surface/10 rounded-2xl flex items-center justify-center p-2 border border-kenth-border shadow-inner">
                  <img src={visorActivo.modicon} alt="icon" className="w-full h-full object-contain" />
                </div>
                <div>
                  <h2 className="text-kenth-text font-black text-xl tracking-tight uppercase leading-none">{visorActivo.name}</h2>
                  <p className="text-[10px] text-kenth-brightred font-black tracking-widest uppercase mt-1 opacity-80">Recurso Interactivo</p>
                </div>
              </div>
              <button 
                onClick={() => setVisorActivo(null)} 
                className="group relative overflow-hidden bg-kenth-surface/10 hover:bg-kenth-brightred text-kenth-subtext hover:text-white px-6 py-2.5 rounded-2xl transition-all duration-300 font-black text-[10px] tracking-widest uppercase flex items-center gap-3 border border-kenth-border hover:border-kenth-brightred hover:shadow-[0_0_20px_rgba(225,29,72,0.4)]"
              >
                <span className="relative z-10 flex items-center gap-2">
                  <svg className="w-4 h-4 transition-transform group-hover:rotate-90 duration-300" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg> 
                  Cerrar Recurso
                </span>
              </button>
            </div>
            <div className={`flex-1 w-full bg-kenth-bg relative scrollbar-hide ${['h5pactivity', 'hvp'].includes(visorActivo?.modname) ? 'p-0 overflow-hidden min-h-0' : 'p-4 md:p-10 overflow-y-auto min-h-0'}`}>
              <MoodleRenderer modulo={visorActivo} />
            </div>
            <div className="h-1 w-full bg-gradient-to-r from-transparent via-kenth-brightred/50 to-transparent" />
          </div>
        </div>
      )}
    </PageContainer>
  );
}