import React, { useState, useRef, useEffect } from 'react';
import { askOllamaDirect, getChatMessages } from '../../services/aiService';

export default function OllamaChat({ contextoLeccion = '', sessionId = null }) {
  const [pregunta, setPregunta] = useState('');
  const [cargando, setCargando] = useState(false);
  const [historial, setHistorial] = useState([]); 
  const [imagenBase64, setImagenBase64] = useState('');
  const [usarInternet, setUsarInternet] = useState(false);
  
  const fileInputRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Cargar historial de la base de datos si hay un sessionId
  useEffect(() => {
    if (sessionId) {
      const loadHistory = async () => {
        try {
          setCargando(true);
          const messages = await getChatMessages(sessionId);
          setHistorial(messages);
        } catch (error) {
          console.error("Error al cargar historial:", error);
        } finally {
          setCargando(false);
        }
      };
      loadHistory();
    } else {
      setHistorial([]);
    }
  }, [sessionId]);

  // Auto-scroll
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [historial, cargando]);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImagenBase64(reader.result);
      reader.readAsDataURL(file);
    }
  };

  const quitarImagen = () => {
    setImagenBase64('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const consultarOllama = async () => {
    if (!pregunta.trim() && !imagenBase64) return;
    
    // Guardar temporalmente en UI
    const nuevoMensajeUsuario = { role: 'user', content: pregunta, image: imagenBase64 };
    setHistorial(prev => [...prev, nuevoMensajeUsuario]);
    
    setCargando(true);
    const preguntaEnviada = pregunta;
    const imagenEnviada = imagenBase64;
    
    setPregunta(''); 
    quitarImagen();

    try {
      // Usar el nuevo servicio directo que soporta session_id
      const data = await askOllamaDirect(
        preguntaEnviada, 
        contextoLeccion, 
        imagenEnviada, 
        usarInternet, 
        sessionId
      );
      
      setHistorial(prev => [...prev, { role: 'assistant', content: data.respuesta }]);
    } catch (error) {
      console.error("Error de conexión:", error);
      setHistorial(prev => [...prev, { role: 'assistant', content: `Error: ${error.message}` }]);
    } finally {
      setCargando(false);
      setUsarInternet(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full">
        
        {/* Historial con Scroll */}
        <div 
          ref={chatContainerRef} 
          className="flex-1 overflow-y-auto p-4 flex flex-col gap-6 scrollbar-thin scrollbar-thumb-kenth-surface scrollbar-track-transparent"
        >
          {historial.length === 0 && !cargando && (
            <div className="flex flex-col items-center justify-center h-full text-center text-kenth-subtext gap-4 animate-in fade-in duration-700">
               <div className="w-20 h-20 bg-kenth-surface/20 rounded-full flex items-center justify-center">
                 <svg className="w-10 h-10 text-kenth-brightred/40" fill="none" stroke="currentColor" strokeWidth={1} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
               </div>
               <p className="max-w-xs italic">Hola, soy KENTH. ¿En qué módulo de audio estamos trabajando hoy? Pregúntame lo que necesites.</p>
            </div>
          )}
          
          {historial.map((msg, index) => (
            <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 duration-300`}>
              <div className={`flex flex-col gap-2 max-w-[85%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`rounded-2xl p-4 shadow-lg ${
                  msg.role === 'user' 
                    ? 'bg-kenth-brightred text-white rounded-br-sm shadow-kenth-brightred/20' 
                    : 'bg-kenth-card border border-kenth-border text-kenth-text rounded-bl-sm'
                }`}>
                  {msg.role === 'assistant' && (
                    <div className="flex items-center gap-2 mb-2 text-kenth-brightred text-[10px] font-bold uppercase tracking-tighter">
                      <div className="w-5 h-5 bg-kenth-brightred/20 rounded-full flex items-center justify-center">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                      </div>
                      Tutor KENTH
                    </div>
                  )}
                  {msg.image && (
                    <img src={msg.image} alt="Adjunto" className="w-full max-w-[300px] h-auto rounded-lg mb-3 border border-kenth-surface/50" />
                  )}
                  <div className="text-sm leading-relaxed whitespace-pre-wrap font-light tracking-wide">
                    {msg.content}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {cargando && (
            <div className="flex justify-start">
              <div className="bg-kenth-surface/20 border border-kenth-surface/30 rounded-2xl rounded-bl-sm p-4 flex items-center gap-3">
                 <div className="flex gap-1">
                   <div className="w-2 h-2 bg-kenth-brightred rounded-full animate-bounce"></div>
                   <div className="w-2 h-2 bg-kenth-brightred rounded-full animate-bounce [animation-delay:0.2s]"></div>
                   <div className="w-2 h-2 bg-kenth-brightred rounded-full animate-bounce [animation-delay:0.4s]"></div>
                 </div>
                 <span className="text-xs text-kenth-subtext italic font-medium">Analizando contexto socrático...</span>
              </div>
            </div>
          )}
        </div>

        {/* Área de Input Flotante estilo WhatsApp/ChatGPT */}
        <div className="p-4 bg-transparent border-t border-kenth-border">
          <div className="w-full flex flex-col gap-3">
            
            {/* Previsualización Imagen */}
            {imagenBase64 && (
              <div className="relative w-20 h-20 rounded-xl overflow-hidden border-2 border-kenth-brightred shadow-xl animate-in zoom-in duration-200">
                <img src={imagenBase64} alt="Preview" className="w-full h-full object-cover" />
                <button onClick={quitarImagen} className="absolute top-1 right-1 bg-black/60 text-white rounded-full p-1 hover:bg-red-600">
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>
            )}

            <div className="flex items-end gap-3 bg-kenth-card p-2 rounded-[1.5rem] border border-kenth-border shadow-inner focus-within:border-kenth-brightred/50 transition-all">
              <button 
                onClick={() => fileInputRef.current.click()}
                className="p-3 text-kenth-subtext hover:text-kenth-text transition rounded-full hover:bg-kenth-surface/10"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" /></svg>
              </button>
              <input type="file" ref={fileInputRef} onChange={handleImageUpload} accept="image/*" className="hidden" />
              
              <textarea 
                className="flex-1 bg-transparent text-kenth-text border-none focus:ring-0 p-2 text-sm max-h-32 resize-none scrollbar-none"
                placeholder="Pregunta algo sobre tu mezcla..."
                value={pregunta}
                onChange={(e) => setPregunta(e.target.value)}
                rows={1}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    consultarOllama();
                  }
                }}
              />

              <button 
                onClick={() => setUsarInternet(!usarInternet)}
                className={`p-3 transition rounded-full ${usarInternet ? 'text-kenth-brightred bg-kenth-brightred/10' : 'text-kenth-subtext hover:text-kenth-text'}`}
                title="Buscar en la web"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>
              </button>

              <button 
                onClick={consultarOllama}
                disabled={cargando || (!pregunta.trim() && !imagenBase64)}
                className="p-3 bg-kenth-brightred text-white rounded-full shadow-lg hover:scale-105 active:scale-95 transition disabled:opacity-20 disabled:grayscale disabled:scale-100"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" /></svg>
              </button>
            </div>
            <p className="text-[10px] text-kenth-subtext/40 text-center uppercase tracking-widest font-bold">Tutor Socrático KENTH v1.0 • Impulsado por Ollama</p>
          </div>
        </div>
    </div>
  );
}