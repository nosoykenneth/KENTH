import React, { useState, useRef, useEffect } from 'react';
import { askOllamaDirect } from '../../services/aiService';
import ReactMarkdown from 'react-markdown';

/**
 * TutorAssistCard
 * Versión compacta del tutor IA para embeber en módulos y lecciones.
 */
export default function TutorAssistCard({
  titulo = "Tutor IA",
  contexto = "",
  variant = "module",
  activityContext = null,
  // Mensaje proactivo opcional: si llega, se inserta como primer mensaje
  // del assistant en el historial. Pensado para "Estas en E2-L01..."
  proactiveMessage = '',
  // Sugerencias contextuales por leccion (chips). Si llegan reemplazan
  // a las acciones rapidas por variante.
  suggestedPrompts = null,
  // Badge visual opcional para mostrar la leccion activa.
  badge = null,
  // Guidance H5P nueva: { id, message }. Se agrega sin pisar el historial.
  proactiveGuidance = null,
}) {
  const [pregunta, setPregunta] = useState('');
  const [cargando, setCargando] = useState(false);
  const [historial, setHistorial] = useState(() => (
    proactiveMessage
      ? [{ role: 'assistant', content: proactiveMessage, proactive: true }]
      : []
  ));
  const chatEndRef = useRef(null);
  const proactiveIdsRef = useRef(new Set());

  const accionesPorVariante = {
    module: [
      'Resúmeme este módulo',
      'Qué debo entender sí o sí',
      'Qué error es común aquí',
      'Qué repasar antes de seguir'
    ],
    lesson: [
      'No entendí esta parte',
      'Explícamelo más simple',
      'Dame un ejemplo',
      'Hazme una pregunta rápida'
    ]
  };

  const accionesRapidas = Array.isArray(suggestedPrompts) && suggestedPrompts.length
    ? suggestedPrompts
    : (accionesPorVariante[variant] || []);

  // Si cambia el mensaje proactivo (al cambiar de leccion enlazada),
  // reinyectarlo siempre que el chat siga "limpio" (solo proactivo o
  // vacio). Asi no pisamos una conversacion ya iniciada.
  useEffect(() => {
    setHistorial((prev) => {
      const limpio = prev.length === 0 || (prev.length === 1 && prev[0].proactive);
      if (!limpio) return prev;
      return proactiveMessage
        ? [{ role: 'assistant', content: proactiveMessage, proactive: true }]
        : [];
    });
  }, [proactiveMessage]);

  useEffect(() => {
    if (!proactiveGuidance?.message || !proactiveGuidance?.id) return;
    if (proactiveIdsRef.current.has(proactiveGuidance.id)) return;
    proactiveIdsRef.current.add(proactiveGuidance.id);
    setHistorial((prev) => {
      if (prev.some((msg) => msg.proactiveId === proactiveGuidance.id)) return prev;
      return [
        ...prev,
        {
          role: 'assistant',
          content: proactiveGuidance.message,
          proactive: true,
          proactiveId: proactiveGuidance.id,
        },
      ];
    });
  }, [proactiveGuidance]);

  // Auto-scroll al final del historial
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [historial, cargando]);

  const consultarTutor = async (textoPregunta) => {
    const query = textoPregunta || pregunta;
    if (!query.trim() || cargando) return;

    const nuevoMensajeUsuario = { role: 'user', content: query };
    setHistorial(prev => [...prev, nuevoMensajeUsuario]);
    setPregunta('');
    setCargando(true);

    try {
      const data = await askOllamaDirect(
        query,
        contexto,
        '',
        false,
        '',
        historial.slice(-5),
        activityContext
      );
      setHistorial(prev => [...prev, { role: 'assistant', content: data.respuesta }]);
    } catch (error) {
      setHistorial(prev => [...prev, {
        role: 'assistant',
        content: error?.message || "No pude generar la respuesta en este momento. Intenta de nuevo.",
      }]);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="bg-kenth-card border border-kenth-border rounded-3xl p-5 flex flex-col gap-4 shadow-xl animate-in fade-in zoom-in-95 duration-300">
      {/* Cabecera */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-kenth-brightred/10 rounded-xl flex items-center justify-center border border-kenth-brightred/20 shadow-inner">
            <svg className="w-4 h-4 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-xs font-black uppercase tracking-widest text-kenth-text">{titulo}</h3>
        </div>
        <div className="flex gap-1">
          <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></div>
          <span className="text-[8px] font-black uppercase tracking-widest text-kenth-subtext">Online</span>
        </div>
      </div>

      {badge && (
        <div className="px-3 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-start gap-2">
          <span className="mt-1 w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse shrink-0"></span>
          <div className="flex-1 min-w-0">
            <p className="text-[9px] uppercase font-black tracking-widest text-emerald-300">
              {badge.label || 'Tutor contextual activo'}
            </p>
            {badge.detail && (
              <p className="text-[11px] text-emerald-100 font-bold truncate">{badge.detail}</p>
            )}
          </div>
        </div>
      )}

      {/* Historial Compacto */}
      {historial.length > 0 && (
        <div className="max-h-[300px] overflow-y-auto flex flex-col gap-3 pr-2 scrollbar-thin scrollbar-thumb-kenth-border">
          {historial.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[90%] p-3 text-[11px] leading-relaxed rounded-2xl ${
                msg.role === 'user'
                  ? 'bg-kenth-brightred text-white rounded-tr-none'
                  : msg.proactive
                    ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-50 rounded-tl-none'
                    : 'bg-kenth-surface/10 border border-kenth-border text-kenth-text rounded-tl-none'
              }`}>
                <div className="prose prose-invert prose-xs max-w-none">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              </div>
            </div>
          ))}
          {cargando && (
            <div className="flex justify-start">
              <div className="bg-kenth-surface/5 border border-kenth-border rounded-full px-4 py-2 flex items-center gap-2">
                <div className="flex gap-1">
                  <div className="w-1.5 h-1.5 bg-kenth-brightred rounded-full animate-bounce"></div>
                  <div className="w-1.5 h-1.5 bg-kenth-brightred rounded-full animate-bounce [animation-delay:0.2s]"></div>
                </div>
                <span className="text-[8px] text-kenth-subtext uppercase font-black tracking-widest italic">Pensando...</span>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
      )}

      {/* Acciones Rapidas / Sugerencias contextuales */}
      {(() => {
        // Mostrar chips si el chat aun no tiene interaccion real:
        // - vacio, o
        // - solo el mensaje proactivo inicial.
        const sinInteraccion =
          historial.length === 0 ||
          (historial.length === 1 && historial[0].proactive);
        if (!sinInteraccion || cargando || accionesRapidas.length === 0) return null;
        return (
          <div className="flex flex-wrap gap-2">
            {accionesRapidas.map((acc, idx) => (
              <button
                key={idx}
                onClick={() => consultarTutor(acc)}
                className="text-[10px] text-left px-3 py-2 rounded-full bg-kenth-surface/5 border border-kenth-border hover:border-kenth-brightred/50 hover:bg-kenth-surface/10 text-kenth-subtext hover:text-kenth-text transition-all font-medium leading-tight"
              >
                {acc}
              </button>
            ))}
          </div>
        );
      })()}

      {/* Input */}
      <div className="relative flex items-center gap-2 bg-kenth-surface/5 p-1 rounded-2xl border border-kenth-border focus-within:border-kenth-brightred/50 transition-all">
        <input
          type="text"
          className="flex-1 bg-transparent border-none focus:ring-0 text-xs text-kenth-text px-3 py-2 placeholder:text-kenth-subtext/40"
          placeholder="Hazme una pregunta..."
          value={pregunta}
          onChange={(e) => setPregunta(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && consultarTutor()}
        />
        <button
          onClick={() => consultarTutor()}
          disabled={cargando || !pregunta.trim()}
          className="p-2 bg-kenth-brightred text-white rounded-xl shadow-lg hover:scale-105 active:scale-95 transition-all disabled:opacity-30"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  );
}
