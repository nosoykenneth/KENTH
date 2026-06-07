import React, { useEffect, useRef, useState } from 'react';
import { getStudentLessonResources } from '../../services/ragService';

const MEDIA_META = {
  image: { icon: '🖼️', label: 'Imagen' },
  audio: { icon: '🎵', label: 'Audio' },
  template: { icon: '🎛️', label: 'Plantilla DAW' },
  document: { icon: '📄', label: 'Documento' },
  file: { icon: '📎', label: 'Archivo' },
};

/**
 * StudentLessonResources
 * Botón "📎 Recursos (N)" en la barra del visor. Al pulsarlo despliega un panel con
 * los recursos VISIBLES de la lección (imágenes con preview, plantillas/audios/PDF
 * descargables). Si la lección no tiene recursos visibles, no renderiza nada.
 */
export default function StudentLessonResources({ courseId, lessonId }) {
  const [resources, setResources] = useState([]);
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    let alive = true;
    getStudentLessonResources(courseId, lessonId)
      .then((r) => { if (alive) setResources(r); })
      .catch(() => { if (alive) setResources([]); });
    return () => { alive = false; };
  }, [courseId, lessonId]);

  // Cerrar al hacer click fuera.
  useEffect(() => {
    if (!open) return undefined;
    const onDoc = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener('mousedown', onDoc);
    return () => document.removeEventListener('mousedown', onDoc);
  }, [open]);

  if (resources.length === 0) return null;

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen((o) => !o)}
        className={`px-5 py-2.5 rounded-2xl transition-all duration-300 font-black text-[10px] tracking-widest uppercase flex items-center gap-2 border ${open ? 'bg-kenth-brightred text-white border-kenth-brightred' : 'bg-kenth-surface/10 text-kenth-text border-kenth-border hover:border-kenth-brightred'}`}
      >
        📎 Recursos
        <span className="inline-flex items-center justify-center min-w-[18px] h-[18px] px-1 rounded-full bg-kenth-brightred text-white text-[10px]">
          {resources.length}
        </span>
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-[340px] max-h-[60vh] overflow-y-auto z-50 rounded-2xl border border-kenth-border shadow-[0_20px_60px_rgba(0,0,0,0.7)] p-3 flex flex-col gap-2" style={{ backgroundColor: 'var(--kenth-bg, #1A1A1D)' }}>
          <p className="text-[10px] font-black uppercase tracking-[0.2em] text-kenth-brightred mb-1">
            Recursos de esta lección
          </p>
          {resources.map((r) => {
            const meta = MEDIA_META[r.media_type] || MEDIA_META.file;
            const isImage = r.media_type === 'image';
            return (
              <a
                key={r.doc_id}
                href={r.download_url}
                target="_blank"
                rel="noopener noreferrer"
                download={!isImage ? (r.filename || true) : undefined}
                className="group flex gap-3 p-2.5 rounded-xl border border-kenth-border bg-kenth-surface/5 hover:border-kenth-brightred/50 transition"
              >
                {isImage ? (
                  <img src={r.download_url} alt={r.title} className="w-14 h-14 rounded-lg object-cover border border-kenth-border flex-shrink-0" loading="lazy" />
                ) : (
                  <div className="w-14 h-14 rounded-lg border border-kenth-border bg-kenth-surface/10 flex items-center justify-center text-2xl flex-shrink-0">
                    {meta.icon}
                  </div>
                )}
                <div className="min-w-0 flex flex-col">
                  <span className="text-[9px] uppercase font-black tracking-widest text-kenth-subtext">{meta.label}</span>
                  <p className="text-sm font-bold text-kenth-text truncate group-hover:text-kenth-brightred transition">{r.title}</p>
                  {r.description && <p className="text-[11px] text-kenth-subtext line-clamp-2 mt-0.5">{r.description}</p>}
                  <span className="text-[10px] font-black uppercase tracking-widest text-kenth-brightred mt-auto pt-1">
                    {isImage ? '🔍 Ver' : '⬇ Descargar'}
                  </span>
                </div>
              </a>
            );
          })}
        </div>
      )}
    </div>
  );
}
