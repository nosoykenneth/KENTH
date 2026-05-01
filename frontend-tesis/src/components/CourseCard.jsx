import React from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * Tarjeta de Curso Estilo Billboard (Ancha y con Imagen de Fondo)
 * 
 * @param {Object} props
 * @param {Object} props.curso - Objeto que contiene {id, fullname, shortname, courseimage} de Moodle.
 */
export default function CourseCard({ curso }) {
  const navigate = useNavigate();
  const token = localStorage.getItem('moodle_token');
  
  // Procesar la URL de la imagen para que funcione con el token de Moodle
  let imageUrl = curso.courseimage;
  if (imageUrl && token && !imageUrl.includes('token=')) {
    imageUrl += imageUrl.includes('?') ? `&token=${token}` : `?token=${token}`;
  }

  // Extraer posición vertical si existe en el resumen
  let posY = 50;
  if (curso.summary) {
    const match = curso.summary.match(/\[kenth_pos_y:\s*(\d+)\]/);
    if (match) posY = parseInt(match[1]);
  }

  const manejarNavegacion = () => {
     navigate(`/dashboard/course/${curso.id}`);
  };

  return (
    <div 
      onClick={manejarNavegacion}
      className="group relative w-full h-64 md:h-80 rounded-[2rem] overflow-hidden border border-kenth-surface/30 cursor-pointer shadow-2xl hover:scale-[1.01] transition-all duration-500"
    >
      {/* Imagen de Fondo con Overlay */}
      {imageUrl ? (
        <img 
          src={imageUrl} 
          alt={curso.fullname} 
          style={{ objectPosition: `center ${posY}%` }}
          className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
        />
      ) : (
        <div className="absolute inset-0 bg-gradient-to-br from-kenth-bg to-kenth-surface group-hover:scale-110 transition-transform duration-700" />
      )}
      
      {/* Overlay Oscuro Gradual */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent group-hover:via-black/20 transition-all duration-500" />
      
      {/* Contenido de la Tarjeta */}
      <div className="absolute inset-0 p-8 flex flex-col justify-end">
        <div className="transform group-hover:translate-y-[-10px] transition-transform duration-500">
          <div className="flex items-center gap-3 mb-2">
            <span className="bg-kenth-brightred text-white text-[10px] font-black px-3 py-1 rounded-full tracking-widest uppercase shadow-lg">
  {curso.categoryname || 'CURSO'}
</span>
            {curso.visible === 0 && (
              <span className="bg-yellow-500 text-black text-[10px] font-black px-3 py-1 rounded-full tracking-widest uppercase">
                Oculto
              </span>
            )}
          </div>
          
          <h2 className="text-3xl md:text-5xl font-black text-white uppercase tracking-tight drop-shadow-2xl">
            {curso.fullname}
          </h2>
          
          {curso.shortname && (
            <p className="text-gray-300 text-sm md:text-lg font-medium italic mt-2 opacity-80 group-hover:opacity-100 transition-opacity">
              {curso.shortname}
            </p>
          )}
        </div>
        
        {/* Botón Flotante de Entrada */}
        <div className="mt-6 flex items-center gap-4 opacity-0 group-hover:opacity-100 translate-y-4 group-hover:translate-y-0 transition-all duration-500 delay-100">
           <button className="bg-white text-black px-8 py-3 rounded-full font-black text-xs tracking-widest uppercase flex items-center gap-3 hover:bg-kenth-brightred hover:text-white transition shadow-2xl">
             ENTRAR AL CURSO
             <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
           </button>
        </div>
      </div>

      {/* Decoración: Gradiente en el borde inferior */}
      <div className="absolute bottom-0 left-0 w-full h-1.5 bg-gradient-to-r from-transparent via-kenth-brightred to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
    </div>
  );
}
