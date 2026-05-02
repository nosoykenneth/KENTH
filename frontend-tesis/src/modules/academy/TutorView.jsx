import React, { useState, useEffect } from 'react';
import OllamaChat from '../../shared/components/ai/OllamaChat';
import { getChatSessions, createChatSession, deleteChatSession } from '../../shared/services/aiService';
import { motion, AnimatePresence } from 'framer-motion';

export default function TutorView() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [loading, setLoading] = useState(true);

  const userId = localStorage.getItem('moodle_userid');

  useEffect(() => {
    if (userId) {
      loadSessions();
    } else {
      setLoading(false);
    }
  }, [userId]);

  const loadSessions = async () => {
    try {
      setLoading(true);
      const data = await getChatSessions(userId);
      setSessions(data);
      if (data.length > 0 && !activeSessionId) {
        setActiveSessionId(data[0].id);
      }
    } catch (error) {
      console.error("Error cargando sesiones:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = async () => {
    try {
      const newSession = await createChatSession(userId, "Nuevo Chat " + new Date().toLocaleTimeString());
      setSessions([newSession, ...sessions]);
      setActiveSessionId(newSession.id);
    } catch (error) {
      console.error("Error creando nuevo chat:", error);
    }
  };

  const handleDeleteChat = async (e, id) => {
    e.stopPropagation();
    try {
      await deleteChatSession(id);
      const newSessions = sessions.filter(s => s.id !== id);
      setSessions(newSessions);
      if (activeSessionId === id) {
        setActiveSessionId(newSessions.length > 0 ? newSessions[0].id : null);
      }
    } catch (error) {
      console.error("Error borrando chat:", error);
    }
  };

  const [generatingSessions, setGeneratingSessions] = useState(new Set());

  const setSessionLoading = (id, isLoading) => {
    setGeneratingSessions(prev => {
      const next = new Set(prev);
      if (isLoading) next.add(id);
      else next.delete(id);
      return next;
    });
  };

  return (
    <div className="h-[calc(100vh-80px)] w-full flex bg-kenth-bg overflow-hidden transition-colors">
      
      {/* SIDEBAR: SESIONES */}
      <div className="w-64 md:w-80 bg-kenth-bg border-r border-kenth-border flex flex-col z-10 shadow-2xl relative">
        <div className="p-6 border-b border-kenth-border bg-gradient-to-b from-kenth-card/10 to-transparent">
          <button 
            onClick={handleNewChat} 
            className="w-full flex items-center justify-center gap-3 bg-kenth-brightred hover:bg-red-600 text-white p-4 rounded-2xl font-black uppercase tracking-widest text-[10px] transition-all shadow-[0_10px_25px_rgba(195,7,63,0.3)] hover:-translate-y-0.5 active:translate-y-0"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" /></svg>
            Nuevo Chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3 scrollbar-none">
          <span className="text-[10px] font-black uppercase tracking-[0.3em] text-kenth-subtext/50 mb-2 px-2">Historial Reciente</span>
          
          {loading ? (
            <div className="flex flex-col gap-3 px-2">
               {[1,2,3].map(i => <div key={i} className="h-12 bg-kenth-surface/10 rounded-xl animate-pulse" />)}
            </div>
          ) : sessions.length === 0 ? (
            <div className="text-center text-kenth-subtext/40 text-[10px] mt-8 uppercase font-bold tracking-widest px-6">
              Empieza una conversación para ver tu historial.
            </div>
          ) : (
            <AnimatePresence>
              {sessions.map((session, idx) => (
                <motion.div 
                  key={session.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  onClick={() => setActiveSessionId(session.id)} 
                  className={`group relative flex items-center justify-between p-4 rounded-2xl cursor-pointer transition-all duration-300 border ${activeSessionId === session.id ? 'bg-kenth-surface/20 border-kenth-brightred/30 text-kenth-text shadow-xl' : 'border-transparent text-kenth-subtext hover:bg-kenth-surface/10 hover:text-kenth-text'}`}
                >
                  <div className="flex items-center gap-4 overflow-hidden">
                    <div className="relative">
                      <svg className={`w-5 h-5 shrink-0 transition-colors ${activeSessionId === session.id ? 'text-kenth-brightred' : 'text-kenth-subtext'}`} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
                      {generatingSessions.has(session.id) && (
                        <span className="absolute -top-1 -right-1 flex h-2 w-2">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-kenth-brightred opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-2 w-2 bg-kenth-brightred"></span>
                        </span>
                      )}
                    </div>
                    <span className="truncate text-xs font-bold uppercase tracking-tight italic">{session.title}</span>
                  </div>
                  <button 
                    onClick={(e) => handleDeleteChat(e, session.id)} 
                    className="opacity-0 group-hover:opacity-100 text-kenth-subtext hover:text-red-500 transition-all p-1 hover:scale-110"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                  </button>
                </motion.div>
              ))}
            </AnimatePresence>
          )}
        </div>
      </div>

      {/* ÁREA PRINCIPAL: CHAT */}
      <div className="flex-1 flex flex-col bg-kenth-bg relative overflow-hidden">
        
        {/* HEADER DEL TUTOR */}
        <div className="bg-kenth-bg/60 backdrop-blur-xl p-6 border-b border-kenth-border flex items-center justify-between z-20 sticky top-0 shadow-lg">
          <div className="flex items-center gap-5">
            <div className="relative">
              <div className="w-12 h-12 bg-kenth-surface/20 rounded-2xl flex items-center justify-center text-kenth-brightred border border-kenth-brightred/20 shadow-[0_0_20px_rgba(195,7,63,0.1)]">
                <svg className={`w-7 h-7 ${generatingSessions.has(activeSessionId) ? 'animate-bounce' : 'animate-pulse'}`} fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
              </div>
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 rounded-full border-4 border-kenth-bg animate-pulse"></div>
            </div>
            <div>
              <h2 className="text-xl font-black uppercase tracking-tighter italic text-kenth-text">Tutor Socrático KENTH</h2>
              <p className="text-[10px] uppercase font-black tracking-widest text-emerald-500/80 mt-1 flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                Sistemas en Línea
              </p>
            </div>
          </div>
          <div className="hidden md:flex gap-4">
             <div className="px-4 py-2 bg-kenth-surface/5 border border-kenth-border rounded-xl">
                <span className="text-[9px] font-black uppercase tracking-widest text-kenth-subtext">Modelo: Llama 3.1 • Vision</span>
             </div>
          </div>
        </div>

        <div className="flex-1 relative overflow-hidden bg-kenth-bg">
          {!userId ? (
            <div className="flex flex-col items-center justify-center h-full text-red-400 p-10 text-center gap-4">
              <svg className="w-20 h-20 opacity-30" fill="none" stroke="currentColor" strokeWidth={1} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
              <p className="font-black uppercase tracking-widest text-xs">Acceso Denegado</p>
              <p className="text-kenth-subtext text-sm">Inicia sesión en Moodle para habilitar tu asistente personal.</p>
            </div>
          ) : !activeSessionId ? (
            <div className="flex items-center justify-center h-full p-10 text-center flex-col gap-8">
              <div className="w-32 h-32 bg-kenth-surface/5 rounded-[3rem] flex items-center justify-center border border-kenth-border relative overflow-hidden">
                <div className="absolute inset-0 bg-kenth-brightred opacity-[0.02] animate-pulse"></div>
                <svg className="w-16 h-16 text-kenth-subtext/20" fill="none" stroke="currentColor" strokeWidth={1} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
              </div>
              <div className="max-w-xs">
                <h3 className="text-lg font-black uppercase tracking-tighter italic text-kenth-text mb-2">Comienza una sesión</h3>
                <p className="text-xs text-kenth-subtext font-medium leading-relaxed">
                  Selecciona una conversación del historial o crea una nueva para empezar a resolver tus dudas sobre producción.
                </p>
              </div>
            </div>
          ) : (
            <div className="absolute inset-0">
              <OllamaChat 
                sessionId={activeSessionId} 
                isExternalLoading={generatingSessions.has(activeSessionId)}
                setExternalLoading={(loading) => setSessionLoading(activeSessionId, loading)}
                contextoLeccion={JSON.stringify({ tipo: "navegacion_libre", mensaje: "El usuario está en el chat principal del tutor." })} 
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
