import React from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * Tarjeta de Curso Dinámica reutilizable en el Dashboard.
 * 
 * @param {Object} props
 * @param {Object} props.curso - Objeto que contiene {id, fullname, shortname} de Moodle.
 * @param {number} props.index - Para mapear gradientes cíclicos estéticos
 * @param {string} props.btnText - Texto del botón (ej: "ENTRAR")
 * @param {string} props.themeScheme - Esquema general ("emerald", "red")
 */
export default function CourseCard({ curso, index = 0, btnText = "ENTRAR", themeScheme = "red" }) {
  const navigate = useNavigate();
  // Establecemos gradientes visuales dependiendo del tema escogido para re-usar el componente
  let mapGradient = [];
  if (themeScheme === "emerald") {
    mapGradient = ["from-[#047857] to-[#064e3b]", "from-[#2A2A2D] to-[#202022]", "from-[#1a1a1c] to-[#141416]"];
  } else {
    // default (red)
    mapGradient = ["from-[#950740] to-[#6F2232]", "from-[#2A2A2D] to-[#202022]", "from-[#1a1a1c] to-[#141416]"];
  }
  
  const gradientStyle = mapGradient[index % mapGradient.length];
  
  // Color the text and icons based on theme
  const highlightColor = themeScheme === "emerald" ? "text-emerald-400" : "text-kenth-brightred";
  const hoverColorClass = themeScheme === "emerald" ? "hover:text-emerald-400" : "hover:text-kenth-brightred";

  const manejarNavegacion = () => {
     navigate(`/dashboard/course/${curso.id}`);
  };

  return (
    <div className={`bg-gradient-to-tr ${gradientStyle} rounded-[1.5rem] p-6 lg:p-8 border border-kenth-surface/50 shadow-2xl relative overflow-hidden group hover:-translate-y-2 transition-all duration-300 flex flex-col justify-between`}>
      {/* Pattern Overlay */}
      <div className="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMSIgY3k9IjEiIHI9IjEiIGZpbGw9IiNmZmYiLz48L3N2Zz4=')] mix-blend-overlay"></div>
      
      <div className="relative z-10 flex-col flex h-full">
        <div className="mb-auto">
          <p className={`${highlightColor} font-black text-xs tracking-widest uppercase mb-2`}>
             ID: {curso.id}
          </p>
          <h3 className="text-xl md:text-2xl font-bold leading-tight text-white line-clamp-2">
             {curso.fullname}
          </h3>
          {curso.shortname && (
             <p className="text-gray-400 text-sm font-medium italic mt-1 line-clamp-1">
                {curso.shortname}
             </p>
          )}
        </div>

        <div className="mt-8 flex justify-between items-center w-full">
           {themeScheme === 'red' ? (
              <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center flex-shrink-0 text-white group-hover:scale-110 transition-transform shadow-inner">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 14l9-5-9-5-9 5 9 5z" /><path strokeLinecap="round" strokeLinejoin="round" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" /><path strokeLinecap="round" strokeLinejoin="round" d="M12 14v6" /></svg>
              </div>
           ) : <div />}

          <button 
             onClick={manejarNavegacion}
             className={`text-white ${hoverColorClass} font-bold text-sm tracking-widest uppercase flex items-center gap-2 group-hover:underline transition`}
          >
             {btnText}
             <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
          </button>
        </div>
      </div>
    </div>
  );
}
