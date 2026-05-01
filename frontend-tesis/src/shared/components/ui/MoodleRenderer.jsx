import React, { useState, useEffect } from 'react';

export default function MoodleRenderer({ modulo }) {
  const miToken = localStorage.getItem('moodle_token');
  const [htmlContent, setHtmlContent] = useState('');
  const [cargando, setCargando] = useState(false);
  const [enIntento, setEnIntento] = useState(false);
  const [iframeCargando, setIframeCargando] = useState(true);

  useEffect(() => {
    // Resetear intento si se cambia de modulo
    setEnIntento(false);
    setIframeCargando(true);
    // Solo hacemos fetch si es contenido de texto (Page/Label)
    if (['page', 'label'].includes(modulo.modname)) {
      const fetchData = async () => {
        setCargando(true);
        try {
          // Buscamos el contenido crudo en el array contents
          const contentObj = modulo.contents?.find(c => c.type === 'file' || c.content);
          if (contentObj?.content) {
            setHtmlContent(contentObj.content);
          } else if (contentObj?.fileurl) {
            const res = await fetch(`${contentObj.fileurl.replace('http://localhost/', '/moodle_api/')}&token=${miToken}`);
            const text = await res.text();
            setHtmlContent(text);
          }
        } catch (e) { console.error(e); }
        finally { setCargando(false); }
      };
      fetchData();
    }
  }, [modulo, miToken]);

  // RENDERIZADO POR TIPO (SIN IFRAMES NATIVAMENTE)
  switch (modulo.modname) {
    case 'page':
    case 'label':
      return (
        <div className="prose dark:prose-invert prose-rose max-w-none animate-kenth-slide relative min-h-[100px]">
          {cargando && !htmlContent && (
            <div className="flex items-center gap-4 text-kenth-brightred animate-pulse py-8 justify-center">
              <div className="relative">
                <div className="absolute inset-0 bg-kenth-brightred/20 blur-xl rounded-full animate-ping" />
                <svg className="animate-spin h-8 w-8 relative z-10" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <span className="text-sm font-black uppercase tracking-[0.2em] animate-pulse">Sincronizando Data...</span>
            </div>
          )}
          <div className="bg-kenth-card p-6 md:p-10 rounded-[2rem] border border-kenth-border shadow-inner" dangerouslySetInnerHTML={{ __html: htmlContent || modulo.description || '' }} />
        </div>
      );

    case 'assign':
    case 'forum':
      return (
        <div className="bg-kenth-card p-10 rounded-[2.5rem] border border-kenth-border relative overflow-hidden animate-kenth-pop shadow-2xl">
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-emerald-500 via-indigo-500 to-emerald-500 animate-gradient-x"></div>
          <div className="absolute -top-24 -right-24 w-48 h-48 bg-indigo-500/10 blur-[100px] rounded-full" />
          
          <h3 className="text-4xl font-black text-kenth-text mb-8 uppercase flex items-center gap-5 tracking-tighter">
             <span className="p-4 bg-kenth-surface/10 rounded-2xl border border-kenth-border shadow-inner">
               {modulo.modname === 'assign' ? '📝' : '💬'}
             </span>
             {modulo.modname === 'assign' ? 'Tarea de Curso' : 'Foro de Discusión'}
          </h3>
          <div className="prose dark:prose-invert prose-indigo max-w-none text-kenth-subtext bg-kenth-bg/20 p-8 rounded-3xl border border-kenth-border">
             <div dangerouslySetInnerHTML={{ __html: modulo.description || 'No hay instrucciones adicionales para esta actividad.' }} />
          </div>
        </div>
      );

    case 'quiz':
      return (
        <div className="bg-kenth-card rounded-[3rem] border border-kenth-border overflow-hidden relative shadow-[0_30px_60px_rgba(0,0,0,0.1)] animate-kenth-pop">
          <div className="absolute top-0 left-0 w-full h-3 bg-gradient-to-r from-orange-400 via-rose-500 to-orange-400"></div>
          <div className="p-10 md:p-16 flex flex-col items-center text-center">
            <div className="w-24 h-24 bg-orange-500/10 rounded-[2rem] flex items-center justify-center mb-8 border border-orange-500/30 shadow-[0_0_50px_rgba(251,146,60,0.3)] animate-pulse">
               <svg className="w-12 h-12 text-orange-400" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            
            <h3 className="text-4xl md:text-5xl font-black text-kenth-text mb-6 uppercase tracking-tighter leading-none">{modulo.name}</h3>
            
            <div className="prose dark:prose-invert prose-orange max-w-2xl mx-auto mb-10 text-kenth-subtext text-lg leading-relaxed">
               <div dangerouslySetInnerHTML={{ __html: modulo.description || '<p>Evaluación técnica automatizada. Haz clic debajo para iniciar el entorno de examen seguro.</p>' }} />
            </div>
            
            <div className="bg-kenth-bg/30 w-full max-w-xl p-8 rounded-[2rem] border border-kenth-border mb-10 flex flex-col md:flex-row justify-around gap-8 text-xs font-black text-kenth-subtext tracking-[0.2em] uppercase">
               <div className="flex flex-col items-center gap-3">
                  <div className="p-3 bg-orange-500/5 rounded-xl border border-orange-500/10">
                    <svg className="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  </div>
                  Modo Asíncrono
               </div>
               <div className="flex flex-col items-center gap-3">
                  <div className="p-3 bg-orange-500/5 rounded-xl border border-orange-500/10">
                    <svg className="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138z" /></svg>
                  </div>
                  Certificable
               </div>
            </div>

            {!enIntento ? (
              <button 
                onClick={() => setEnIntento(true)}
                className="group relative overflow-hidden bg-gradient-to-r from-orange-600 to-rose-600 hover:from-orange-500 hover:to-rose-500 text-white font-black py-5 px-14 rounded-2xl uppercase tracking-[0.2em] shadow-[0_20px_50px_rgba(225,29,72,0.3)] hover:-translate-y-1 transition-all flex items-center gap-4 text-sm"
              >
                <span className="relative z-10 flex items-center gap-3">
                  Iniciar Examen Seguro
                  <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
              </button>
            ) : (
              <div className="w-full bg-black/40 rounded-[2.5rem] border border-white/10 overflow-hidden h-[700px] relative animate-in fade-in zoom-in-95 duration-700 shadow-inner ring-1 ring-white/5">
                {iframeCargando && (
                  <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-[#1e1e20] text-orange-500 gap-6">
                    <div className="relative">
                      <div className="absolute inset-0 bg-orange-500/20 blur-2xl rounded-full animate-pulse" />
                      <svg className="animate-spin h-14 w-14 relative z-10" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    </div>
                    <span className="font-black tracking-[0.3em] uppercase text-[10px] animate-pulse">Desplegando Entorno Seguro...</span>
                  </div>
                )}
                <iframe 
                  name="moodle_view_iframe"
                  onLoad={() => setIframeCargando(false)}
                  src={`/moodle_api/proyecto_curso/api_persistente/tesis_view.php?token=${miToken}&cmid=${modulo.id}&modname=${modulo.modname}`}
                  className={`w-full h-full absolute inset-0 border-none bg-transparent transition-opacity duration-1000 ${iframeCargando ? 'opacity-0' : 'opacity-100'}`}
                  allow="fullscreen *; microphone *; camera *"
                  title="Evaluación Nivel Dios"
                />
              </div>
            )}
          </div>
        </div>
      );

    case 'url':
      const urlItem = modulo.contents?.[0];
      return (
        <div className="bg-[#1e1e20] p-10 rounded-3xl border-2 border-dashed border-sky-500/30 flex flex-col items-center text-center gap-6 animate-kenth-pop">
          <div className="w-24 h-24 bg-sky-500/10 rounded-full flex items-center justify-center shadow-[0_0_40px_rgba(14,165,233,0.2)]">
            <svg className="w-12 h-12 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
          </div>
          <div>
            <h3 className="text-2xl font-bold text-kenth-text mb-2">{modulo.name}</h3>
            <p className="text-kenth-subtext max-w-md mx-auto">Este es un recurso externo. Al hacer clic, serás redirigido a la página de destino en una pestaña segura.</p>
          </div>
          <a 
            href={urlItem?.fileurl || modulo.url} 
            target="_blank" 
            rel="noreferrer"
            className="bg-sky-600 hover:bg-sky-500 text-white px-8 py-3 rounded-xl font-bold transition shadow-lg flex items-center gap-2"
          >
            Abrir Enlace Web
            <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
          </a>
        </div>
      );

    case 'folder':
      return (
        <div className="bg-kenth-card rounded-[3rem] border border-kenth-border overflow-hidden shadow-[0_40px_80px_rgba(0,0,0,0.1)] animate-kenth-slide">
           <div className="bg-kenth-surface/10 p-8 border-b border-kenth-border flex items-center gap-6 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 blur-3xl rounded-full" />
              <div className="w-16 h-16 bg-amber-500/10 rounded-2xl flex items-center justify-center border border-amber-500/20 shadow-[0_0_20px_rgba(245,158,11,0.2)]">
                <svg className="w-8 h-8 text-amber-500" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
              </div>
              <div>
                <h3 className="text-2xl font-black text-kenth-text tracking-tighter uppercase leading-none">Repositorio Digital</h3>
                <p className="text-[10px] text-amber-500 font-black tracking-[0.3em] uppercase mt-2">Gestión de Archivos Adjuntos</p>
              </div>
           </div>
           <div className="p-8 md:p-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 bg-kenth-surface/5">
              {modulo.contents?.map((file, idx) => (
                 <a 
                   key={idx} 
                   href={`${file.fileurl.replace('http://localhost/', '/moodle_api/')}&token=${miToken}`} 
                   download={file.filename}
                   className="group p-6 bg-kenth-surface/10 border border-kenth-border hover:border-amber-500/50 rounded-3xl flex flex-col gap-4 transition-all duration-500 hover:-translate-y-2 hover:shadow-[0_20px_40px_rgba(245,158,11,0.15)] relative overflow-hidden"
                 >
                    <div className="absolute top-0 right-0 w-1 h-full bg-amber-500/0 group-hover:bg-amber-500 transition-all" />
                    <div className="w-12 h-12 rounded-xl bg-amber-500/5 text-amber-500 flex items-center justify-center border border-amber-500/10 group-hover:scale-110 group-hover:bg-amber-500 group-hover:text-black transition-all duration-500">
                       <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                    </div>
                    <div className="mt-2">
                      <p className="text-sm font-black text-kenth-text group-hover:text-amber-400 transition line-clamp-1">{file.filename}</p>
                      <p className="text-[9px] text-kenth-subtext font-black tracking-widest uppercase mt-1">
                        {file.mimetype?.split('/')[1] || 'Documento'} • {Math.round(file.filesize / 1024)} KB
                      </p>
                    </div>
                 </a>
              ))}
              {(!modulo.contents || modulo.contents.length === 0) && (
                 <div className="col-span-full text-center text-kenth-subtext py-12 italic font-medium">Este repositorio se encuentra temporalmente vacío.</div>
              )}
           </div>
        </div>
      );

    // ----------------------------------------
    // MODO INTERACTIVO (H5P) - ENCUADRE PERFECTO FINAL
    // ----------------------------------------
    case 'h5pactivity':
    case 'hvp':
      return (
        <div className="w-full h-full flex justify-center items-center p-4 md:p-8 bg-kenth-bg">
          
          {/* El marco visible: Le damos el tamaño exacto del video + la barra útil */}
          <div className="relative w-full max-w-[950px] rounded-2xl overflow-hidden shadow-[0_0_60px_rgba(0,0,0,0.2)] bg-kenth-bg animate-kenth-pop delay-300">
            
            {/* 1. EL ESPACIO DEL VIDEO: 16:9 exacto */}
            <div style={{ paddingTop: '56.25%' }}></div>
            
            {/* 2. LA VENTANA DE LOS CONTROLES: Reducimos de 44px a 34px (lo que mide la barra azul) */}
            <div style={{ height: '36px' }}></div>
            
            {/* 3. EL IFRAME (El pozo profundo): Le damos 50px extras hacia abajo. 
                 H5P dibujará el video, luego los controles, y el "cachito negro" caerá
                 en esos 50px invisibles, siendo devorado por el overflow-hidden del marco. */}
            {iframeCargando && (
              <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-kenth-bg text-indigo-400 gap-4">
                <svg className="animate-spin h-12 w-12" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span className="font-bold tracking-widest uppercase text-xs animate-pulse text-kenth-subtext">Sincronizando contenido H5P...</span>
              </div>
            )}
            <iframe
              name="moodle_view_iframe"
              onLoad={() => setIframeCargando(false)}
              src={`/moodle_api/proyecto_curso/api_persistente/tesis_view.php?token=${miToken}&cmid=${modulo.id}&modname=${modulo.modname}`}
              className={`absolute top-0 left-0 w-full border-none bg-transparent transition-opacity duration-700 ${iframeCargando ? 'opacity-0' : 'opacity-100'}`}
              style={{ height: 'calc(100% + 50px)' }}
              allow="fullscreen *; microphone *; camera *"
              scrolling="no" 
              title="Visor H5P Nativo"
            />
          </div>

        </div>
      );

    case 'resource':
      const fileRes = modulo.contents?.[0];
      return (
        <div className="bg-kenth-card max-w-2xl mx-auto p-12 rounded-[3rem] border border-kenth-border flex flex-col items-center text-center shadow-[0_40px_80px_rgba(0,0,0,0.2)] animate-kenth-pop relative overflow-hidden">
           <div className="absolute -top-24 -left-24 w-48 h-48 bg-teal-500/5 blur-[80px] rounded-full" />
           <div className="w-24 h-24 bg-teal-500/10 rounded-[2rem] flex items-center justify-center mb-8 border border-teal-500/20 shadow-[0_0_40px_rgba(20,184,166,0.2)]">
              <svg className="w-12 h-12 text-teal-400" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
           </div>
           <h3 className="text-4xl font-black text-kenth-text mb-4 uppercase tracking-tighter leading-tight">{modulo.name}</h3>
           <p className="text-kenth-subtext text-lg mb-10 font-medium italic opacity-70 px-6">{fileRes?.filename || 'Documento de Referencia'}</p>
           
           <a 
              href={fileRes ? `${fileRes.fileurl.replace('http://localhost/', '/moodle_api/')}&token=${miToken}` : '#'} 
              download 
              className="group relative overflow-hidden bg-teal-600 hover:bg-teal-500 text-white py-5 px-16 rounded-[2rem] font-black tracking-[0.2em] uppercase transition-all shadow-[0_20px_40px_rgba(13,148,136,0.3)] hover:-translate-y-2 hover:shadow-[0_30px_60px_rgba(13,148,136,0.4)]"
            >
              <span className="relative z-10 flex items-center gap-3">
                Descargar Material
                <svg className="w-5 h-5 animate-bounce" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
           </a>
        </div>
      );

    default:
      return (
        <div className="p-10 text-center border-2 border-dashed border-kenth-border rounded-3xl bg-kenth-bg/20">
          <svg className="w-12 h-12 text-kenth-subtext/40 mx-auto mb-4" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" /></svg>
          <h3 className="text-xl font-bold text-kenth-subtext mb-2">Construcción Nativa Pendiente</h3>
          <p className="text-kenth-subtext">Este módulo (<span className="text-kenth-text font-mono">{modulo.modname}</span>) será rediseñado nativamente en iteraciones futuras.</p>
        </div>
      );
  }
}