import React, { useState, useEffect } from 'react';

export default function ThemeToggle() {
  const [isLight, setIsLight] = useState(localStorage.getItem('kenth-theme') === 'light');

  useEffect(() => {
    if (isLight) {
      document.documentElement.classList.add('light');
      localStorage.setItem('kenth-theme', 'light');
    } else {
      document.documentElement.classList.remove('light');
      localStorage.setItem('kenth-theme', 'dark');
    }
  }, [isLight]);

  return (
    <button 
      onClick={() => setIsLight(!isLight)}
      className="p-2 rounded-xl bg-kenth-surface/20 hover:bg-kenth-surface/40 border border-white/10 transition-all flex items-center justify-center group"
      title={isLight ? 'Activar Modo Oscuro' : 'Activar Modo Claro'}
    >
      {isLight ? (
        <svg className="w-5 h-5 text-kenth-brightred group-hover:rotate-45 transition-transform duration-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      ) : (
        <svg className="w-5 h-5 text-amber-400 group-hover:rotate-90 transition-transform duration-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707M6.343 6.343l-.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
        </svg>
      )}
    </button>
  );
}
