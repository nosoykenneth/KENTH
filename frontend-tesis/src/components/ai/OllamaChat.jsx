import React, { useState, useRef } from 'react';
import { askOllama } from '../../services/aiService';

export default function OllamaChat({ contextoLeccion = '' }) {
  const [pregunta, setPregunta] = useState('');
  const [cargando, setCargando] = useState(false);
  const [respuestaIA, setRespuestaIA] = useState('');
  
  // Estados para manejar la captura de pantalla y la red
  const [imagenBase64, setImagenBase64] = useState('');
  const [usarInternet, setUsarInternet] = useState(false); // <--- NUEVO ESTADO
  const fileInputRef = useRef(null);

  // Convertir imagen seleccionada a Base64
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagenBase64(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Limpiar la imagen
  const quitarImagen = () => {
    setImagenBase64('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const consultarOllama = async () => {
    // Evitamos envíos vacíos (Debe haber pregunta o imagen)
    if (!pregunta.trim() && !imagenBase64) return;
    
    setCargando(true);
    setRespuestaIA(''); 

    const miToken = localStorage.getItem('moodle_token'); 
    
    if(!miToken) {
        setRespuestaIA("NO ESTÁS LOGUEADO: Ollama Service requiere que hayas iniciado sesión en Moodle.");
        setCargando(false);
        return;
    }

    try {
      // AQUÍ ENVIAMOS EL NUEVO PARÁMETRO AL SERVICIO
      const respTeorica = await askOllama(miToken, pregunta, contextoLeccion, imagenBase64, usarInternet);
      setRespuestaIA(respTeorica);
    } catch (error) {
      console.error("Error de conexión:", error);
      setRespuestaIA(`Error al consultar Ollama: ${error.message}`);
    } finally {
      setCargando(false);
      setPregunta(''); 
      quitarImagen(); // Limpiamos la imagen tras enviar
      setUsarInternet(false); // Opcional: Apagar el botón de internet después de cada uso
    }
  };

  return (
    <div className="bg-[#2D2D30] rounded-[2rem] p-6 lg:p-8 border border-kenth-surface/20 shadow-lg relative overflow-hidden">
        <h3 className="text-xl md:text-2xl font-bold text-white mb-6 flex items-center gap-3 relative z-10">
          <svg className="w-6 h-6 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" /></svg>
          Asistente de Inteligencia Artificial
        </h3>
        
        <div className="flex flex-col gap-4 relative z-10">
          
          {/* Previsualización de la Imagen */}
          {imagenBase64 && (
            <div className="relative w-32 h-32 rounded-xl overflow-hidden border-2 border-kenth-brightred shadow-md">
              <img src={imagenBase64} alt="Captura subida" className="w-full h-full object-cover" />
              <button onClick={quitarImagen} className="absolute top-1 right-1 bg-black/70 text-white rounded-full p-1 hover:bg-red-600 transition" title="Quitar imagen">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
          )}

          <textarea 
            className="w-full bg-[#1e1e20] text-white border border-kenth-surface/30 rounded-xl p-4 focus:outline-none focus:border-kenth-brightred transition resize-none min-h-[100px] shadow-inner font-light"
            placeholder="Sube una captura de tu ecualizador/compresor o escribe tu pregunta aquí..."
            value={pregunta}
            onChange={(e) => setPregunta(e.target.value)}
          />
          
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-4">
              {/* Botón de Adjuntar Imagen */}
              <button 
                onClick={() => fileInputRef.current.click()}
                className="p-3 bg-kenth-surface/30 hover:bg-kenth-surface/50 text-white rounded-xl transition shadow-inner flex items-center justify-center border border-transparent hover:border-gray-500"
                title="Adjuntar captura de pantalla"
              >
                <svg className="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </button>
              <input type="file" ref={fileInputRef} onChange={handleImageUpload} accept="image/png, image/jpeg, image/webp" className="hidden" />

              {/* NUEVO: Toggle Switch para Buscar en Internet */}
              <label className="flex items-center gap-2 cursor-pointer text-gray-300 hover:text-white transition group" title="Buscar información actualizada en la web">
                <div className="relative">
                  <input 
                    type="checkbox" 
                    className="sr-only" 
                    checked={usarInternet}
                    onChange={() => setUsarInternet(!usarInternet)}
                  />
                  <div className={`block w-12 h-7 rounded-full transition-colors duration-300 ease-in-out ${usarInternet ? 'bg-kenth-brightred' : 'bg-gray-600'}`}></div>
                  <div className={`absolute left-1 top-1 bg-white w-5 h-5 rounded-full transition-transform duration-300 ease-in-out ${usarInternet ? 'translate-x-5' : ''}`}></div>
                </div>
                <span className="text-sm font-medium flex items-center gap-1">
                  <svg className={`w-4 h-4 ${usarInternet ? 'text-kenth-brightred' : 'text-gray-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>
                  Red Web
                </span>
              </label>
            </div>

            {/* Botón de Enviar */}
            <button 
              onClick={consultarOllama}
              disabled={cargando || (!pregunta.trim() && !imagenBase64)}
              className="bg-kenth-brightred hover:bg-kenth-red text-white py-3 px-6 rounded-xl font-bold transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed group w-fit"
            >
              {cargando ? (
                <span className="flex items-center gap-2">
                   <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                     <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                     <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                   </svg>
                   Analizando...
                </span>
              ) : (
                <>
                  <span>Enviar Consulta</span>
                  <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                </>
              )}
            </button>
          </div>
          
          {respuestaIA && (
            <div className="mt-4 p-6 bg-[#1e1e20] rounded-xl border border-kenth-surface/30 relative shadow-inner animate-in fade-in zoom-in-95 duration-300">
              <p className="text-sm text-kenth-brightred mb-3 font-bold flex items-center gap-2 uppercase tracking-wide">
                 <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                 Recomendación:
              </p>
              <div className="text-gray-200 whitespace-pre-wrap leading-relaxed font-light">{respuestaIA}</div>
            </div>
          )}
        </div>
      </div>
  );
}