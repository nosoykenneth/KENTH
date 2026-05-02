import React, { useState, useRef, useEffect } from 'react';
import { askOllamaDirect, getChatMessages } from '../../services/aiService';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

export default function OllamaChat({ contextoLeccion = '', sessionId = null, isExternalLoading = false, setExternalLoading = () => {} }) {
  const [pregunta, setPregunta] = useState('');
  const [internalLoading, setInternalLoading] = useState(false);
  const [historial, setHistorial] = useState([]); 
  const [imagenBase64, setImagenBase64] = useState('');
  const [usarInternet, setUsarInternet] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  
  const fileInputRef = useRef(null);
  const chatContainerRef = useRef(null);
  
  // Ref para rastrear el sessionId actual y evitar fugas de mensajes entre sesiones
  const currentSessionIdRef = useRef(sessionId);

  // El estado de carga real es la unión del interno y el externo
  const cargando = internalLoading || isExternalLoading;

  // Actualizar el ref cada vez que cambie el sessionId
  useEffect(() => {
    currentSessionIdRef.current = sessionId;
  }, [sessionId]);

  // Cargar historial de la base de datos si hay un sessionId
  useEffect(() => {
    if (sessionId) {
      const loadHistory = async () => {
        try {
          setInternalLoading(true);
          const messages = await getChatMessages(sessionId);
          // Antes de setear, verificamos que seguimos en la misma sesión
          if (currentSessionIdRef.current === sessionId) {
            setHistorial(messages);
          }
        } catch (error) {
          console.error("Error al cargar historial:", error);
        } finally {
          setInternalLoading(false);
        }
      };
      loadHistory();
    } else {
      setHistorial([]);
    }
  }, [sessionId]);

  // Auto-scroll suave
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, [historial, cargando]);

  const handleFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onloadend = () => setImagenBase64(reader.result);
      reader.readAsDataURL(file);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    handleFile(file);
  };

  const handlePaste = (e) => {
    const items = e.clipboardData.items;
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf('image') !== -1) {
        const file = items[i].getAsFile();
        handleFile(file);
        break;
      }
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const quitarImagen = () => {
    setImagenBase64('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const consultarOllama = async () => {
    if (!pregunta.trim() && !imagenBase64) return;
    
    const requestSessionId = sessionId; // Sesión en la que se disparó la pregunta
    const nuevoMensajeUsuario = { role: 'user', content: pregunta, image: imagenBase64 };
    setHistorial(prev => [...prev, nuevoMensajeUsuario]);
    
    setExternalLoading(true);
    const preguntaEnviada = pregunta;
    const imagenEnviada = imagenBase64;
    
    setPregunta(''); 
    quitarImagen();

    try {
      const data = await askOllamaDirect(
        preguntaEnviada, 
        contextoLeccion, 
        imagenEnviada, 
        usarInternet, 
        requestSessionId
      );
      
      // CRÍTICO: Verificamos si la sesión activa (según el ref) sigue siendo
      // la misma en la que disparamos la pregunta.
      if (currentSessionIdRef.current === requestSessionId) {
        setHistorial(prev => [...prev, { role: 'assistant', content: data.respuesta }]);
      }
    } catch (error) {
      console.error("Error de conexión:", error);
      if (currentSessionIdRef.current === requestSessionId) {
        setHistorial(prev => [...prev, { role: 'assistant', content: `Error: ${error.message}` }]);
      }
    } finally {
      // Liberamos la carga para esa sesión específica
      setExternalLoading(false);
    }
  };

  return (
    <div 
      className={`flex flex-col h-full w-full bg-transparent overflow-hidden transition-all duration-300 ${isDragging ? 'bg-kenth-brightred/5' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
        
        {/* Overlay de Drag & Drop */}
        <AnimatePresence>
          {isDragging && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 z-50 bg-kenth-bg/80 backdrop-blur-md flex flex-col items-center justify-center border-4 border-dashed border-kenth-brightred pointer-events-none"
            >
              <div className="w-24 h-24 bg-kenth-brightred/20 rounded-full flex items-center justify-center mb-4">
                <svg className="w-12 h-12 text-kenth-brightred animate-bounce" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
              </div>
              <p className="text-xl font-black uppercase tracking-widest text-kenth-text italic">Suelta tu imagen aquí</p>
              <p className="text-sm text-kenth-subtext mt-2">Soporta PNG, JPG y Capturas de Pantalla</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Historial con Scroll */}
        <div 
          ref={chatContainerRef} 
          className="flex-1 overflow-y-auto px-6 py-10 flex flex-col gap-8 scrollbar-none"
        >
          {historial.length === 0 && !cargando && (
            <div className="flex flex-col items-center justify-center h-full text-center text-kenth-subtext gap-6 animate-in fade-in duration-1000">
               <div className="w-24 h-24 bg-kenth-surface/5 rounded-full flex items-center justify-center border border-kenth-border shadow-inner">
                 <svg className="w-12 h-12 text-kenth-brightred/30 animate-pulse" fill="none" stroke="currentColor" strokeWidth={1} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
               </div>
               <div className="max-w-sm">
                 <p className="text-sm font-bold uppercase tracking-widest text-kenth-text mb-2 italic">Laboratorio de Audio KENTH</p>
                 <p className="text-xs text-kenth-subtext leading-relaxed font-medium">
                   "El conocimiento se construye a través de la pregunta correcta." 
                   Dime, ¿qué aspecto de tu sonido quieres perfeccionar hoy?
                 </p>
               </div>
            </div>
          )}
          
          <AnimatePresence initial={false}>
            {historial.map((msg, index) => (
              <motion.div 
                key={index} 
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex flex-col gap-2 max-w-[85%] md:max-w-[70%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                  
                  {/* Etiqueta de Autor */}
                  <span className={`text-[9px] font-black uppercase tracking-[0.2em] mb-1 ${msg.role === 'user' ? 'text-kenth-subtext' : 'text-kenth-brightred'}`}>
                    {msg.role === 'user' ? 'Tú' : 'Tutor Socrático'}
                  </span>

                  <div className={`relative group px-5 py-4 shadow-2xl transition-all duration-300 ${
                    msg.role === 'user' 
                      ? 'bg-kenth-brightred text-white rounded-[2rem] rounded-tr-sm shadow-[0_10px_30px_rgba(195,7,63,0.2)]' 
                      : 'bg-kenth-card border border-kenth-border text-kenth-text rounded-[2rem] rounded-tl-sm backdrop-blur-sm'
                  }`}>
                    {msg.image && (
                      <div className="mb-4 rounded-2xl overflow-hidden border border-white/10 shadow-lg">
                        <img src={msg.image} alt="Adjunto" className="w-full max-w-[400px] h-auto" />
                      </div>
                    )}
                    <div className={`text-sm md:text-[15px] leading-relaxed font-normal tracking-wide prose prose-invert prose-sm max-w-none ${msg.role === 'user' ? 'prose-p:text-white prose-headings:text-white' : 'prose-p:text-kenth-text prose-headings:text-kenth-text prose-strong:text-kenth-brightred'}`}>
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {cargando && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="bg-kenth-surface/10 border border-kenth-border rounded-full px-6 py-3 flex items-center gap-4 backdrop-blur-md">
                 <div className="flex gap-1.5">
                   <div className="w-2 h-2 bg-kenth-brightred rounded-full animate-bounce [animation-duration:0.8s]"></div>
                   <div className="w-2 h-2 bg-kenth-brightred rounded-full animate-bounce [animation-duration:0.8s] [animation-delay:0.2s]"></div>
                   <div className="w-2 h-2 bg-kenth-brightred rounded-full animate-bounce [animation-duration:0.8s] [animation-delay:0.4s]"></div>
                 </div>
                 <span className="text-[10px] text-kenth-subtext uppercase font-black tracking-widest italic">Kenth está pensando...</span>
              </div>
            </motion.div>
          )}
        </div>

        {/* Área de Input con diseño integrado */}
        <div className="px-6 pb-8 pt-2 bg-gradient-to-t from-kenth-bg via-kenth-bg to-transparent z-30">
          <div className="max-w-4xl mx-auto flex flex-col gap-4">
            
            {/* Previsualización Imagen (Flotante) */}
            <AnimatePresence>
              {imagenBase64 && (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.8, y: 20 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.8, y: 20 }}
                  className="relative w-24 h-24 rounded-2xl overflow-hidden border-2 border-kenth-brightred shadow-2xl z-50 ml-4 mb-2"
                >
                  <img src={imagenBase64} alt="Preview" className="w-full h-full object-cover" />
                  <button onClick={quitarImagen} className="absolute top-1 right-1 bg-kenth-brightred text-white rounded-full p-1 shadow-lg hover:bg-red-700 transition-colors">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                  </button>
                </motion.div>
              )}
            </AnimatePresence>

            <div className="relative group">
              {/* Resplandor de fondo al enfocar */}
              <div className="absolute -inset-1 bg-gradient-to-r from-kenth-brightred/20 to-transparent rounded-[2rem] blur-xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-700"></div>
              
              <div className="relative flex items-end gap-4 bg-kenth-card/80 backdrop-blur-2xl p-3 rounded-[2rem] border border-kenth-border shadow-2xl focus-within:border-kenth-brightred transition-all duration-500">
                <button 
                  onClick={() => fileInputRef.current.click()}
                  className="p-3.5 text-kenth-subtext hover:text-white transition-all rounded-full hover:bg-kenth-surface/20"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" /></svg>
                </button>
                <input type="file" ref={fileInputRef} onChange={handleImageUpload} accept="image/*" className="hidden" />
                
                <textarea 
                  className="flex-1 bg-transparent text-kenth-text border-none focus:ring-0 py-3 text-sm md:text-base max-h-40 resize-none scrollbar-none font-medium placeholder:text-kenth-subtext/40"
                  placeholder="Describe tu duda o adjunta una captura de tu DAW..."
                  value={pregunta}
                  onChange={(e) => setPregunta(e.target.value)}
                  onPaste={handlePaste}
                  rows={1}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      consultarOllama();
                    }
                  }}
                />

                <div className="flex items-center gap-2 pr-1">
                  <button 
                    onClick={() => setUsarInternet(!usarInternet)}
                    className={`p-3.5 transition-all rounded-full ${usarInternet ? 'text-white bg-kenth-brightred shadow-[0_0_20px_rgba(195,7,63,0.4)]' : 'text-kenth-subtext hover:text-white hover:bg-kenth-surface/20'}`}
                    title="Modo Búsqueda Web"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>
                  </button>

                  <button 
                    onClick={consultarOllama}
                    disabled={cargando || (!pregunta.trim() && !imagenBase64)}
                    className="p-4 bg-kenth-brightred text-white rounded-full shadow-2xl hover:bg-red-600 hover:scale-105 active:scale-95 transition-all duration-300 disabled:opacity-10 disabled:grayscale disabled:scale-100 disabled:hover:bg-kenth-brightred"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" /></svg>
                  </button>
                </div>
              </div>
            </div>
            
            <div className="flex justify-center gap-6">
               <span className="text-[9px] text-kenth-subtext/40 uppercase tracking-[0.3em] font-black">AI Socratic Engine</span>
               <span className="text-[9px] text-kenth-subtext/40 uppercase tracking-[0.3em] font-black">•</span>
               <span className="text-[9px] text-kenth-subtext/40 uppercase tracking-[0.3em] font-black">Low Latency Core</span>
            </div>
          </div>
        </div>
    </div>
  );
}