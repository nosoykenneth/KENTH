import React, { useState, useEffect } from 'react';

export default function MoodleRenderer({ modulo }) {
  const miToken = localStorage.getItem('moodle_token');
  const [htmlContent, setHtmlContent] = useState('');
  const [cargando, setCargando] = useState(false);
  const [enIntento, setEnIntento] = useState(false);

  useEffect(() => {
    // Resetear intento si se cambia de modulo
    setEnIntento(false);
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
        <div className="prose prose-invert prose-rose max-w-none animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div dangerouslySetInnerHTML={{ __html: htmlContent || modulo.description || '' }} />
        </div>
      );

    case 'assign':
    case 'forum':
      return (
        <div className="bg-[#2D2D30] p-8 rounded-3xl border border-kenth-surface/20 relative overflow-hidden animate-in fade-in slide-in-from-bottom-4 zoom-in-95 duration-500">
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-emerald-500 to-indigo-500"></div>
          <h3 className="text-3xl font-extrabold text-white mb-6 uppercase flex items-center gap-4">
             {modulo.modname === 'assign' ? '📝 Tarea Asignada' : '💬 Foro de Discusión'}
          </h3>
          <div className="prose prose-invert prose-indigo max-w-none text-gray-300">
             <div dangerouslySetInnerHTML={{ __html: modulo.description || 'No hay instrucciones para esta actividad.' }} />
          </div>
        </div>
      );

    case 'quiz':
      return (
        <div className="bg-[#2D2D30] rounded-3xl border border-orange-500/30 overflow-hidden relative shadow-2xl animate-in fade-in duration-500">
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-orange-400 to-rose-500"></div>
          <div className="p-8 md:p-12 flex flex-col items-center text-center">
            <div className="w-20 h-20 bg-orange-400/10 rounded-full flex items-center justify-center mb-6 border border-orange-500/20 shadow-[0_0_30px_rgba(251,146,60,0.2)]">
               <svg className="w-10 h-10 text-orange-400" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            
            <h3 className="text-3xl font-extrabold text-white mb-4 uppercase tracking-wider">{modulo.name}</h3>
            
            <div className="prose prose-invert prose-orange max-w-2xl mx-auto mb-8 text-gray-300">
               <div dangerouslySetInnerHTML={{ __html: modulo.description || '<p>Este es un cuestionario automatizado de evaluación continua. Haz clic en el botón inferior para abrir el entorno seguro de examen.</p>' }} />
            </div>
            
            <div className="bg-[#1e1e20] w-full max-w-lg p-6 rounded-2xl border border-kenth-surface/50 mb-8 flex flex-col md:flex-row justify-around gap-4 text-sm font-bold text-gray-400">
               <div className="flex flex-col items-center">
                  <span className="text-orange-400 text-2xl mb-1 mt-1">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  </span>
                  Asíncrono
               </div>
               <div className="flex flex-col items-center">
                  <span className="text-orange-400 text-2xl mb-1 mt-1">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" /></svg>
                  </span>
                  Autocalificable
               </div>
            </div>

            {!enIntento ? (
              <button 
                onClick={() => setEnIntento(true)}
                className="bg-gradient-to-r from-orange-500 to-rose-500 hover:from-orange-400 hover:to-rose-400 text-white font-bold py-4 px-10 rounded-xl uppercase tracking-widest shadow-[0_10px_25px_rgba(249,115,22,0.3)] hover:-translate-y-1 transition-all flex items-center gap-3"
              >
                Cargar Motor de Evaluación
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
              </button>
            ) : (
              <div className="w-full bg-[#1e1e20] rounded-2xl border border-kenth-surface/50 overflow-hidden h-[600px] relative animate-in fade-in zoom-in-95 duration-500 shadow-inner">
                <iframe 
                  name="moodle_view_iframe"
                  src={`/moodle_api/tesis_view.php?token=${miToken}&cmid=${modulo.id}&modname=${modulo.modname}`}
                  className="w-full h-full absolute inset-0 border-none bg-[#1e1e20]"
                  allow="fullscreen *; microphone *; camera *"
                  title="Motor de Cuestionario Nivel Dios"
                />
              </div>
            )}
          </div>
        </div>
      );

    case 'url':
      const urlItem = modulo.contents?.[0];
      return (
        <div className="bg-[#1e1e20] p-10 rounded-3xl border-2 border-dashed border-sky-500/30 flex flex-col items-center text-center gap-6 animate-in fade-in duration-500">
          <div className="w-24 h-24 bg-sky-500/10 rounded-full flex items-center justify-center shadow-[0_0_40px_rgba(14,165,233,0.2)]">
            <svg className="w-12 h-12 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
          </div>
          <div>
            <h3 className="text-2xl font-bold text-white mb-2">{modulo.name}</h3>
            <p className="text-gray-400 max-w-md mx-auto">Este es un recurso externo. Al hacer clic, serás redirigido a la página de destino en una pestaña segura.</p>
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
        <div className="bg-[#2D2D30] rounded-3xl border border-kenth-surface/50 overflow-hidden shadow-2xl animate-in fade-in duration-500">
           <div className="bg-[#1e1e20] p-6 border-b border-white/5 flex items-center gap-4">
              <svg className="w-8 h-8 text-amber-500" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
              <div>
                <h3 className="text-xl font-bold text-white">Directorio Físico</h3>
                <p className="text-xs text-gray-500 tracking-wider uppercase">Archivos Adjuntos</p>
              </div>
           </div>
           <div className="p-2 md:p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {modulo.contents?.map((file, idx) => (
                 <a 
                   key={idx} 
                   href={`${file.fileurl.replace('http://localhost/', '/moodle_api/')}&token=${miToken}`} 
                   download={file.filename}
                   className="group p-4 bg-[#1a1a1c] border border-white/5 hover:border-amber-500/50 rounded-xl flex items-center gap-4 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_10px_20px_rgba(245,158,11,0.1)]"
                 >
                    <div className="w-10 h-10 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center shrink-0">
                       <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                    </div>
                    <div className="truncate">
                      <p className="text-sm font-bold text-white truncate group-hover:text-amber-400 transition">{file.filename}</p>
                      <p className="text-[10px] text-gray-500 uppercase">{file.mimetype || 'Archivo'}</p>
                    </div>
                 </a>
              ))}
              {(!modulo.contents || modulo.contents.length === 0) && (
                 <div className="col-span-full text-center text-gray-500 py-6 italic">Carpeta vacía</div>
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
        <div className="w-full h-full flex justify-center items-center p-4 md:p-8 bg-[#1e1e20]">
          
          {/* El marco visible: Le damos el tamaño exacto del video + la barra útil */}
          <div className="relative w-full max-w-[950px] rounded-2xl overflow-hidden shadow-[0_0_60px_rgba(0,0,0,0.8)] bg-[#1e1e20]">
            
            {/* 1. EL ESPACIO DEL VIDEO: 16:9 exacto */}
            <div style={{ paddingTop: '56.25%' }}></div>
            
            {/* 2. LA VENTANA DE LOS CONTROLES: Reducimos de 44px a 34px (lo que mide la barra azul) */}
            <div style={{ height: '36px' }}></div>
            
            {/* 3. EL IFRAME (El pozo profundo): Le damos 50px extras hacia abajo. 
                 H5P dibujará el video, luego los controles, y el "cachito negro" caerá
                 en esos 50px invisibles, siendo devorado por el overflow-hidden del marco. */}
            <iframe
              name="moodle_view_iframe"
              src={`/moodle_api/tesis_view.php?token=${miToken}&cmid=${modulo.id}&modname=${modulo.modname}`}
              className="absolute top-0 left-0 w-full border-none bg-transparent"
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
        <div className="bg-[#2D2D30] max-w-xl mx-auto p-8 rounded-3xl border border-kenth-surface/20 flex flex-col items-center text-center shadow-2xl animate-in fade-in duration-500">
           <svg className="w-16 h-16 text-teal-400 mb-6 drop-shadow-[0_0_15px_rgba(45,212,191,0.4)]" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
           <h3 className="text-2xl font-bold text-white mb-2">{modulo.name}</h3>
           <p className="text-gray-400 mb-8">{fileRes?.filename}</p>
           
           <a 
              href={fileRes ? `${fileRes.fileurl.replace('http://localhost/', '/moodle_api/')}&token=${miToken}` : '#'} 
              download 
              className="bg-teal-600 hover:bg-teal-500 focus:ring-4 focus:ring-teal-500/50 text-white py-4 px-10 rounded-2xl font-bold tracking-widest uppercase transition-all shadow-[0_10px_20px_rgba(13,148,136,0.3)] hover:-translate-y-1 hover:shadow-[0_15px_25px_rgba(13,148,136,0.4)]"
            >
              Descargar Archivo
           </a>
        </div>
      );

    default:
      return (
        <div className="p-10 text-center border-2 border-dashed border-white/10 rounded-3xl bg-[#1e1e20]">
          <svg className="w-12 h-12 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" /></svg>
          <h3 className="text-xl font-bold text-gray-300 mb-2">Construcción Nativa Pendiente</h3>
          <p className="text-gray-500">Este módulo (<span className="text-white font-mono">{modulo.modname}</span>) será rediseñado nativamente en iteraciones futuras.</p>
        </div>
      );
  }
}