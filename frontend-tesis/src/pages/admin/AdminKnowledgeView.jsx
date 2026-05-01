import React, { useState, useEffect, useRef } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { getDocuments, uploadDocument, deleteDocument, indexKnowledgeBase } from '../../services/ragService';

export default function AdminKnowledgeView() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [isIndexing, setIsIndexing] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchDocuments();
    
    // Polling cada 3 segundos para actualizar el estado de procesamiento en tiempo real
    const interval = setInterval(() => {
      fetchDocuments(false); // pasar false para no mostrar loading spinner de toda la página
    }, 3000);
    
    return () => clearInterval(interval);
  }, []);

  const fetchDocuments = async (showLoading = true) => {
    if (showLoading) setLoading(true);
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (error) {
      if (showLoading) showMessage('error', 'Error al cargar los documentos de la base de conocimiento.');
    } finally {
      if (showLoading) setLoading(false);
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      showMessage('error', 'Solo se permiten archivos PDF.');
      return;
    }

    setIsUploading(true);
    try {
      const res = await uploadDocument(file);
      showMessage('success', res.message);
      fetchDocuments();
    } catch (error) {
      showMessage('error', error.message);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDelete = async (filename) => {
    if (!window.confirm(`¿Estás seguro de eliminar el archivo "${filename}"? La IA lo olvidará en la próxima sincronización.`)) return;
    
    try {
      const res = await deleteDocument(filename);
      showMessage('success', res.message);
      fetchDocuments();
    } catch (error) {
      showMessage('error', error.message);
    }
  };

  const handleIndex = async () => {
    setIsIndexing(true);
    try {
      const res = await indexKnowledgeBase();
      showMessage('success', res.message);
    } catch (error) {
      showMessage('error', error.message);
    } finally {
      setTimeout(() => setIsIndexing(false), 2000); // Dar un tiempo extra visual
    }
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <DashboardLayout>
      <div className="max-w-5xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-2 uppercase tracking-tighter italic">
          Gestor de <span className="text-kenth-brightred">Conocimiento IA</span>
        </h1>
        <p className="text-gray-400 mb-8 font-medium">Administra los documentos que alimentan la memoria del asistente virtual.</p>

        {message.text && (
          <div className={`p-4 rounded-xl mb-6 font-bold flex items-center gap-3 animate-in fade-in ${message.type === 'success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-red-500/10 text-red-400 border border-red-500/30'}`}>
            {message.type === 'success' ? (
               <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
            ) : (
               <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            )}
            {message.text}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Columna Izquierda: Acciones */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Tarjeta de Subida */}
            <div className="bg-[#1e1e20] p-6 rounded-[2rem] border border-kenth-surface/20 shadow-[0_20px_50px_rgba(0,0,0,0.3)] flex flex-col items-center text-center">
              <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mb-4 text-blue-400">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Subir Documento</h3>
              <p className="text-gray-400 text-sm mb-6">Solo archivos PDF. El contenido será extraído y vectorizado.</p>
              
              <input 
                type="file" 
                ref={fileInputRef}
                onChange={handleFileChange}
                accept="application/pdf"
                className="hidden"
              />
              
              <button 
                onClick={() => fileInputRef.current?.click()}
                disabled={isUploading}
                className="w-full bg-[#2D2D30] hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-xl border border-blue-500/30 transition-all shadow-inner disabled:opacity-50 flex justify-center items-center gap-2"
              >
                {isUploading ? (
                  <><svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Subiendo...</>
                ) : 'Seleccionar PDF'}
              </button>
            </div>

            {/* Tarjeta de Sincronización */}
            <div className="bg-[#1e1e20] p-6 rounded-[2rem] border border-kenth-brightred/30 shadow-[0_20px_50px_rgba(225,29,72,0.1)] flex flex-col items-center text-center">
              <div className="w-16 h-16 bg-kenth-brightred/10 rounded-full flex items-center justify-center mb-4 text-kenth-brightred">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Sincronizar IA</h3>
              <p className="text-gray-400 text-sm mb-6">Convierte todos los PDFs de la carpeta en vectores para la memoria de la IA. ¡Hazlo después de subir o borrar!</p>
              
              <button 
                onClick={handleIndex}
                disabled={isIndexing}
                className="w-full bg-kenth-brightred hover:bg-white hover:text-kenth-bg text-white font-black py-4 rounded-xl transition-all shadow-xl shadow-kenth-brightred/20 uppercase tracking-tighter italic disabled:opacity-50 flex justify-center items-center gap-2 group"
              >
                {isIndexing ? (
                  <><svg className="animate-spin h-5 w-5 text-white group-hover:text-kenth-bg" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Vectorizando...</>
                ) : 'Iniciar Vectorización'}
              </button>
            </div>

          </div>

          {/* Columna Derecha: Lista de Documentos */}
          <div className="lg:col-span-2 bg-[#1e1e20] p-6 md:p-8 rounded-[2rem] border border-kenth-surface/20 shadow-[0_20px_50px_rgba(0,0,0,0.3)]">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <svg className="w-6 h-6 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
              Documentos Indexados ({documents.length})
            </h2>

            {loading ? (
              <div className="flex justify-center items-center py-20">
                <svg className="animate-spin h-10 w-10 text-kenth-brightred" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              </div>
            ) : documents.length === 0 ? (
              <div className="text-center py-20 border-2 border-dashed border-gray-700/50 rounded-2xl">
                <p className="text-gray-500 font-bold italic text-lg mb-2">La base de conocimiento está vacía</p>
                <p className="text-sm text-gray-600">Sube algunos PDFs para entrenar a tu asistente virtual.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {documents.map((doc, idx) => (
                  <div key={idx} className="bg-[#2D2D30] p-4 rounded-xl flex items-center justify-between group hover:border-kenth-brightred/30 border border-transparent transition-colors">
                    <div className="flex items-center gap-4 overflow-hidden">
                      <div className="w-10 h-10 bg-red-500/10 rounded-lg flex items-center justify-center shrink-0 text-red-500">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
                      </div>
                      <div className="truncate">
                        <div className="flex items-center gap-3">
                          <p className="text-white font-bold truncate max-w-[200px] sm:max-w-xs">{doc.filename}</p>
                          {doc.status === 'indexed' && (
                            <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider flex items-center gap-1">
                              <svg className="w-3 h-3" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg> Vectorizado
                            </span>
                          )}
                          {doc.status === 'processing' && (
                            <span className="bg-blue-500/20 text-blue-400 border border-blue-500/30 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider flex items-center gap-1">
                              <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Procesando
                            </span>
                          )}
                          {doc.status === 'failed' && (
                            <span className="bg-red-500/20 text-red-400 border border-red-500/30 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider flex items-center gap-1" title={doc.error_msg}>
                              <svg className="w-3 h-3" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg> Error
                            </span>
                          )}
                          {doc.status === 'unindexed' && (
                            <span className="bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider flex items-center gap-1">
                              <svg className="w-3 h-3" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg> Pendiente
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">{formatBytes(doc.size_bytes)}</p>
                      </div>
                    </div>
                    <button 
                      onClick={() => handleDelete(doc.filename)}
                      className="p-2 text-gray-500 hover:text-white hover:bg-red-500 rounded-lg transition-colors shrink-0 opacity-0 group-hover:opacity-100 focus:opacity-100"
                      title="Eliminar PDF"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
