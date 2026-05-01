import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * Función global para disparar notificaciones desde cualquier parte del app
 * @param {('success'|'error')} type 
 * @param {string} text 
 */
export const showNotification = (type, text) => {
  window.dispatchEvent(new CustomEvent('kenth-notification', { 
    detail: { type, text, id: Date.now() } 
  }));
};

export default function Notification() {
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    const handleNotification = (e) => {
      setNotification(e.detail);
      
      // Auto ocultar después de 5 segundos
      const timer = setTimeout(() => {
        setNotification(prev => prev?.id === e.detail.id ? null : prev);
      }, 5000);
      
      return () => clearTimeout(timer);
    };

    window.addEventListener('kenth-notification', handleNotification);
    return () => window.removeEventListener('kenth-notification', handleNotification);
  }, []);

  return (
    <AnimatePresence>
      {notification && (
        <motion.div
          key={notification.id}
          initial={{ opacity: 0, y: -40, scale: 0.9, filter: 'blur(10px)' }}
          animate={{ opacity: 1, y: 0, scale: 1, filter: 'blur(0px)' }}
          exit={{ opacity: 0, y: -20, scale: 0.95, filter: 'blur(5px)' }}
          transition={{ 
            type: "spring",
            stiffness: 400,
            damping: 30
          }}
          className="fixed top-[90px] left-1/2 -translate-x-1/2 z-[100] w-full max-w-md px-6"
        >
          <div className={`
            backdrop-blur-2xl border p-4 rounded-[1.5rem] shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)]
            flex items-center gap-4 relative overflow-hidden group
            ${notification.type === 'success' 
              ? 'bg-[#061a14] border-emerald-500/50 text-emerald-400' 
              : 'bg-[#1a0606] border-red-500/50 text-red-400'
            }
          `}>
            {/* Brillo dinámico de fondo */}
            <div className={`absolute -inset-2 opacity-20 blur-2xl transition-all duration-500 group-hover:opacity-30 ${notification.type === 'success' ? 'bg-emerald-500' : 'bg-red-500'}`}></div>

            <div className={`
              w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 shadow-lg relative z-10
              ${notification.type === 'success' ? 'bg-emerald-500/20' : 'bg-red-500/20'}
            `}>
              {notification.type === 'success' ? (
                <svg className="w-7 h-7" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
              ) : (
                <svg className="w-7 h-7" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
              )}
            </div>

            <div className="flex-1 relative z-10">
              <h4 className="text-[10px] font-black uppercase tracking-[0.2em] opacity-50 mb-0.5">
                {notification.type === 'success' ? 'Éxito' : 'Atención'}
              </h4>
              <p className="font-bold text-[13px] leading-tight tracking-tight">{notification.text}</p>
            </div>

            <button 
              onClick={() => setNotification(null)}
              className="p-2 hover:bg-white/10 rounded-xl transition-all active:scale-90 relative z-10"
            >
              <svg className="w-4 h-4 opacity-50 hover:opacity-100" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
            
            {/* Barra de progreso de auto-ocultado */}
            <motion.div 
              initial={{ width: "100%" }}
              animate={{ width: "0%" }}
              transition={{ duration: 5, ease: "linear" }}
              className={`absolute bottom-0 left-0 h-[2px] opacity-30 ${notification.type === 'success' ? 'bg-emerald-400' : 'bg-red-400'}`}
            />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
