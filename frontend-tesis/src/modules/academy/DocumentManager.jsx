import React, { useEffect, useState, useCallback } from 'react';
import {
  getCourseDocuments,
  uploadCourseDocument,
  deleteCourseDocument,
  reindexCourseDocuments,
} from '../../shared/services/ragService';
import { showNotification } from '../../shared/components/ui/Notification';

const inputCls = 'w-full bg-kenth-surface/10 border border-kenth-border rounded-lg px-3 py-2 text-sm text-kenth-text focus:border-kenth-brightred focus:outline-none';
const labelCls = 'text-[10px] uppercase tracking-widest text-kenth-subtext font-bold';

function statusClass(status) {
  if (status === 'active') return 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30';
  if (status === 'pending_review') return 'bg-amber-500/10 text-amber-300 border-amber-500/30';
  return 'bg-kenth-surface/20 text-kenth-subtext border-kenth-border';
}

export default function DocumentManager({ courseId, axes = [] }) {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [file, setFile] = useState(null);
  const [form, setForm] = useState({
    title: '',
    axis_id: '',
    doc_layer: 'canonico',
    attribution_required: false,
    ownership: 'kenth_academy',
    notes: '',
  });

  const loadDocs = useCallback(async () => {
    if (!courseId) return;
    try {
      setLoading(true);
      setDocs(await getCourseDocuments(courseId));
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setLoading(false);
    }
  }, [courseId]);

  useEffect(() => { loadDocs(); }, [loadDocs]);

  const setField = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  const submit = async (event) => {
    event.preventDefault();
    if (!file) {
      showNotification('error', 'Selecciona un archivo .md, .pdf o .json.');
      return;
    }
    setBusy(true);
    try {
      const result = await uploadCourseDocument(courseId, { ...form, file });
      showNotification('success', `Documento indexado (${result.chunks || 0} chunks).`);
      setFile(null);
      setForm((prev) => ({ ...prev, title: '', notes: '' }));
      await loadDocs();
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setBusy(false);
    }
  };

  const remove = async (docId) => {
    if (!window.confirm(`Eliminar ${docId} del conocimiento del curso?`)) return;
    setBusy(true);
    try {
      await deleteCourseDocument(courseId, docId);
      showNotification('success', 'Documento eliminado del RAG.');
      await loadDocs();
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setBusy(false);
    }
  };

  const reindex = async () => {
    setBusy(true);
    try {
      const result = await reindexCourseDocuments(courseId);
      showNotification('success', `Reindex listo: ${result.processed || 0} documentos.`);
      await loadDocs();
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="bg-kenth-card border border-kenth-border rounded-2xl p-5">
      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between mb-4">
        <div>
          <h2 className="text-sm font-black uppercase tracking-widest text-kenth-text">Documentos RAG del curso</h2>
          <p className="text-xs text-kenth-subtext mt-1">
            Sube conocimiento propio o derivado. La politica de copyright del backend valida antes de indexar.
          </p>
        </div>
        <button
          type="button"
          onClick={reindex}
          disabled={busy}
          className="px-4 py-2 rounded-xl border border-kenth-border bg-kenth-surface/10 text-kenth-text text-[10px] font-black uppercase tracking-widest hover:border-kenth-brightred disabled:opacity-40"
        >
          Reindex curso
        </button>
      </div>

      <form onSubmit={submit} className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-5">
        <div>
          <label className={labelCls}>Archivo</label>
          <input
            type="file"
            accept=".md,.pdf,.json"
            className={inputCls}
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            disabled={busy}
          />
        </div>
        <div>
          <label className={labelCls}>Titulo</label>
          <input className={inputCls} value={form.title} onChange={(e) => setField('title', e.target.value)} placeholder={file?.name || 'Nombre visible'} />
        </div>
        <div>
          <label className={labelCls}>Eje</label>
          <select className={inputCls} value={form.axis_id} onChange={(e) => setField('axis_id', e.target.value)}>
            <option value="">Curso completo</option>
            {axes.map((axis) => (
              <option key={axis.axis_id} value={axis.axis_id}>{axis.axis_id} - {axis.axis_title}</option>
            ))}
          </select>
        </div>
        <div>
          <label className={labelCls}>Capa</label>
          <select className={inputCls} value={form.doc_layer} onChange={(e) => setField('doc_layer', e.target.value)}>
            <option value="canonico">Canonico</option>
            <option value="derivado">Derivado</option>
          </select>
        </div>
        <div>
          <label className={labelCls}>Propiedad</label>
          <input className={inputCls} value={form.ownership} onChange={(e) => setField('ownership', e.target.value)} />
        </div>
        <label className="flex items-center gap-2 text-xs text-kenth-subtext pt-6">
          <input
            type="checkbox"
            checked={form.attribution_required}
            onChange={(e) => setField('attribution_required', e.target.checked)}
          />
          Requiere atribucion
        </label>
        <div className="md:col-span-2">
          <label className={labelCls}>Notas</label>
          <textarea rows={2} className={inputCls} value={form.notes} onChange={(e) => setField('notes', e.target.value)} />
        </div>
        <div className="md:col-span-2">
          <button
            type="submit"
            disabled={busy}
            className="px-4 py-2 rounded-xl bg-kenth-brightred hover:bg-red-600 text-white text-xs font-black uppercase tracking-widest disabled:opacity-40"
          >
            {busy ? 'Procesando...' : 'Subir e indexar'}
          </button>
        </div>
      </form>

      {loading ? (
        <p className="text-sm text-kenth-subtext">Cargando documentos...</p>
      ) : (
        <div className="overflow-x-auto border border-kenth-border rounded-xl">
          <table className="w-full text-sm">
            <thead className="bg-kenth-surface/10 text-kenth-subtext text-[10px] uppercase tracking-widest">
              <tr>
                <th className="text-left p-3">Documento</th>
                <th className="text-left p-3">Eje</th>
                <th className="text-left p-3">Capa</th>
                <th className="text-left p-3">Estado</th>
                <th className="text-right p-3">Accion</th>
              </tr>
            </thead>
            <tbody>
              {docs.map((doc) => (
                <tr key={doc.doc_id} className="border-t border-kenth-border">
                  <td className="p-3">
                    <div className="font-bold text-kenth-text">{doc.title || doc.doc_id}</div>
                    <div className="text-[11px] text-kenth-subtext">{doc.filename} {doc.chunks ? `- ${doc.chunks} chunks` : ''}</div>
                  </td>
                  <td className="p-3 text-kenth-subtext">{doc.axis_id || 'Curso'}</td>
                  <td className="p-3 text-kenth-subtext">{doc.doc_layer}</td>
                  <td className="p-3">
                    <span className={`inline-flex px-2 py-1 rounded-full border text-[10px] font-black uppercase tracking-widest ${statusClass(doc.status)}`}>
                      {doc.status || 'active'}
                    </span>
                  </td>
                  <td className="p-3 text-right">
                    <button
                      type="button"
                      onClick={() => remove(doc.doc_id)}
                      disabled={busy}
                      className="text-[10px] font-black uppercase tracking-widest text-red-400 hover:text-red-300 disabled:opacity-40"
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
              {docs.length === 0 && (
                <tr>
                  <td colSpan={5} className="p-5 text-center text-sm text-kenth-subtext">
                    No hay documentos del profesor para este curso.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
