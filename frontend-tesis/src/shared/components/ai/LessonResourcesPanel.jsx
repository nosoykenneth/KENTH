import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  listLessonResources,
  uploadLessonResource,
  deleteLessonResource,
  suggestResourceCaption,
  fetchMediaUrl,
} from '../../services/ragService';
import { showNotification } from '../../utils/notify';

const MEDIA_META = {
  image: { icon: '🖼️', label: 'Imagen' },
  audio: { icon: '🎵', label: 'Audio' },
  template: { icon: '🎛️', label: 'Plantilla DAW' },
  document: { icon: '📄', label: 'Documento' },
  file: { icon: '📎', label: 'Archivo' },
};

// Estado de indexación → color + etiqueta.
const STATUS_META = {
  indexed: { label: 'Indexado', cls: 'text-emerald-400 border-emerald-500/30' },
  pending: { label: 'Pendiente', cls: 'text-amber-400 border-amber-500/30' },
  failed: { label: 'Error', cls: 'text-red-400 border-red-500/30' },
  stale: { label: 'Reindexar', cls: 'text-orange-400 border-orange-500/30' },
};

// resource_type = uso pedagógico (distinto del formato técnico = media_type).
const RESOURCE_TYPES = [
  { value: '', label: 'Automático (según formato)' },
  { value: 'theory', label: 'Teoría' },
  { value: 'pdf_reading', label: 'Lectura PDF' },
  { value: 'audio_practice', label: 'Práctica de audio' },
  { value: 'daw_template', label: 'Plantilla DAW' },
  { value: 'image_reference', label: 'Imagen de referencia' },
  { value: 'exercise', label: 'Ejercicio' },
  { value: 'solution', label: 'Solución (oculto por defecto)' },
  { value: 'rubric', label: 'Rúbrica (oculto por defecto)' },
  { value: 'downloadable', label: 'Descargable' },
  { value: 'other', label: 'Otro' },
];

const IMAGE_RE = /\.(png|jpe?g|webp)$/i;

const EMPTY_FORM = {
  title: '',
  description: '',
  concepts: '',
  resource_type: '',
  index_to_tutor: true,
  visible_to_student: true,
};

// Etiqueta de estado de indexación reutilizable.
function StatusBadge({ status, error }) {
  const m = STATUS_META[status] || STATUS_META.pending;
  return (
    <span
      className={`text-[8px] uppercase font-black tracking-widest border rounded px-1 ${m.cls}`}
      title={status === 'failed' && error ? error : m.label}
    >
      {m.label}
    </span>
  );
}

// Miniatura/icono de un recurso (imagen vía blob autenticado; resto, icono grande).
function ResourceThumb({ courseId, resource }) {
  const [url, setUrl] = useState('');
  useEffect(() => {
    let alive = true;
    let made = '';
    if (resource.media_type === 'image') {
      fetchMediaUrl(courseId, resource.doc_id)
        .then((u) => { if (alive) { made = u; setUrl(u); } })
        .catch(() => {});
    }
    return () => { alive = false; if (made) URL.revokeObjectURL(made); };
  }, [courseId, resource.doc_id, resource.media_type]);

  if (resource.media_type === 'image' && url) {
    return <img src={url} alt={resource.title} className="w-14 h-14 rounded-lg object-cover border border-kenth-border" />;
  }
  const meta = MEDIA_META[resource.media_type] || MEDIA_META.file;
  return (
    <div className="w-14 h-14 rounded-lg border border-kenth-border bg-kenth-surface/5 flex items-center justify-center text-2xl flex-shrink-0">
      {meta.icon}
    </div>
  );
}

/**
 * LessonResourcesPanel
 * Recursos de UNA lección (imagen / plantilla / audio / pdf). Cada recurso declara
 * dos flags: Indexar al tutor (su descripción/contenido entra al RAG) y Visible al
 * alumno (panel + el tutor lo enlaza). Subida inmediata (no depende del Guardar global).
 */
export default function LessonResourcesPanel({ courseId, lessonId }) {
  const [resources, setResources] = useState([]);
  const [inherited, setInherited] = useState([]); // recursos del eje (solo lectura)
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [file, setFile] = useState(null);
  const [imgPreview, setImgPreview] = useState('');
  const [suggesting, setSuggesting] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const fileRef = useRef(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listLessonResources(courseId, lessonId, true);
      setResources(data.resources || []);
      setInherited(data.inherited_section_resources || []);
    } catch (e) {
      showNotification(e.message || 'No se pudieron cargar los recursos', 'error');
    } finally {
      setLoading(false);
    }
  }, [courseId, lessonId]);

  useEffect(() => { load(); }, [load]);

  const isImage = file && IMAGE_RE.test(file.name);

  const resetForm = () => {
    setAdding(false);
    setFile(null);
    setForm(EMPTY_FORM);
    if (imgPreview) { URL.revokeObjectURL(imgPreview); setImgPreview(''); }
    if (fileRef.current) fileRef.current.value = '';
  };

  const onFile = (e) => {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    if (imgPreview) { URL.revokeObjectURL(imgPreview); setImgPreview(''); }
    if (IMAGE_RE.test(f.name)) setImgPreview(URL.createObjectURL(f));
    if (!form.title) setForm((p) => ({ ...p, title: f.name.replace(/\.[^.]+$/, '') }));
  };

  const suggest = async () => {
    if (!file) return;
    setSuggesting(true);
    try {
      const desc = await suggestResourceCaption(courseId, file);
      setForm((p) => ({ ...p, description: desc }));
    } catch (e) {
      showNotification(e.message || 'No se pudo sugerir la descripción', 'error');
    } finally {
      setSuggesting(false);
    }
  };

  const submit = async () => {
    if (!file) { showNotification('Elige un archivo', 'error'); return; }
    const needsDesc = form.index_to_tutor && !isImage && !IMAGE_RE.test(file.name)
      && !/\.(pdf|txt|md)$/i.test(file.name);
    if ((isImage || needsDesc) && form.index_to_tutor && !form.description.trim()) {
      showNotification('Este recurso necesita una descripción para indexarlo al tutor', 'error');
      return;
    }
    setUploading(true);
    try {
      await uploadLessonResource(courseId, lessonId, { ...form, file });
      showNotification('Recurso agregado', 'success');
      resetForm();
      await load();
    } catch (e) {
      showNotification(e.message || 'No se pudo subir el recurso', 'error');
    } finally {
      setUploading(false);
    }
  };

  const remove = async (r) => {
    if (!window.confirm(`¿Eliminar "${r.title}"? Se quita del panel del alumno y del índice del tutor.`)) return;
    try {
      await deleteLessonResource(courseId, lessonId, r.doc_id);
      setResources((prev) => prev.filter((x) => x.doc_id !== r.doc_id));
    } catch (e) {
      showNotification(e.message || 'No se pudo eliminar', 'error');
    }
  };

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <p className="text-[11px] text-kenth-subtext leading-relaxed max-w-md">
          Material de esta lección: imágenes, plantillas (.flp/.als), audios, PDF.
          <strong className="text-kenth-text"> Indexar</strong> = el tutor lo conoce ·
          <strong className="text-kenth-text"> Visible</strong> = el alumno lo ve/descarga.
        </p>
        {!adding && (
          <button
            onClick={() => setAdding(true)}
            className="px-3 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest flex-shrink-0"
          >
            + Recurso
          </button>
        )}
      </div>

      {/* Formulario de subida */}
      {adding && (
        <div className="rounded-xl border border-kenth-border bg-kenth-surface/5 p-3 flex flex-col gap-3">
          <input
            ref={fileRef}
            type="file"
            onChange={onFile}
            accept=".png,.jpg,.jpeg,.webp,.wav,.mp3,.flac,.ogg,.aiff,.aif,.m4a,.flp,.als,.ptx,.logicx,.cpr,.rpp,.band,.aup3,.pdf,.txt,.md,.zip"
            className="text-xs text-kenth-subtext file:mr-3 file:px-3 file:py-1.5 file:rounded-lg file:border-0 file:bg-kenth-brightred file:text-white file:text-[10px] file:font-black file:uppercase file:tracking-widest"
          />

          {imgPreview && (
            <img src={imgPreview} alt="preview" className="max-h-40 rounded-lg border border-kenth-border object-contain self-start" />
          )}

          <input
            value={form.title}
            onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))}
            placeholder="Título del recurso"
            className="bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none"
          />

          <div className="flex flex-col gap-1.5">
            <div className="flex items-center justify-between">
              <label className="text-[10px] uppercase font-black tracking-widest text-kenth-subtext">
                Descripción {form.index_to_tutor && '(qué es y para qué sirve)'}
              </label>
              {isImage && (
                <button
                  onClick={suggest}
                  disabled={suggesting}
                  className="text-[10px] font-black uppercase tracking-widest text-indigo-300 hover:text-indigo-200 disabled:opacity-40"
                >
                  {suggesting ? 'Analizando…' : '✨ Sugerir con IA'}
                </button>
              )}
            </div>
            <textarea
              value={form.description}
              onChange={(e) => setForm((p) => ({ ...p, description: e.target.value }))}
              rows={3}
              placeholder="Ej: Plantilla de masterización con limitador en el master y cadena de EQ…"
              className="bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text leading-relaxed focus:border-kenth-brightred focus:outline-none resize-y"
            />
          </div>

          <input
            value={form.concepts}
            onChange={(e) => setForm((p) => ({ ...p, concepts: e.target.value }))}
            placeholder="Conceptos (separados por coma): limitador, headroom, true peak…"
            className="bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-xs text-kenth-text focus:border-kenth-brightred focus:outline-none"
          />

          <div className="flex flex-col gap-1.5">
            <label className="text-[10px] uppercase font-black tracking-widest text-kenth-subtext">
              Tipo de recurso (uso pedagógico)
            </label>
            <select
              value={form.resource_type}
              onChange={(e) => setForm((p) => ({ ...p, resource_type: e.target.value }))}
              className="bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-xs text-kenth-text focus:border-kenth-brightred focus:outline-none"
            >
              {RESOURCE_TYPES.map((rt) => <option key={rt.value} value={rt.value}>{rt.label}</option>)}
            </select>
          </div>

          <div className="flex flex-wrap gap-4">
            <label className="flex items-center gap-2 text-[11px] uppercase tracking-widest text-kenth-subtext cursor-pointer">
              <input type="checkbox" checked={form.index_to_tutor} onChange={(e) => setForm((p) => ({ ...p, index_to_tutor: e.target.checked }))} className="accent-kenth-brightred" />
              Indexar al tutor
            </label>
            <label className="flex items-center gap-2 text-[11px] uppercase tracking-widest text-kenth-subtext cursor-pointer">
              <input type="checkbox" checked={form.visible_to_student} onChange={(e) => setForm((p) => ({ ...p, visible_to_student: e.target.checked }))} className="accent-kenth-brightred" />
              Visible al alumno
            </label>
          </div>

          <div className="flex gap-2">
            <button
              onClick={submit}
              disabled={uploading || !file}
              className="px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40"
            >
              {uploading ? 'Subiendo…' : 'Subir e indexar'}
            </button>
            <button
              onClick={resetForm}
              disabled={uploading}
              className="px-4 py-2 rounded-xl bg-kenth-surface/10 border border-kenth-border text-kenth-text text-xs font-bold uppercase tracking-widest disabled:opacity-40"
            >
              Cancelar
            </button>
          </div>
        </div>
      )}

      {/* Lista */}
      {loading ? (
        <p className="text-sm text-kenth-subtext">Cargando…</p>
      ) : resources.length === 0 ? (
        <p className="text-xs text-kenth-subtext">Aún no hay recursos en esta lección.</p>
      ) : (
        <div className="flex flex-col gap-2">
          {resources.map((r) => {
            const meta = MEDIA_META[r.media_type] || MEDIA_META.file;
            return (
              <div key={r.doc_id} className="flex gap-3 p-2.5 rounded-xl border border-kenth-border bg-kenth-surface/5">
                <ResourceThumb courseId={courseId} resource={r} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <span className="text-[9px] uppercase font-black tracking-widest text-kenth-subtext">{meta.label}</span>
                    <span className="text-[8px] uppercase font-black tracking-widest text-violet-300 border border-violet-500/30 rounded px-1">Lección</span>
                    {r.resource_type && <span className="text-[8px] uppercase font-black tracking-widest text-kenth-subtext border border-kenth-border rounded px-1">{r.resource_type}</span>}
                    {r.indexed && <StatusBadge status={r.index_status} error={r.index_error} />}
                    {r.visible_to_student
                      ? <span className="text-[8px] uppercase font-black tracking-widest text-sky-400 border border-sky-500/30 rounded px-1">Visible</span>
                      : <span className="text-[8px] uppercase font-black tracking-widest text-kenth-subtext border border-kenth-border rounded px-1">Oculto</span>}
                    {typeof r.chunk_count === 'number' && r.chunk_count > 0 && (
                      <span className="text-[8px] text-kenth-subtext">{r.chunk_count} chunks</span>
                    )}
                  </div>
                  <p className="text-sm font-bold text-kenth-text truncate">{r.title}</p>
                  {r.description && <p className="text-[11px] text-kenth-subtext line-clamp-2">{r.description}</p>}
                  {r.index_status === 'failed' && r.index_error && (
                    <p className="text-[10px] text-red-400 mt-0.5">⚠ {r.index_error}</p>
                  )}
                </div>
                <button
                  onClick={() => remove(r)}
                  className="text-red-400 hover:text-red-300 text-xs flex-shrink-0 self-start"
                  title="Eliminar recurso"
                >
                  🗑
                </button>
              </div>
            );
          })}
        </div>
      )}

      {/* Recursos HEREDADOS del eje (solo lectura): aplican a todas las lecciones del eje. */}
      {inherited.length > 0 && (
        <div className="mt-2 border-t border-kenth-border pt-3">
          <p className="text-[10px] uppercase font-black tracking-widest text-kenth-subtext mb-1">
            🧩 Heredados del eje (no editables aquí)
          </p>
          <p className="text-[10px] text-kenth-subtext mb-2">
            Pertenecen a todo el eje. Para gestionarlos, ve a <strong className="text-kenth-text">Conocimiento → Recursos del eje</strong>.
          </p>
          <div className="flex flex-col gap-2 opacity-90">
            {inherited.map((r) => {
              const meta = MEDIA_META[r.media_type] || MEDIA_META.file;
              return (
                <div key={r.doc_id} className="flex gap-3 p-2.5 rounded-xl border border-dashed border-kenth-border bg-kenth-surface/[0.03]">
                  <div className="w-10 h-10 rounded-lg border border-kenth-border bg-kenth-surface/5 flex items-center justify-center text-xl flex-shrink-0">{meta.icon}</div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5 flex-wrap">
                      <span className="text-[8px] uppercase font-black tracking-widest text-amber-300 border border-amber-500/30 rounded px-1">Eje</span>
                      {r.resource_type && <span className="text-[8px] uppercase font-black tracking-widest text-kenth-subtext border border-kenth-border rounded px-1">{r.resource_type}</span>}
                      {r.indexed && <StatusBadge status={r.index_status} error={r.index_error} />}
                    </div>
                    <p className="text-sm font-bold text-kenth-text truncate">{r.title}</p>
                    {r.description && <p className="text-[11px] text-kenth-subtext line-clamp-1">{r.description}</p>}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
