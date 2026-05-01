import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getCommercialCatalog, updateCommercialData } from '../services/courseService';
import { showNotification } from '../components/ui/Notification';
import DashboardLayout from '../components/layout/DashboardLayout';

export default function AdminCommercialView() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(null); // ID del curso que se está guardando
  const token = localStorage.getItem('moodle_token');

  useEffect(() => {
    fetchCatalog();
  }, []);

  const fetchCatalog = async () => {
    try {
      setLoading(true);
      const data = await getCommercialCatalog(token);
      setCourses(data);
    } catch (error) {
      showNotification('error', 'No tienes permisos de administrador o hubo un error.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (id, field, value) => {
    setCourses(prev => prev.map(c => {
      if (c.id === id) {
        return {
          ...c,
          commercial: { ...c.commercial, [field]: value }
        };
      }
      return c;
    }));
  };

  const saveChanges = async (courseId) => {
    const course = courses.find(c => c.id === courseId);
    if (!course) return;

    setSaving(courseId);
    try {
      await updateCommercialData(token, courseId, course.commercial);
      showNotification('success', `Ajustes de "${course.shortname}" guardados.`);
    } catch (error) {
      showNotification('error', 'Error al guardar los cambios.');
    } finally {
      setSaving(null);
    }
  };

  return (
    <DashboardLayout>
      <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <span className="text-[10px] font-black uppercase tracking-[0.4em] text-kenth-brightred mb-4 block">Panel de Control</span>
          <h1 className="text-4xl md:text-5xl font-black uppercase tracking-tighter italic leading-none">
            Gestión <span className="text-kenth-brightred">Comercial</span>
          </h1>
          <p className="text-kenth-subtext mt-4 max-w-2xl uppercase tracking-widest text-[10px] font-bold">
            Configura los precios, ofertas y visibilidad de los cursos en el catálogo público.
          </p>
        </motion.div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-32 border border-dashed border-kenth-border rounded-[3rem] bg-kenth-surface/5">
             <div className="w-12 h-12 border-4 border-kenth-brightred/20 border-t-kenth-brightred rounded-full animate-spin mb-4"></div>
             <p className="text-[10px] font-black uppercase tracking-[0.3em] text-kenth-subtext animate-pulse">Cargando Catálogo...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {courses.map((course, index) => (
              <motion.div
                key={course.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="bg-kenth-card border border-kenth-border rounded-[2.5rem] p-6 md:p-8 flex flex-col lg:flex-row items-center gap-8 hover:border-kenth-brightred/30 transition-all group shadow-xl"
              >
                <div className="flex-1 w-full lg:w-auto">
                  <span className="text-[10px] font-black text-kenth-subtext uppercase tracking-widest block mb-1">ID: {course.id}</span>
                  <h3 className="text-xl md:text-2xl font-black uppercase tracking-tight italic group-hover:text-kenth-brightred transition-colors">
                    {course.fullname}
                  </h3>
                  <p className="text-xs text-kenth-subtext font-bold uppercase tracking-widest mt-1">{course.shortname}</p>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 items-end w-full lg:w-auto">
                  {/* PRECIO */}
                  <div className="space-y-2">
                    <label className="text-[9px] font-black uppercase tracking-widest text-kenth-subtext">Precio ($)</label>
                    <input
                      type="number"
                      step="0.01"
                      value={course.commercial.price}
                      onChange={(e) => handleInputChange(course.id, 'price', e.target.value)}
                      className="w-full bg-kenth-bg border border-kenth-border p-3 rounded-2xl outline-none focus:border-kenth-brightred transition-all font-bold text-sm"
                    />
                  </div>

                  {/* OFERTA */}
                  <div className="space-y-2">
                    <label className="text-[9px] font-black uppercase tracking-widest text-kenth-subtext">Oferta ($)</label>
                    <input
                      type="number"
                      step="0.01"
                      value={course.commercial.offer_price}
                      onChange={(e) => handleInputChange(course.id, 'offer_price', e.target.value)}
                      className="w-full bg-kenth-bg border border-kenth-border p-3 rounded-2xl outline-none focus:border-kenth-brightred transition-all font-bold text-sm text-emerald-500"
                    />
                  </div>

                  {/* VISIBILIDAD */}
                  <div className="space-y-2">
                    <label className="text-[9px] font-black uppercase tracking-widest text-kenth-subtext">Estado</label>
                    <button
                      onClick={() => handleInputChange(course.id, 'is_visible', !course.commercial.is_visible)}
                      className={`w-full p-3 rounded-2xl font-black uppercase tracking-tighter text-[10px] transition-all border h-[46px] ${
                        course.commercial.is_visible 
                        ? 'bg-emerald-500/10 border-emerald-500/50 text-emerald-500' 
                        : 'bg-kenth-subtext/10 border-kenth-border text-kenth-subtext'
                      }`}
                    >
                      {course.commercial.is_visible ? 'Visible' : 'Oculto'}
                    </button>
                  </div>

                  {/* ACCIÓN */}
                  <button
                    onClick={() => saveChanges(course.id)}
                    disabled={saving === course.id}
                    className="bg-kenth-text text-kenth-bg hover:bg-kenth-brightred hover:text-white p-3 rounded-2xl font-black uppercase tracking-tighter text-[10px] transition-all disabled:opacity-50 h-[46px] shadow-lg shadow-black/20"
                  >
                    {saving === course.id ? (
                      <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mx-auto"></div>
                    ) : 'Guardar'}
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
