import React, { useState, useEffect } from 'react';
import OllamaChat from '../../shared/components/ai/OllamaChat';
import { getChatSessions, createChatSession, deleteChatSession } from '../../shared/services/aiService';

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

  return (
    <div className="h-[calc(100vh-80px)] w-full flex bg-kenth-bg overflow-hidden transition-colors">
      <div className="w-64 md:w-80 bg-kenth-card border-r border-kenth-border flex flex-col">
        <div className="p-4 border-b border-kenth-border">
          <button onClick={handleNewChat} className="w-full flex items-center justify-center gap-2 bg-kenth-brightred hover:bg-red-600 text-white p-3 rounded-xl font-bold transition shadow-lg">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" /></svg>
            Nuevo Chat
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-3 flex flex-col gap-2 scrollbar-thin">
          {loading ? (
            <div className="text-center text-kenth-subtext text-sm mt-4">Cargando chats...</div>
          ) : sessions.length === 0 ? (
            <div className="text-center text-kenth-subtext text-sm mt-4 italic">No hay historial de chats. Crea uno nuevo.</div>
          ) : (
            sessions.map(session => (
              <div key={session.id} onClick={() => setActiveSessionId(session.id)} className={`group relative flex items-center justify-between p-3 rounded-xl cursor-pointer transition ${activeSessionId === session.id ? 'bg-kenth-surface/30 text-kenth-text shadow-inner' : 'text-kenth-subtext hover:bg-kenth-surface/10 hover:text-kenth-text'}`}>
                <div className="flex items-center gap-3 overflow-hidden">
                  <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
                  <span className="truncate text-sm font-medium">{session.title}</span>
                </div>
                <button onClick={(e) => handleDeleteChat(e, session.id)} className="opacity-0 group-hover:opacity-100 text-kenth-subtext hover:text-red-500 transition p-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
              </div>
            ))
          )}
        </div>
      </div>
      <div className="flex-1 flex flex-col bg-kenth-bg relative">
        <div className="bg-kenth-card/50 p-4 border-b border-kenth-border flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center text-blue-400">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>
            <div>
              <h2 className="text-lg font-bold text-kenth-text leading-none">Tutor Socrático KENTH</h2>
              <p className="text-xs text-kenth-subtext mt-1">Conectado y listo para ayudar</p>
            </div>
          </div>
        </div>
        <div className="flex-1 relative">
          {!userId ? (
            <div className="flex items-center justify-center h-full text-red-400 p-8 text-center">Inicia sesión en Moodle para usar el Tutor KENTH.</div>
          ) : !activeSessionId ? (
            <div className="flex items-center justify-center h-full text-kenth-subtext p-8 text-center flex-col gap-4">
              <svg className="w-16 h-16 opacity-50" fill="none" stroke="currentColor" strokeWidth={1} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
              <p>Selecciona un chat del panel lateral o crea uno nuevo para empezar.</p>
            </div>
          ) : (
            <div className="absolute inset-0 p-4 sm:p-6 overflow-y-auto">
              <OllamaChat sessionId={activeSessionId} contextoLeccion={JSON.stringify({ tipo: "navegacion_libre", mensaje: "El usuario está en el chat principal del tutor." })} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
