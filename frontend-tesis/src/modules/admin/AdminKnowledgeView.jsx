import React, { useState, useEffect, useRef } from 'react';
import { getDocuments, uploadDocument, deleteDocument, indexKnowledgeBase, rebuildKnowledgeBase } from '../../shared/services/ragService';
import { showNotification } from '../../shared/components/ui/Notification';
import PageContainer from '../../shared/components/layout/PageContainer';

export default function AdminKnowledgeView() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [isIndexing, setIsIndexing] = useState(false);
  const [isRebuilding, setIsRebuilding] = useState(false);
  const [activeKnowledgeTab, setActiveKnowledgeTab] = useState('pdf');

  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchDocuments();
    const interval = setInterval(() => {
      fetchDocuments(false);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchDocuments = async (showLoading = true) => {
    if (showLoading) setLoading(true);
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch {
      if (showLoading) showNotification('error', 'Error al cargar los documentos de la base de conocimiento.');
    } finally {
      if (showLoading) setLoading(false);
    }
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const filename = file.name?.toLowerCase() || '';
    const isAllowedFile = (
      file.type === 'application/pdf'
      || file.type === 'application/json'
      || filename.endsWith('.json')
      || filename.endsWith('.md')
    );

    if (!isAllowedFile) {
      showNotification('error', 'Solo se permiten archivos PDF, JSON o Markdown.');
      return;
    }

    setIsUploading(true);
    try {
      const res = await uploadDocument(file);
      showNotification('success', res.message);
      fetchDocuments();
    } catch (error) {
      showNotification('error', error.message);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDelete = async (filename) => {
    if (!window.confirm(`Estas seguro de eliminar el archivo "${filename}"? La IA lo olvidara en la proxima sincronizacion.`)) return;

    try {
      const res = await deleteDocument(filename);
      showNotification('success', res.message);
      fetchDocuments();
    } catch (error) {
      showNotification('error', error.message);
    }
  };

  const handleIndex = async () => {
    setIsIndexing(true);
    try {
      const res = await indexKnowledgeBase();
      showNotification('success', res.message);
      fetchDocuments();
    } catch (error) {
      showNotification('error', error.message);
    } finally {
      setIsIndexing(false);
    }
  };

  const handleRebuild = async () => {
    const confirmed = window.confirm(
      '⚠️ REBUILD COMPLETO\n\nEsto eliminará TODA la base vectorial y re-indexará todos los documentos desde cero.\n\nUsa esto si modificaste ingest.py, chunking o metadatos.\n\n¿Estás seguro?'
    );
    if (!confirmed) return;
    
    setIsRebuilding(true);
    try {
      const res = await rebuildKnowledgeBase();
      showNotification('success', res.message);
      fetchDocuments();
    } catch (error) {
      showNotification('error', error.message);
    } finally {
      setIsRebuilding(false);
    }
  };

  const formatBytes = (bytes) => {
    if (!bytes) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  };

  const getDocumentType = (doc) => {
    const filename = doc.filename?.toLowerCase() || '';
    if (filename.endsWith('.pdf')) return 'pdf';
    if (filename.endsWith('.json')) return 'json';
    if (filename.endsWith('.md')) return 'md';
    return 'other';
  };

  const getVisualStatus = (doc) => {
    const status = doc.status || '';
    const errorMsg = doc.error_msg || '';
    const filename = doc.filename || '';

    if (status === 'indexed') return 'indexed';
    if (status === 'ready') return 'ready';
    if (status === 'processing') return 'processing';
    if (status === 'failed') return 'failed';

    const isCanonicalReference = (
      errorMsg.includes("status='canonical_v1'")
      || ['curso_manifest.json', 'mapa_curricular.json', 'TEMARIO_OFICIAL_V1.md'].includes(filename)
    );

    if (isCanonicalReference) return 'canonical';
    if (status === 'blocked') return 'blocked';
    return 'unclassified';
  };

  const pdfDocuments = documents.filter(doc => getDocumentType(doc) === 'pdf');
  const jsonDocuments = documents.filter(doc => getDocumentType(doc) === 'json');
  const mdDocuments = documents.filter(doc => getDocumentType(doc) === 'md');
  const otherDocuments = documents.filter(doc => getDocumentType(doc) === 'other');
  const indexedCount = documents.filter(doc => getVisualStatus(doc) === 'indexed').length;
  const readyCount = documents.filter(doc => getVisualStatus(doc) === 'ready').length;
  const processingCount = documents.filter(doc => getVisualStatus(doc) === 'processing').length;
  const failedCount = documents.filter(doc => getVisualStatus(doc) === 'failed').length;
  const blockedCount = documents.filter(doc => getVisualStatus(doc) === 'blocked').length;
  const canonicalCount = documents.filter(doc => getVisualStatus(doc) === 'canonical').length;
  const unclassifiedCount = documents.filter(doc => getVisualStatus(doc) === 'unclassified').length;
  const totalSize = documents.reduce((sum, doc) => sum + Number(doc.size_bytes || 0), 0);
  const activeDocuments = activeKnowledgeTab === 'pdf'
    ? pdfDocuments
    : activeKnowledgeTab === 'json'
      ? jsonDocuments
      : mdDocuments;
  const activeTabData = {
    pdf: {
      title: 'Teoria y conceptos',
      subtitle: 'Material principal en formato PDF',
      type: 'pdf'
    },
    json: {
      title: 'Videos y recursos',
      subtitle: 'Metadatos y referencias en JSON',
      type: 'json'
    },
    md: {
      title: 'Guias canonicas',
      subtitle: 'Documentos Markdown autorales',
      type: 'md'
    }
  }[activeKnowledgeTab];

  const statusStyles = {
    indexed: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    ready: 'bg-lime-500/10 text-lime-400 border-lime-500/30',
    processing: 'bg-sky-500/10 text-sky-400 border-sky-500/30',
    failed: 'bg-red-500/10 text-red-400 border-red-500/30',
    blocked: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    canonical: 'bg-violet-500/10 text-violet-300 border-violet-500/30',
    unclassified: 'bg-zinc-500/10 text-zinc-300 border-zinc-500/30'
  };

  const statusLabels = {
    indexed: 'Vectorizado',
    ready: 'Listo para indexar',
    processing: 'Procesando',
    failed: 'Error',
    blocked: 'Bloqueado por politica',
    canonical: 'Canonico / no indexable',
    unclassified: 'No clasificado'
  };

  const renderStatusBadge = (doc) => {
    const status = getVisualStatus(doc);
    return (
      <span
        title={doc.error_msg || statusLabels[status] || 'No clasificado'}
        className={`inline-flex h-7 items-center rounded-full border px-3 text-[9px] font-black uppercase tracking-widest ${statusStyles[status] || statusStyles.unclassified}`}
      >
        {statusLabels[status] || 'No clasificado'}
      </span>
    );
  };

  const renderDocumentIcon = (type) => {
    const iconData = {
      pdf: {
        color: 'text-kenth-brightred bg-kenth-brightred/10',
        path: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.414V19a2 2 0 01-2 2z'
      },
      json: {
        color: 'text-sky-400 bg-sky-500/10',
        path: 'M4 6h16M4 10h16M4 14h16M4 18h16'
      },
      md: {
        color: 'text-violet-300 bg-violet-500/10',
        path: 'M8 7h8M8 11h8M8 15h4m-5 6h10a2 2 0 002-2V7.5a2 2 0 00-.586-1.414l-3.5-3.5A2 2 0 0013.5 2H7a2 2 0 00-2 2v15a2 2 0 002 2z'
      }
    }[type] || {
      color: 'text-zinc-300 bg-zinc-500/10',
      path: 'M12 6v6l4 2'
    };

    return (
      <div className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl ${iconData.color}`}>
        <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d={iconData.path} />
        </svg>
      </div>
    );
  };

  const typeLabels = {
    pdf: 'Documento PDF',
    json: 'Metadata JSON',
    md: 'Guia Markdown',
    other: 'Archivo no clasificado'
  };

  const renderDocumentRow = (doc, idx, type) => (
    <div
      key={`${doc.filename}-${idx}`}
      className="group grid grid-cols-[auto_1fr] gap-4 rounded-2xl border border-kenth-border bg-kenth-surface/5 p-4 transition-all hover:border-kenth-brightred/30 hover:bg-kenth-surface/10 md:grid-cols-[auto_1fr_auto]"
    >
      {renderDocumentIcon(type)}

      <div className="min-w-0">
        <div className="flex min-w-0 flex-col gap-2 md:flex-row md:items-center">
          <p className="truncate text-sm font-black text-kenth-text md:text-base">{doc.filename}</p>
          {renderStatusBadge(doc)}
        </div>
        <div className="mt-2 flex flex-wrap gap-3 text-[10px] font-black uppercase tracking-widest text-kenth-subtext">
          <span>{typeLabels[type] || typeLabels.other}</span>
          <span className="text-kenth-border">/</span>
          <span>{formatBytes(doc.size_bytes)}</span>
        </div>
      </div>

      <button
        type="button"
        onClick={() => handleDelete(doc.filename)}
        className="col-span-2 flex h-11 items-center justify-center rounded-2xl border border-red-500/20 bg-red-500/10 px-4 text-[10px] font-black uppercase tracking-widest text-red-400 transition-all hover:bg-red-500 hover:text-white md:col-span-1 md:w-11 md:px-0 md:opacity-0 md:group-hover:opacity-100 md:focus:opacity-100"
        aria-label={`Eliminar ${doc.filename}`}
      >
        <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
        <span className="ml-2 md:hidden">Eliminar</span>
      </button>
    </div>
  );

  const renderDocumentGroup = (title, subtitle, items, type) => (
    <section className="space-y-4">
      <div className="flex flex-col gap-2 border-b border-kenth-border pb-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h3 className="text-lg font-black uppercase italic tracking-tighter text-kenth-text">{title}</h3>
          <p className="text-[10px] font-bold uppercase tracking-widest text-kenth-subtext">{subtitle}</p>
        </div>
        <span className="w-fit rounded-full border border-kenth-border bg-kenth-surface/10 px-3 py-1 text-[10px] font-black uppercase tracking-widest text-kenth-subtext">
          {items.length} archivos
        </span>
      </div>

      {items.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-kenth-border bg-kenth-surface/5 p-6 text-sm font-bold text-kenth-subtext">
          No hay archivos en esta categoria.
        </div>
      ) : (
        <div className="space-y-3">
          {items.map((doc, idx) => renderDocumentRow(doc, idx, type))}
        </div>
      )}
    </section>
  );

  return (
    <PageContainer>
      <div className="mb-10 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <span className="mb-4 block text-[10px] font-black uppercase tracking-[0.4em] text-kenth-brightred">Panel de IA</span>
          <h1 className="text-4xl font-black uppercase italic leading-none tracking-tighter md:text-6xl">
            Gestor de <span className="text-kenth-brightred">Conocimiento IA</span>
          </h1>
          <p className="mt-4 max-w-2xl text-[10px] font-bold uppercase tracking-widest text-kenth-subtext">
            Organiza los documentos que alimentan la memoria del asistente virtual.
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={handleIndex}
            disabled={isIndexing || isRebuilding}
            className="inline-flex h-12 items-center justify-center gap-3 rounded-2xl border border-emerald-500/30 bg-emerald-500/10 px-5 text-[10px] font-black uppercase tracking-widest text-emerald-400 transition-all hover:bg-emerald-500 hover:text-white disabled:opacity-50"
          >
            <svg className={`h-4 w-4 ${isIndexing ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {isIndexing ? 'Sincronizando...' : 'Sincronizar Nuevos'}
          </button>

          <button
            type="button"
            onClick={handleRebuild}
            disabled={isIndexing || isRebuilding}
            className="inline-flex h-12 items-center justify-center gap-3 rounded-2xl border border-amber-500/30 bg-amber-500/10 px-5 text-[10px] font-black uppercase tracking-widest text-amber-400 transition-all hover:bg-amber-500 hover:text-white disabled:opacity-50"
          >
            <svg className={`h-4 w-4 ${isRebuilding ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            {isRebuilding ? 'Reconstruyendo...' : 'Rebuild Completo'}
          </button>
        </div>
      </div>

      <div className="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <div className="rounded-[2rem] border border-kenth-border bg-kenth-card p-5 shadow-xl">
          <p className="text-[9px] font-black uppercase tracking-widest text-kenth-subtext">Archivos</p>
          <p className="mt-3 text-4xl font-black italic tracking-tighter text-kenth-text">{documents.length}</p>
        </div>
        <div className="rounded-[2rem] border border-emerald-500/20 bg-emerald-500/5 p-5 shadow-xl">
          <p className="text-[9px] font-black uppercase tracking-widest text-emerald-400">Vectorizados</p>
          <p className="mt-3 text-4xl font-black italic tracking-tighter text-emerald-400">{indexedCount}</p>
        </div>
        <div className="rounded-[2rem] border border-lime-500/20 bg-lime-500/5 p-5 shadow-xl">
          <p className="text-[9px] font-black uppercase tracking-widest text-lime-400">Para indexar</p>
          <p className="mt-3 text-4xl font-black italic tracking-tighter text-lime-400">{readyCount}</p>
        </div>
        <div className="rounded-[2rem] border border-kenth-border bg-kenth-card p-5 shadow-xl">
          <p className="text-[9px] font-black uppercase tracking-widest text-kenth-subtext">Bloqueados</p>
          <p className="mt-3 text-4xl font-black italic tracking-tighter text-amber-400">{blockedCount + canonicalCount}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-8 xl:grid-cols-12">
        <aside className="xl:col-span-4">
          <div className="sticky top-8 space-y-6">
            <div className="overflow-hidden rounded-[2.5rem] border border-kenth-border bg-kenth-card shadow-2xl">
              <div className="border-b border-kenth-border bg-kenth-surface/5 p-7">
                <div className="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-kenth-brightred/10 text-kenth-brightred">
                  <svg className="h-7 w-7" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                </div>
                <h2 className="text-2xl font-black uppercase italic tracking-tighter text-kenth-text">Subir fuente</h2>
                <p className="mt-3 text-sm font-medium leading-relaxed text-kenth-subtext">
                  Agrega PDFs, JSONs o Markdown. Los archivos subidos quedan fuera de indexacion hasta cumplir la politica documental.
                </p>
              </div>

              <div className="p-7">
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept="application/pdf,application/json,.json,.md"
                  className="hidden"
                />
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isUploading}
                  className="flex h-14 w-full items-center justify-center gap-3 rounded-2xl bg-kenth-text px-5 text-[10px] font-black uppercase tracking-widest text-kenth-bg shadow-lg shadow-black/20 transition-all hover:bg-kenth-brightred hover:text-white disabled:opacity-50"
                >
                  {isUploading ? (
                    <>
                      <span className="h-5 w-5 rounded-full border-2 border-current border-t-transparent animate-spin" />
                      Subiendo...
                    </>
                  ) : (
                    <>
                      <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                      </svg>
                      Seleccionar archivo
                    </>
                  )}
                </button>

                <div className="mt-6 grid grid-cols-3 gap-3">
                  <div className="rounded-2xl border border-kenth-border bg-kenth-surface/5 p-4">
                    <p className="text-[9px] font-black uppercase tracking-widest text-kenth-subtext">PDF</p>
                    <p className="mt-2 text-xl font-black text-kenth-text">{pdfDocuments.length}</p>
                  </div>
                  <div className="rounded-2xl border border-kenth-border bg-kenth-surface/5 p-4">
                    <p className="text-[9px] font-black uppercase tracking-widest text-kenth-subtext">JSON</p>
                    <p className="mt-2 text-xl font-black text-kenth-text">{jsonDocuments.length}</p>
                  </div>
                  <div className="rounded-2xl border border-kenth-border bg-kenth-surface/5 p-4">
                    <p className="text-[9px] font-black uppercase tracking-widest text-kenth-subtext">MD</p>
                    <p className="mt-2 text-xl font-black text-kenth-text">{mdDocuments.length}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="rounded-[2rem] border border-kenth-border bg-kenth-surface/5 p-6">
              <p className="text-[10px] font-black uppercase tracking-widest text-kenth-subtext">Estado de indexacion</p>
              <div className="mt-5 space-y-3 text-sm font-bold text-kenth-subtext">
                <div className="flex items-center justify-between"><span>Vectorizados</span><span className="text-emerald-400">{indexedCount}</span></div>
                <div className="flex items-center justify-between"><span>Listos para indexar</span><span className="text-lime-400">{readyCount}</span></div>
                <div className="flex items-center justify-between"><span>Bloqueados por politica</span><span className="text-amber-400">{blockedCount}</span></div>
                <div className="flex items-center justify-between"><span>Canonicos/no indexables</span><span className="text-violet-300">{canonicalCount}</span></div>
                {unclassifiedCount > 0 && (
                  <div className="flex items-center justify-between"><span>No clasificados</span><span className="text-zinc-300">{unclassifiedCount}</span></div>
                )}
                {processingCount > 0 && (
                  <div className="flex items-center justify-between"><span>Procesando</span><span className="text-sky-400">{processingCount}</span></div>
                )}
                <div className="flex items-center justify-between"><span>Con error</span><span className="text-red-400">{failedCount}</span></div>
                <div className="flex items-center justify-between"><span>Tamano total</span><span className="text-kenth-text">{formatBytes(totalSize)}</span></div>
              </div>
            </div>

            {/* Panel de Acciones Rapidas */}
            <div className="rounded-[2rem] border border-amber-500/20 bg-amber-500/5 p-6">
              <div className="mb-4 flex items-center gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-500/10 text-amber-400">
                  <svg className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <p className="text-[10px] font-black uppercase tracking-widest text-amber-400">Acciones rapidas</p>
              </div>
              <div className="space-y-3">
                <button
                  type="button"
                  onClick={handleIndex}
                  disabled={isIndexing || isRebuilding}
                  className="flex h-11 w-full items-center justify-center gap-2 rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-[9px] font-black uppercase tracking-widest text-emerald-400 transition-all hover:bg-emerald-500 hover:text-white disabled:opacity-40"
                >
                  {isIndexing ? (
                    <><span className="h-4 w-4 rounded-full border-2 border-current border-t-transparent animate-spin" /> Procesando...</>
                  ) : (
                    'Indexar nuevos archivos'
                  )}
                </button>
                <button
                  type="button"
                  onClick={handleRebuild}
                  disabled={isIndexing || isRebuilding}
                  className="flex h-11 w-full items-center justify-center gap-2 rounded-xl border border-amber-500/20 bg-amber-500/10 text-[9px] font-black uppercase tracking-widest text-amber-400 transition-all hover:bg-amber-500 hover:text-white disabled:opacity-40"
                >
                  {isRebuilding ? (
                    <><span className="h-4 w-4 rounded-full border-2 border-current border-t-transparent animate-spin" /> Reconstruyendo...</>
                  ) : (
                    'Rebuild completo'
                  )}
                </button>
              </div>
              <p className="mt-4 text-[9px] font-medium leading-relaxed text-amber-400/60">
                Rebuild elimina la base vectorial y re-indexa todo. Usar si cambiaste ingest.py o metadatos.
              </p>
            </div>
          </div>
        </aside>

        <section className="xl:col-span-8">
          <div className="rounded-[2.5rem] border border-kenth-border bg-kenth-card p-5 shadow-2xl md:p-8">
            <div className="mb-8 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="text-2xl font-black uppercase italic tracking-tighter text-kenth-text md:text-3xl">Base de conocimiento</h2>
                <p className="mt-2 text-[10px] font-bold uppercase tracking-widest text-kenth-subtext">
                  Documentos disponibles para el tutor IA.
                </p>
              </div>
              <span className="w-fit rounded-full border border-kenth-brightred/30 bg-kenth-brightred/10 px-4 py-2 text-[10px] font-black uppercase tracking-widest text-kenth-brightred">
                {documents.length} fuentes
              </span>
            </div>

            {loading ? (
              <div className="flex flex-col items-center justify-center rounded-[2rem] border border-dashed border-kenth-border bg-kenth-surface/5 py-24">
                <div className="mb-5 h-12 w-12 rounded-full border-4 border-kenth-brightred/20 border-t-kenth-brightred animate-spin" />
                <p className="text-[10px] font-black uppercase tracking-[0.3em] text-kenth-subtext animate-pulse">Cargando memoria...</p>
              </div>
            ) : documents.length === 0 ? (
              <div className="rounded-[2rem] border border-dashed border-kenth-border bg-kenth-surface/5 px-6 py-20 text-center">
                <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-kenth-brightred/10 text-kenth-brightred">
                  <svg className="h-8 w-8" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </div>
                <h3 className="text-2xl font-black uppercase italic tracking-tighter text-kenth-text">Memoria vacia</h3>
                <p className="mx-auto mt-3 max-w-md text-sm font-medium text-kenth-subtext">
                  Sube tu primer PDF, JSON o Markdown para empezar a construir la base de conocimiento del asistente.
                </p>
              </div>
            ) : (
              <div className="space-y-8">
                <div className="grid grid-cols-1 gap-3 rounded-[2rem] border border-kenth-border bg-kenth-surface/5 p-2 md:grid-cols-3">
                  <button
                    type="button"
                    onClick={() => setActiveKnowledgeTab('pdf')}
                    className={`flex min-h-20 items-center justify-between gap-4 rounded-[1.5rem] border p-4 text-left transition-all ${
                      activeKnowledgeTab === 'pdf'
                        ? 'border-kenth-brightred/40 bg-kenth-brightred/10 text-kenth-text shadow-lg shadow-kenth-brightred/5'
                        : 'border-transparent text-kenth-subtext hover:border-kenth-border hover:bg-kenth-card'
                    }`}
                  >
                    <div className="min-w-0">
                      <p className="truncate text-sm font-black uppercase italic tracking-tighter md:text-base">Teoria y conceptos</p>
                      <p className="mt-1 text-[9px] font-black uppercase tracking-widest">PDF del asistente</p>
                    </div>
                    <span className={`shrink-0 rounded-full border px-3 py-1 text-[9px] font-black uppercase tracking-widest ${
                      activeKnowledgeTab === 'pdf'
                        ? 'border-kenth-brightred/30 bg-kenth-brightred/10 text-kenth-brightred'
                        : 'border-kenth-border bg-kenth-surface/10 text-kenth-subtext'
                    }`}>
                      {pdfDocuments.length}
                    </span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setActiveKnowledgeTab('json')}
                    className={`flex min-h-20 items-center justify-between gap-4 rounded-[1.5rem] border p-4 text-left transition-all ${
                      activeKnowledgeTab === 'json'
                        ? 'border-sky-400/40 bg-sky-500/10 text-kenth-text shadow-lg shadow-sky-500/5'
                        : 'border-transparent text-kenth-subtext hover:border-kenth-border hover:bg-kenth-card'
                    }`}
                  >
                    <div className="min-w-0">
                      <p className="truncate text-sm font-black uppercase italic tracking-tighter md:text-base">Videos y recursos</p>
                      <p className="mt-1 text-[9px] font-black uppercase tracking-widest">JSON de contenidos</p>
                    </div>
                    <span className={`shrink-0 rounded-full border px-3 py-1 text-[9px] font-black uppercase tracking-widest ${
                      activeKnowledgeTab === 'json'
                        ? 'border-sky-400/30 bg-sky-500/10 text-sky-400'
                        : 'border-kenth-border bg-kenth-surface/10 text-kenth-subtext'
                    }`}>
                      {jsonDocuments.length}
                    </span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setActiveKnowledgeTab('md')}
                    className={`flex min-h-20 items-center justify-between gap-4 rounded-[1.5rem] border p-4 text-left transition-all ${
                      activeKnowledgeTab === 'md'
                        ? 'border-violet-400/40 bg-violet-500/10 text-kenth-text shadow-lg shadow-violet-500/5'
                        : 'border-transparent text-kenth-subtext hover:border-kenth-border hover:bg-kenth-card'
                    }`}
                  >
                    <div className="min-w-0">
                      <p className="truncate text-sm font-black uppercase italic tracking-tighter md:text-base">Guias y canonicos</p>
                      <p className="mt-1 text-[9px] font-black uppercase tracking-widest">Markdown del corpus</p>
                    </div>
                    <span className={`shrink-0 rounded-full border px-3 py-1 text-[9px] font-black uppercase tracking-widest ${
                      activeKnowledgeTab === 'md'
                        ? 'border-violet-400/30 bg-violet-500/10 text-violet-300'
                        : 'border-kenth-border bg-kenth-surface/10 text-kenth-subtext'
                    }`}>
                      {mdDocuments.length}
                    </span>
                  </button>
                </div>

                {renderDocumentGroup(activeTabData.title, activeTabData.subtitle, activeDocuments, activeTabData.type)}

                {otherDocuments.length > 0 && (
                  <div className="rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-4 text-[10px] font-bold uppercase tracking-widest text-yellow-400">
                    Hay {otherDocuments.length} archivos no clasificados fuera de PDF/JSON/Markdown.
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
      </div>
    </PageContainer>
  );
}
