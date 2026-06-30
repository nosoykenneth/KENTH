import React, { useCallback, useEffect, useState } from 'react';
import {
  getKnowledgeSummary,
  getCourseDocuments,
  getStructuredDocuments,
  uploadCourseDocument,
  uploadSectionResource,
  deleteSectionResource,
  deleteCourseDocument,
  reindexCourseDocuments,
  suggestImageCaption,
  fetchMediaUrl,
  getKnowledgeItem,
  deleteKnowledgeItem,
  fetchKnowledgeFile,
} from '../../shared/services/ragService';
import { showNotification } from '../../shared/utils/notify';

const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none';
const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';
const EMPTY_COUNTS = { teoria: 0, transcripcion: 0, docs: 0, total: 0 };

const KIND_META = {
  teoria: { icon: '📖', label: 'Teoría base' },
  transcripcion: { icon: '🎬', label: 'Transcripción' },
  doc: { icon: '📄', label: 'Doc subido' },
  imagen: { icon: '🖼️', label: 'Imagen' },
};

const STATUS_META = {
  indexed: { label: 'Indexado', cls: 'text-emerald-400 border-emerald-500/30' },
  pending: { label: 'Pendiente', cls: 'text-amber-400 border-amber-500/30' },
  failed: { label: 'Error', cls: 'text-red-400 border-red-500/30' },
  stale: { label: 'Reindexar', cls: 'text-orange-400 border-orange-500/30' },
};

const RESOURCE_TYPES = [
  { value: '', label: 'Automático (según formato)' },
  { value: 'theory', label: 'Teoría' },
  { value: 'pdf_reading', label: 'Lectura PDF' },
  { value: 'audio_practice', label: 'Práctica de audio' },
  { value: 'daw_template', label: 'Plantilla DAW' },
  { value: 'image_reference', label: 'Imagen de referencia' },
  { value: 'exercise', label: 'Ejercicio' },
  { value: 'solution', label: 'Solución (oculto)' },
  { value: 'rubric', label: 'Rúbrica (oculto)' },
  { value: 'downloadable', label: 'Descargable' },
  { value: 'other', label: 'Otro' },
];

// Fila de recurso (BD autoritativa) con badges de scope/tipo/estado/visibilidad.
function ResourceRow({ r, scopeLabel, onDelete }) {
  const st = STATUS_META[r.index_status] || STATUS_META.pending;
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/5">
      <span className="flex-1 min-w-0">
        <span className="text-xs text-kenth-text truncate">{r.title || r.filename || r.doc_id}</span>
        <span className="flex items-center gap-1.5 flex-wrap mt-0.5">
          {scopeLabel && <span className="text-[8px] uppercase font-black tracking-widest text-amber-300 border border-amber-500/30 rounded px-1">{scopeLabel}</span>}
          <span className="text-[8px] uppercase font-black tracking-widest text-kenth-subtext border border-kenth-border rounded px-1">{r.media_type || 'doc'}</span>
          {r.resource_type && <span className="text-[8px] uppercase font-black tracking-widest text-kenth-subtext border border-kenth-border rounded px-1">{r.resource_type}</span>}
          <span className={`text-[8px] uppercase font-black tracking-widest border rounded px-1 ${st.cls}`} title={r.index_status === 'failed' ? (r.index_error || st.label) : st.label}>{st.label}</span>
          {r.visible_to_student
            ? <span className="text-[8px] uppercase font-black tracking-widest text-sky-400 border border-sky-500/30 rounded px-1">Visible</span>
            : <span className="text-[8px] uppercase font-black tracking-widest text-kenth-subtext border border-kenth-border rounded px-1">Oculto</span>}
          {typeof r.chunk_count === 'number' && <span className="text-[8px] text-kenth-subtext">{r.chunk_count} chunks</span>}
        </span>
        {r.index_status === 'failed' && r.index_error && <span className="block text-[10px] text-red-400 mt-0.5">⚠ {r.index_error}</span>}
      </span>
      {onDelete && (
        <button onClick={() => onDelete(r)} className="text-red-400 hover:text-red-300 text-xs flex-shrink-0" title="Borrar recurso">🗑</button>
      )}
    </div>
  );
}

function CountLine({ c = EMPTY_COUNTS }) {
  return (
    <span className="text-[11px] text-kenth-subtext">
      teoría <span className="text-kenth-text font-bold">{c.teoria || 0}</span>
      {' · '}transcripción <span className="text-kenth-text font-bold">{c.transcripcion || 0}</span>
      {' · '}docs <span className="text-kenth-text font-bold">{c.docs || 0}</span>
    </span>
  );
}

function ImageThumb({ courseId, docId, scope }) {
  const [url, setUrl] = useState('');
  useEffect(() => {
    let alive = true; let obj = '';
    fetchMediaUrl(courseId, docId, scope).then((u) => { if (alive) { obj = u; setUrl(u); } }).catch(() => {});
    return () => { alive = false; if (obj) URL.revokeObjectURL(obj); };
  }, [courseId, docId, scope]);
  return url
    ? <img src={url} alt="" className="w-9 h-9 rounded object-cover border border-kenth-border flex-shrink-0" />
    : <span className="w-9 h-9 rounded bg-kenth-surface/20 flex items-center justify-center text-sm flex-shrink-0">🖼️</span>;
}

function ItemRow({ it, courseId, scope, onDelete, onView }) {
  const k = KIND_META[it.kind] || KIND_META.doc;
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-kenth-border bg-kenth-surface/5">
      {it.kind === 'imagen'
        ? <ImageThumb courseId={courseId} docId={it.doc_id} scope={scope} />
        : <span title={k.label}>{k.icon}</span>}
      <span className="flex-1 min-w-0 text-xs text-kenth-text truncate">
        {it.label}
        <span className="text-[10px] text-kenth-subtext ml-2 uppercase tracking-widest">{k.label}</span>
      </span>
      <span className="text-[10px] text-kenth-subtext whitespace-nowrap">{it.chunks} chunks</span>
      {onView && (
        <button onClick={() => onView(it)} className="text-kenth-subtext hover:text-kenth-text text-xs" title="Ver contenido indexado">👁</button>
      )}
      {onDelete && (
        <button onClick={() => onDelete(it)} className="text-red-400 hover:text-red-300 text-xs" title="Borrar del índice">🗑</button>
      )}
    </div>
  );
}

/**
 * KnowledgeHub — pestaña "Conocimiento" de Gestión del Tutor (rol PROFE).
 * AUDITORÍA: muestra TODO lo que el tutor tiene indexado, por eje
 * (teoría/transcripción/docs/imágenes), con borrar y reindexar.
 * El material de cada lección se sube desde la pestaña RECURSOS de la lección;
 * aquí SOLO se sube conocimiento GLOBAL (compartido por todos los cursos).
 */
export default function KnowledgeHub({ courseId, sections = [] }) {
  const [summary, setSummary] = useState({ total: 0, global: EMPTY_COUNTS, by_section: {} });
  const [globalDocs, setGlobalDocs] = useState([]);
  const [structured, setStructured] = useState({ course: [], sections: {}, global_docs: [] });
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [openKey, setOpenKey] = useState(null);

  // subida. uploadTarget: { scope:'global'|'course'|'section', moodle_section_id? }
  const [uploadTarget, setUploadTarget] = useState(null);
  const [docType, setDocType] = useState('documento'); // 'documento' | 'imagen' | 'binario' (solo eje)
  const [file, setFile] = useState(null);
  const [imgPreview, setImgPreview] = useState('');
  const [suggesting, setSuggesting] = useState(false);
  const EMPTY_FORM = {
    title: '', description: '', concepts: '', doc_layer: 'canonico',
    attribution_required: false, resource_type: '', index_to_tutor: true, visible_to_student: true,
  };
  const [form, setForm] = useState(EMPTY_FORM);

  const load = useCallback(async () => {
    if (!courseId) return;
    try {
      setLoading(true);
      const [sum, gdocs, struct] = await Promise.all([
        getKnowledgeSummary(courseId),
        getCourseDocuments(courseId, 'global'),
        getStructuredDocuments(courseId),
      ]);
      setSummary(sum || { total: 0, global: EMPTY_COUNTS, by_section: {} });
      setGlobalDocs(gdocs || []);
      setStructured(struct || { course: [], sections: {}, global_docs: [] });
    } catch (e) { showNotification('error', e.message); }
    finally { setLoading(false); }
  }, [courseId]);

  useEffect(() => { load(); }, [load]);

  const setField = (k, v) => setForm((p) => ({ ...p, [k]: v }));

  const startUpload = (target) => {
    setUploadTarget(target);
    setDocType('documento');
    setFile(null);
    setImgPreview('');
    setForm(EMPTY_FORM);
  };
  const cancelUpload = () => { setUploadTarget(null); setFile(null); setImgPreview(''); };

  const onFile = (f) => {
    setFile(f || null);
    if (imgPreview) { URL.revokeObjectURL(imgPreview); setImgPreview(''); }
    if (f && docType === 'imagen') setImgPreview(URL.createObjectURL(f));
  };

  const suggest = async () => {
    if (!file) { showNotification('error', 'Selecciona la imagen primero.'); return; }
    setSuggesting(true);
    try {
      const desc = await suggestImageCaption(courseId, file);
      setField('description', desc);
    } catch (e) { showNotification('error', e.message); }
    finally { setSuggesting(false); }
  };

  const submitUpload = async (e) => {
    e.preventDefault();
    if (!file) { showNotification('error', 'Selecciona un archivo.'); return; }
    if (docType === 'imagen' && !form.description.trim()) {
      showNotification('error', 'Describe qué muestra la imagen (o usa "Sugerir con IA").'); return;
    }
    setBusy(true);
    try {
      let res;
      if (uploadTarget?.scope === 'section') {
        // Recurso formal de EJE (soporta todos los formatos, incl. audio/plantilla).
        res = await uploadSectionResource(courseId, uploadTarget.moodle_section_id, {
          file,
          title: form.title,
          description: form.description,
          concepts: form.concepts,
          resource_type: form.resource_type,
          index_to_tutor: form.index_to_tutor,
          visible_to_student: form.visible_to_student,
        });
      } else {
        // Curso completo o GLOBAL (documento/imagen vía conocimiento del curso).
        res = await uploadCourseDocument(courseId, {
          ...form, file,
          moodle_section_id: uploadTarget?.moodle_section_id || '',
          scope: uploadTarget?.scope === 'global' ? 'global' : '',
        });
      }
      showNotification('success', `Indexado (${res.chunks || 0} chunks).`);
      cancelUpload();
      await load();
    } catch (e2) { showNotification('error', e2.message); }
    finally { setBusy(false); }
  };

  const removeSectionResource = async (sectionId, r) => {
    if (!window.confirm(`¿Eliminar el recurso de la sección "${r.title}"?`)) return;
    setBusy(true);
    try {
      await deleteSectionResource(courseId, sectionId, r.doc_id);
      showNotification('success', 'Recurso de sección eliminado.');
      await load();
    } catch (e) { showNotification('error', e.message); }
    finally { setBusy(false); }
  };

  const remove = async (docId, isGlobal) => {
    if (!window.confirm(`¿Eliminar ${docId} del conocimiento${isGlobal ? ' GLOBAL' : ''}?`)) return;
    setBusy(true);
    try {
      await deleteCourseDocument(courseId, docId, isGlobal ? 'global' : '');
      showNotification('success', 'Eliminado.');
      await load();
    } catch (e) { showNotification('error', e.message); }
    finally { setBusy(false); }
  };

  // Visor de contenido indexado (modal): nombre + descripción + visor según tipo.
  const [viewer, setViewer] = useState(null); // { label, description, text, view_type, fileUrl, chunks, loading }
  const viewItem = async (it, scope = '') => {
    if (!it.source) { showNotification('error', 'Esta fuente no tiene contenido visible.'); return; }
    setViewer({ label: it.label, description: '', text: '', view_type: 'text', fileUrl: '', chunks: it.chunks, loading: true });
    try {
      const res = await getKnowledgeItem(courseId, it.source, scope);
      let fileUrl = '';
      if (res.has_file && ['pdf', 'image', 'audio', 'file'].includes(res.view_type)) {
        try { fileUrl = await fetchKnowledgeFile(courseId, it.source, scope); } catch { /* cae a texto */ }
      }
      setViewer({
        label: res.label || it.label,
        description: res.description || '',
        text: res.text || '',
        view_type: res.view_type || 'text',
        fileUrl,
        chunks: res.chunks,
        loading: false,
      });
    } catch (e) { showNotification('error', e.message); setViewer(null); }
  };
  const closeViewer = () => {
    if (viewer?.fileUrl) URL.revokeObjectURL(viewer.fileUrl);
    setViewer(null);
  };

  // Borrar cualquier ítem indexado por source (teoría/transcripción/doc).
  const removeItem = async (it, scope = '') => {
    const aviso = it.kind === 'teoria'
      ? `¿Borrar "${it.label}" del índice? El archivo se moverá a no_indexar (reversible) y el tutor dejará de saberlo.`
      : `¿Borrar "${it.label}" del índice del tutor?`;
    if (!window.confirm(aviso)) return;
    setBusy(true);
    try {
      if (it.source) await deleteKnowledgeItem(courseId, it.source, scope);
      else if (it.doc_id) await deleteCourseDocument(courseId, it.doc_id, scope);
      showNotification('success', 'Borrado del índice.');
      await load();
    } catch (e) { showNotification('error', e.message); }
    finally { setBusy(false); }
  };

  const reindex = async () => {
    setBusy(true);
    try {
      const res = await reindexCourseDocuments(courseId);
      showNotification('success', `Reindex del curso: ${res.processed || 0} docs.`);
      await load();
    } catch (e) { showNotification('error', e.message); }
    finally { setBusy(false); }
  };

  // Form de subida (función, NO componente, para no remontar al teclear).
  const renderUploadForm = () => {
    const sc = uploadTarget?.scope;
    const isSection = sc === 'section';
    const headerTxt = sc === 'global'
      ? 'Subir a GLOBAL (todos los cursos)'
      : isSection ? `Recurso de la sección ${uploadTarget?.moodle_section_id}` : 'Recurso del curso completo';
    // El eje admite todos los formatos; curso/global, solo documento/imagen.
    const allAccept = '.png,.jpg,.jpeg,.webp,.wav,.mp3,.flac,.ogg,.aiff,.aif,.m4a,.flp,.als,.ptx,.logicx,.cpr,.rpp,.band,.aup3,.pdf,.txt,.md,.zip';
    const acceptStr = isSection
      ? allAccept
      : (docType === 'imagen' ? 'image/png,image/jpeg,image/webp' : '.pdf,.txt,.md');
    return (
    <form onSubmit={submitUpload} className="mt-2 border border-kenth-border rounded-xl p-3 bg-kenth-surface/5 flex flex-col gap-2">
      <div className="flex items-center justify-between">
        <span className="text-[10px] font-black uppercase tracking-widest text-kenth-brightred">{headerTxt}</span>
        <button type="button" onClick={cancelUpload} className="text-kenth-subtext hover:text-kenth-text text-xs">✕</button>
      </div>

      {sc === 'global' && (
        <p className="text-[10px] text-amber-300/90 border border-amber-500/30 bg-amber-500/5 rounded-lg px-2 py-1.5">
          ⚠ GLOBAL se comparte con TODOS los cursos. Úsalo solo para conocimiento universal.
        </p>
      )}

      {/* Tipo (curso/global): documento o imagen. El eje acepta todo formato directamente. */}
      {!isSection && (
        <div className="inline-flex rounded-lg border border-kenth-border overflow-hidden w-fit">
          {['documento', 'imagen'].map((t) => (
            <button key={t} type="button" onClick={() => { setDocType(t); onFile(null); }}
              className={`px-3 py-1.5 text-[10px] font-black uppercase tracking-widest ${docType === t ? 'bg-kenth-brightred text-white' : 'text-kenth-subtext hover:text-kenth-text'}`}>
              {t === 'documento' ? '📄 Documento' : '🖼️ Imagen'}
            </button>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        <div>
          <label className={labelCls}>{isSection ? 'Archivo (pdf/img/audio/plantilla)' : (docType === 'imagen' ? 'Imagen (png/jpg/webp)' : 'Archivo (pdf/txt/md)')}</label>
          <input type="file" accept={acceptStr}
            className={inputCls} onChange={(e) => onFile(e.target.files?.[0] || null)} disabled={busy} />
        </div>
        <div>
          <label className={labelCls}>Título</label>
          <input className={inputCls} value={form.title} onChange={(e) => setField('title', e.target.value)} placeholder={file?.name || 'Nombre visible'} />
        </div>
      </div>

      {docType === 'imagen' && imgPreview && (
        <img src={imgPreview} alt="preview" className="max-h-40 rounded-lg border border-kenth-border self-start" />
      )}

      <div>
        <div className="flex items-center justify-between">
          <label className={labelCls}>{docType === 'imagen' ? 'Descripción (qué muestra) *' : 'Descripción / contexto'}</label>
          {docType === 'imagen' && (
            <button type="button" onClick={suggest} disabled={suggesting || !file} className="text-[10px] font-black uppercase text-indigo-400 hover:underline disabled:opacity-40">
              {suggesting ? 'Analizando…' : '✨ Sugerir con IA'}
            </button>
          )}
        </div>
        <textarea rows={docType === 'imagen' ? 4 : 2} className={inputCls} value={form.description}
          onChange={(e) => setField('description', e.target.value)}
          placeholder={isSection ? 'Qué es y para qué sirve (obligatorio para audio/plantilla si se indexa)' : (docType === 'imagen' ? 'Ej: captura del compresor X…' : 'Contexto extra para el tutor (opcional)')} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        <div>
          <label className={labelCls}>Conceptos (coma)</label>
          <input className={inputCls} value={form.concepts} onChange={(e) => setField('concepts', e.target.value)} placeholder="compresor, threshold, ratio" />
        </div>
        <div>
          <label className={labelCls}>Tipo de recurso (uso pedagógico)</label>
          <select className={inputCls} value={form.resource_type} onChange={(e) => setField('resource_type', e.target.value)}>
            {RESOURCE_TYPES.map((rt) => <option key={rt.value} value={rt.value}>{rt.label}</option>)}
          </select>
        </div>
      </div>

      {isSection ? (
        <div className="flex flex-wrap gap-4">
          <label className="flex items-center gap-2 text-[11px] uppercase tracking-widest text-kenth-subtext cursor-pointer">
            <input type="checkbox" checked={form.index_to_tutor} onChange={(e) => setField('index_to_tutor', e.target.checked)} className="accent-kenth-brightred" />
            Indexar al tutor
          </label>
          <label className="flex items-center gap-2 text-[11px] uppercase tracking-widest text-kenth-subtext cursor-pointer">
            <input type="checkbox" checked={form.visible_to_student} onChange={(e) => setField('visible_to_student', e.target.checked)} className="accent-kenth-brightred" />
            Visible al alumno
          </label>
        </div>
      ) : (
        <label className="flex items-center gap-2 text-xs text-kenth-subtext">
          <input type="checkbox" checked={form.attribution_required} onChange={(e) => setField('attribution_required', e.target.checked)} />
          Requiere atribución
        </label>
      )}

      <div className="flex justify-end">
        <button type="submit" disabled={busy} className="px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40">
          {busy ? 'Subiendo…' : 'Subir e indexar'}
        </button>
      </div>
    </form>
    );
  };

  if (loading) return <p className="text-sm text-kenth-subtext">Cargando conocimiento…</p>;

  const curso = summary.by_section?.['(sin seccion)'];
  const cursoItems = curso?.items || [];
  const totalCounts = Object.values(summary.by_section || {}).reduce(
    (a, b) => ({ teoria: a.teoria + (b.teoria || 0), transcripcion: a.transcripcion + (b.transcripcion || 0), docs: a.docs + (b.docs || 0) }),
    { teoria: 0, transcripcion: 0, docs: 0 });

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <p className="text-xs text-kenth-subtext">
          Indexado del curso: <span className="text-kenth-text font-bold">{summary.total || 0}</span> trozos · <CountLine c={totalCounts} />
        </p>
        <button onClick={reindex} disabled={busy} className="px-3 py-2 rounded-xl border border-kenth-border bg-kenth-surface/10 text-kenth-text text-[10px] font-black uppercase tracking-widest hover:border-kenth-brightred disabled:opacity-40">
          Reindexar curso
        </button>
      </div>

      {/* ESTE CURSO (por eje) — solo lectura/auditoría */}
      <div>
        <p className={`${labelCls} mb-1`}>Este curso — por sección (qué sabe el tutor)</p>
        <p className="text-[11px] text-kenth-subtext mb-2">
          Solo lectura. Para añadir material a una sección, súbelo en la pestaña <strong className="text-kenth-text">Recursos</strong> de la lección correspondiente.
        </p>
        <div className="flex flex-col gap-1.5">
          {sections.map((ax, idx) => {
            // Numero pedagogico por POSICION: la primera seccion es Bienvenida
            // (no pedagogica); las demas se numeran 0,1,2… El contenido viaja
            // solo porque va atado al moodle_section_id estable, no a este numero.
            const isWelcome = idx === 0;
            const sectionNumber = idx - 1;
            const counts = summary.by_section?.[ax.moodle_section_id] || EMPTY_COUNTS;
            const open = openKey === ax.moodle_section_id;
            const items = summary.by_section?.[ax.moodle_section_id]?.items || [];
            const sx = structured.sections?.[ax.moodle_section_id] || { section_resources: [], lessons: {} };
            const sectionResources = sx.section_resources || [];
            const lessonsMap = sx.lessons || {};
            const lessonKeys = Object.keys(lessonsMap);
            const lessonCount = lessonKeys.reduce((a, k) => a + lessonsMap[k].length, 0);
            return (
              <div key={ax.moodle_section_id} className="border border-kenth-border rounded-xl bg-kenth-card">
                <div className="flex items-center gap-2 px-3 py-2">
                  <button onClick={() => setOpenKey(open ? null : ax.moodle_section_id)} className="flex-1 text-left min-w-0">
                    <span className="text-sm font-bold text-kenth-text">{open ? '▾' : '▸'} {ax.section_name || ax.moodle_section_id}</span>
                    <span className="text-kenth-subtext text-xs"> · {isWelcome ? 'bienvenida' : `sección ${sectionNumber}`}</span>
                    <div className="mt-0.5">
                      <CountLine c={counts} />
                      <span className="text-[10px] text-kenth-subtext ml-2">· sección {sectionResources.length} · lecciones {lessonCount}</span>
                    </div>
                  </button>
                </div>
                {open && (
                  <div className="px-3 pb-3 flex flex-col gap-3">
                    {/* A) Recursos propios de la SECCION (scope='section') */}
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <p className={labelCls}>🧩 Recursos de la sección</p>
                        <button onClick={() => startUpload({ scope: 'section', moodle_section_id: ax.moodle_section_id })}
                          className="text-[10px] font-black uppercase text-kenth-brightred hover:underline">+ Recurso de sección</button>
                      </div>
                      {sectionResources.length === 0
                        ? <p className="text-[11px] text-kenth-subtext">Sin recursos propios de la sección. Aplican a todas sus lecciones.</p>
                        : <div className="flex flex-col gap-1.5">{sectionResources.map((r) => (
                            <ResourceRow key={r.doc_id} r={r} onDelete={(rr) => removeSectionResource(ax.moodle_section_id, rr)} />
                          ))}</div>}
                      {uploadTarget?.scope === 'section' && uploadTarget?.moodle_section_id === ax.moodle_section_id && renderUploadForm()}
                    </div>

                    {/* B) Recursos por LECCIÓN (scope='lesson') — agrupados, NO como propios del eje */}
                    <div>
                      <p className={`${labelCls} mb-1`}>📚 Recursos por lección</p>
                      {lessonKeys.length === 0
                        ? <p className="text-[11px] text-kenth-subtext">Ninguna lección de esta sección tiene recursos todavía.</p>
                        : <div className="flex flex-col gap-2">{lessonKeys.sort().map((lid) => (
                            <div key={lid}>
                              <p className="text-[11px] font-bold text-kenth-text mb-0.5">{lid} <span className="text-kenth-subtext font-normal">({lessonsMap[lid].length})</span></p>
                              <div className="flex flex-col gap-1.5 pl-2 border-l border-kenth-border">
                                {lessonsMap[lid].map((r) => <ResourceRow key={r.doc_id} r={r} scopeLabel="Lección" />)}
                              </div>
                            </div>
                          ))}</div>}
                      <p className="text-[10px] text-kenth-subtext mt-1">Los recursos de lección se gestionan desde la pestaña <strong>Recursos</strong> de cada lección.</p>
                    </div>

                    {/* C) Auditoría de lo indexado en Chroma (teoría/transcripción/docs) */}
                    {items.length > 0 && (
                      <div>
                        <p className={`${labelCls} mb-1`}>🔎 Indexado (auditoría)</p>
                        <div className="flex flex-col gap-1.5">
                          {items.map((it, i) => <ItemRow key={i} it={it} courseId={courseId} onView={viewItem} onDelete={removeItem} />)}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}

          {/* Curso completo (sin eje) */}
          <div className="border border-kenth-border rounded-xl bg-kenth-card">
            <div className="flex items-center gap-2 px-3 py-2">
              <button onClick={() => setOpenKey(openKey === '__curso__' ? null : '__curso__')} className="flex-1 text-left">
                <span className="text-sm font-bold text-kenth-text">{openKey === '__curso__' ? '▾' : '▸'} 📁 Curso completo (sin sección)</span>
                <div className="mt-0.5"><CountLine c={curso || EMPTY_COUNTS} /></div>
              </button>
            </div>
            {openKey === '__curso__' && (
              <div className="px-3 pb-3 flex flex-col gap-3">
                {/* Recursos del CURSO (scope='course') */}
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <p className={labelCls}>📁 Recursos del curso</p>
                    <button onClick={() => startUpload({ scope: 'course' })}
                      className="text-[10px] font-black uppercase text-kenth-brightred hover:underline">+ Recurso del curso</button>
                  </div>
                  {(structured.course || []).length === 0
                    ? <p className="text-[11px] text-kenth-subtext">Sin recursos a nivel de curso (sin sección).</p>
                    : <div className="flex flex-col gap-1.5">{structured.course.map((r) => (
                        <ResourceRow key={r.doc_id} r={r} onDelete={(rr) => remove(rr.doc_id, false)} />
                      ))}</div>}
                  {uploadTarget?.scope === 'course' && renderUploadForm()}
                </div>

                {/* Auditoría Chroma sin eje */}
                {cursoItems.length > 0 && (
                  <div>
                    <p className={`${labelCls} mb-1`}>🔎 Indexado (auditoría)</p>
                    <div className="flex flex-col gap-1.5">
                      {cursoItems.map((it, i) => <ItemRow key={i} it={it} courseId={courseId} onView={viewItem} onDelete={removeItem} />)}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* GLOBAL */}
      <div>
        <p className={`${labelCls} mb-2`}>🌐 Global — compartido por TODOS los cursos</p>
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/5 p-3">
          <p className="text-[11px] text-amber-300/90 mb-2">
            Lo que subas aquí lo ven <strong>todos los cursos</strong>. Solo conocimiento universal, y
            <strong> coordínate con los otros profes</strong>.
          </p>
          <div className="flex items-center justify-between mb-2">
            <CountLine c={summary.global || EMPTY_COUNTS} />
            <button onClick={() => startUpload({ scope: 'global' })} className="text-[10px] font-black uppercase text-amber-400 hover:underline">+ Subir a global</button>
          </div>
          <div className="flex flex-col gap-1.5">
            {globalDocs.length === 0
              ? <p className="text-[11px] text-kenth-subtext">Aún no hay conocimiento global.</p>
              : globalDocs.map((d) => (
                <ResourceRow key={d.doc_id} r={d} scopeLabel="Global" onDelete={(rr) => remove(rr.doc_id, true)} />
              ))}
            {uploadTarget?.scope === 'global' && renderUploadForm()}
          </div>
        </div>
      </div>

      {/* Visor de contenido indexado */}
      {viewer && (
        <div className="fixed inset-0 z-[120] bg-black/70 backdrop-blur-sm flex items-center justify-center p-4" onClick={closeViewer}>
          <div className="w-full max-w-3xl max-h-[85vh] border border-kenth-border rounded-2xl shadow-2xl flex flex-col" style={{ backgroundColor: 'var(--kenth-bg, #1A1A1D)' }} onClick={(e) => e.stopPropagation()}>
            {/* Nombre */}
            <div className="flex items-start justify-between px-4 py-3 border-b border-kenth-border">
              <div className="min-w-0">
                <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">Recurso indexado</p>
                <p className="text-base font-black text-kenth-text truncate">{viewer.label}</p>
                <p className="text-[10px] text-kenth-subtext uppercase tracking-widest">{viewer.chunks} chunks · {viewer.view_type}</p>
              </div>
              <button onClick={closeViewer} className="text-kenth-subtext hover:text-kenth-text text-lg flex-shrink-0">✕</button>
            </div>

            {viewer.loading ? (
              <div className="p-6"><p className="text-sm text-kenth-subtext">Cargando…</p></div>
            ) : (
              <div className="overflow-y-auto p-4 flex flex-col gap-4">
                {/* Descripción */}
                {viewer.description && (
                  <div>
                    <p className={`${labelCls} mb-1`}>Descripción</p>
                    <p className="text-sm text-kenth-text leading-relaxed bg-kenth-surface/5 border border-kenth-border rounded-lg p-3">{viewer.description}</p>
                  </div>
                )}

                {/* Contenido según el tipo */}
                <div>
                  <p className={`${labelCls} mb-1`}>Contenido</p>
                  {viewer.view_type === 'image' && viewer.fileUrl && (
                    <img src={viewer.fileUrl} alt={viewer.label} className="max-h-[55vh] rounded-lg border border-kenth-border object-contain" />
                  )}
                  {viewer.view_type === 'pdf' && viewer.fileUrl && (
                    <iframe src={viewer.fileUrl} title={viewer.label} className="w-full h-[60vh] rounded-lg border border-kenth-border bg-white" />
                  )}
                  {viewer.view_type === 'audio' && viewer.fileUrl && (
                    <audio src={viewer.fileUrl} controls className="w-full" />
                  )}
                  {viewer.view_type === 'file' && (
                    <div className="flex items-center gap-3 bg-kenth-surface/5 border border-kenth-border rounded-lg p-3">
                      <span className="text-2xl">🎛️</span>
                      <span className="text-sm text-kenth-text">Archivo no previsualizable.</span>
                      {viewer.fileUrl && <a href={viewer.fileUrl} download className="ml-auto text-[10px] font-black uppercase tracking-widest text-kenth-brightred hover:underline">⬇ Descargar</a>}
                    </div>
                  )}

                  {/* Texto indexado (siempre, debajo del visor): es lo que el tutor "lee") */}
                  <div className={viewer.view_type === 'text' ? '' : 'mt-3'}>
                    {viewer.view_type !== 'text' && <p className="text-[10px] text-kenth-subtext uppercase tracking-widest mb-1">Texto que el tutor indexó</p>}
                    <pre className="text-xs text-kenth-text whitespace-pre-wrap leading-relaxed font-sans bg-kenth-surface/5 border border-kenth-border rounded-lg p-3 max-h-[45vh] overflow-y-auto">{viewer.text || '(sin texto)'}</pre>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
