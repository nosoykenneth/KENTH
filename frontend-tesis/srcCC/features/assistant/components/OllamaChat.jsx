import React, { useState } from 'react';
import { askOllama } from '../../services/aiService';
import { getMoodleToken } from '@/shared/lib/moodleSession';

export default function OllamaChat() {
  const [pregunta, setPregunta] = useState('');
  const [cargando, setCargando] = useState(false);
  const [respuestaIA, setRespuestaIA] = useState('');

  const consultarOllama = async () => {
    if (!pregunta.trim()) return;
    
    setCargando(true);
    setRespuestaIA(''); 

    const miToken = localStorage.getItem('moodle_token'); 
    
    // Si no hay token de moodle lo indicamos, este modulo requiere el servidor vivo
    if(!miToken) {
        setRespuestaIA("NO ESTÁS LOGUEADO: Ollama Service requiere que hayas iniciado sesión en Moodle.");
        setCargando(false);
        return;
    }

    try {
      const respTeorica = await askOllama(miToken, pregunta);
      setRespuestaIA(respTeorica);
    } catch (error) {
      console.error("Error de conexión:", error);
      setRespuestaIA(`Error al consultar Ollama: ${error.message}`);
    } finally {
      setCargando(false);
      setPregunta(''); 
    }
  };

  return (
    <div className="bg-[#2D2D30] rounded-[2rem] p-6 lg:p-8 border border-kenth-surface/20 shadow-lg relative overflow-hidden">
        <h3 className="text-xl md:text-2xl font-bold text-white mb-6 flex items-center gap-3 relative z-10">
          <svg className="w-6 h-6 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" /></svg>
          Asistente de Inteligencia Artificial (Ollama)
        </h3>
        
        <div className="flex flex-col gap-4 relative z-10">
          <textarea 
            className="w-full bg-[#1e1e20] text-white border border-kenth-surface/30 rounded-xl p-4 focus:outline-none focus:border-kenth-brightred transition resize-none min-h-[100px] shadow-inner font-light"
            placeholder="Escribe tu pregunta sobre cualquier curso aquí..."
            value={pregunta}
            onChange={(e) => setPregunta(e.target.value)}
          />
          
          <button 
            onClick={consultarOllama}
            disabled={cargando || !pregunta.trim()}
            className="bg-kenth-brightred hover:bg-kenth-red text-white py-3 px-6 rounded-xl font-bold transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed group w-fit"
          >
            {cargando ? (
              <span className="flex items-center gap-2">
                 <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                   <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                   <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                 </svg>
                 Consultando a la IA...
              </span>
            ) : (
              <>
                <span>Enviar Pregunta</span>
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
              </>
            )}
          </button>
          
          {respuestaIA && (
            <div className="mt-4 p-6 bg-[#1e1e20] rounded-xl border border-kenth-surface/30 relative shadow-inner">
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
