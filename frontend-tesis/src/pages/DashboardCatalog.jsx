import React, { useState, useEffect } from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';
import CourseCard from '../components/CourseCard'; 
import { getMyCourses } from '../services/courseService'; // Importamos la nueva función

export default function DashboardCatalog() {
  const [cursos, setCursos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  
  const nombreUsuario = localStorage.getItem('moodle_userfullname') || 'Productor';

  useEffect(() => {
    const cargarMisCursos = async () => {
      const token = localStorage.getItem('moodle_token');
      const userid = localStorage.getItem('moodle_userid');

      if (!token || !userid) {
        setError('No se encontraron credenciales. Por favor, vuelve a iniciar sesión.');
        setCargando(false);
        return;
      }

      try {
        const datosCursos = await getMyCourses(token, userid);
        setCursos(datosCursos);
      } catch (err) {
        setError(err.message || 'No se pudieron cargar tus cursos.');
      } finally {
        setCargando(false);
      }
    };

    cargarMisCursos();
  }, []);

  return (
    <DashboardLayout>
      <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-white uppercase drop-shadow mb-2">
          Bienvenido, <span className="text-kenth-brightred">{nombreUsuario.split(' ')[0]}</span>
        </h1>
        <p className="text-gray-400 mb-10 font-medium">Selecciona un curso para continuar con tu progreso.</p>
        
        {cargando && (
          <div className="flex justify-center items-center py-20">
            <svg className="animate-spin h-10 w-10 text-kenth-brightred" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          </div>
        )}

        {error && (
          <div className="bg-red-900/20 border-l-4 border-kenth-brightred p-6 rounded-r-xl">
             <p className="text-red-200 font-bold font-sans">Ha ocurrido un problema: {error}</p>
          </div>
        )}

        {!cargando && !error && cursos.length === 0 && (
          <div className="text-center py-20 border-2 border-dashed border-gray-700/50 rounded-3xl">
            <p className="text-gray-400 font-bold tracking-widest uppercase">No estás inscrito en ningún curso todavía.</p>
          </div>
        )}

        {!cargando && !error && cursos.length > 0 && (
          <div className="flex flex-col gap-8">
            {cursos.map((curso) => (
              <CourseCard 
                key={curso.id} 
                curso={curso} 
              />
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}