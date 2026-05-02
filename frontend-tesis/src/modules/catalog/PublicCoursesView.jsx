import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { getCommercialCatalog, getMyCourses } from '../../shared/services/courseService';

const AnimatedSection = ({ children, className }) => (
  <motion.section
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: false, amount: 0.2 }}
    transition={{ duration: 0.8, ease: "easeOut" }}
    className={`min-h-[90vh] w-full flex flex-col items-center justify-center py-20 ${className}`}
  >
    {children}
  </motion.section>
);

export default function PublicCoursesView() {
  const [cursos, setCursos] = useState([]);
  const [userCourses, setUserCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem('moodle_token');

  useEffect(() => {
    const fetchCatalogAndUserCourses = async () => {
      try {
        setLoading(true);
        // Cargar catálogo público
        const data = await getCommercialCatalog();
        setCursos(data);

        // Si hay token, cargar cursos del usuario para validar posesión
        if (token) {
          try {
            const misCursos = await getMyCourses(token);
            setUserCourses(misCursos);
          } catch (e) {
            console.error("Error al cargar cursos del usuario:", e);
          }
        }
      } catch (error) {
        console.error("Error al cargar catálogo público:", error);
        setCursos([]);
      } finally {
        setLoading(false);
      }
    };
    fetchCatalogAndUserCourses();
  }, [token]);

  return (
    <div className="w-full bg-kenth-bg text-kenth-text font-sans selection:bg-kenth-brightred selection:text-white">
      <main className="pt-20">
        <AnimatedSection>
          <div className="text-center mb-16 px-4">
            <motion.span 
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-kenth-brightred font-black text-xs md:text-sm uppercase mb-4 block tracking-[0.4em]"
            >
              academy catalog
            </motion.span>
            <h1 className="text-5xl md:text-8xl font-black mb-6 tracking-tighter italic uppercase">
              Explora nuestros <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-kenth-red to-kenth-brightred">programas</span>
            </h1>
            <p className="text-kenth-subtext max-w-2xl mx-auto font-medium text-lg">
              Cursos diseñados para artistas independientes que buscan autonomía técnica y excelencia sonora.
            </p>
          </div>

          <div className="w-full max-w-7xl px-6 grid grid-cols-1 md:grid-cols-2 gap-10">
            {loading ? (
               <div className="col-span-full flex justify-center py-20">
                  <div className="w-16 h-16 border-4 border-kenth-brightred/20 border-t-kenth-brightred rounded-full animate-spin"></div>
               </div>
            ) : cursos.length === 0 ? (
               <div className="col-span-full text-center py-20 border border-dashed border-kenth-border rounded-3xl bg-kenth-surface/5">
                 <p className="text-kenth-subtext font-bold uppercase tracking-widest text-xs">No hay programas disponibles en este momento.</p>
               </div>
            ) : (
              cursos.map((curso, idx) => {
                const hasOffer = curso.commercial?.offer_price > 0 && curso.commercial?.offer_price < curso.commercial?.price;
                const finalPrice = hasOffer ? curso.commercial.offer_price : curso.commercial?.price;
                
                // Validar si el usuario ya tiene este curso
                // Ambos IDs (uc.id y curso.id) son ahora IDs firmados por el backend
                const yaLoTiene = userCourses.some(uc => String(uc.id) === String(curso.id));

                return (
                  <motion.div 
                    key={curso.id}
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className="group relative bg-kenth-card rounded-[2.5rem] overflow-hidden border border-kenth-border hover:border-kenth-brightred/30 transition-all duration-500 shadow-2xl"
                  >
                    <div className="aspect-video bg-kenth-surface/20 relative overflow-hidden">
                      <div className="absolute inset-0 bg-gradient-to-br from-kenth-darkred/20 to-black/60 flex items-center justify-center">
                        <span className="text-kenth-bg font-black text-9xl opacity-10 select-none italic">KENTH</span>
                      </div>
                      <div className="absolute top-6 left-6 bg-kenth-brightred text-white px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest shadow-lg">
                        {yaLoTiene ? 'Adquirido' : (hasOffer ? 'Oferta Especial' : (idx === 0 ? 'Best Seller' : 'Academy'))}
                      </div>
                    </div>

                    <div className="p-10 flex flex-col gap-4">
                      <h3 className="text-3xl font-black uppercase tracking-tighter italic leading-none group-hover:text-kenth-brightred transition-colors">
                        {curso.fullname}
                      </h3>
                      <p className="text-kenth-subtext font-medium line-clamp-2 leading-relaxed">
                        {curso.commercial?.summary || 'Domina las herramientas de la industria y eleva tu sonido al siguiente nivel.'}
                      </p>
                      <div className="mt-6 flex items-center justify-between border-t border-kenth-border pt-8">
                         <div className="flex flex-col">
                            <span className="text-[10px] text-kenth-subtext font-bold uppercase tracking-widest">Inversión única</span>
                            <div className="flex items-center gap-2">
                              {yaLoTiene ? (
                                <span className="text-emerald-500 font-black italic text-xl">PROPIEDAD</span>
                              ) : (
                                <>
                                  {hasOffer && (
                                    <span className="text-sm font-bold text-kenth-subtext line-through opacity-50">
                                      ${curso.commercial.price}
                                    </span>
                                  )}
                                  <span className={`text-2xl font-black italic ${hasOffer ? 'text-emerald-500' : 'text-kenth-text'}`}>
                                    ${finalPrice}
                                  </span>
                                </>
                              )}
                            </div>
                         </div>
                         
                         {yaLoTiene ? (
                           <Link 
                            to={`/dashboard/course/${curso.id}`} 
                            className="bg-emerald-600 text-white hover:bg-emerald-500 px-8 py-4 rounded-2xl font-black uppercase tracking-tighter italic transition-all duration-300 shadow-xl flex items-center gap-2"
                           >
                             <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" /><path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                             Entrar
                           </Link>
                         ) : (
                           <Link 
                             to={`/checkout/${curso.id}`} 
                             className="bg-kenth-text text-kenth-bg hover:bg-kenth-brightred hover:text-white px-8 py-4 rounded-2xl font-black uppercase tracking-tighter italic transition-all duration-300 shadow-xl"
                           >
                             Comprar
                           </Link>
                         )}
                      </div>
                    </div>
                    <div className="absolute inset-0 border-2 border-kenth-brightred/0 group-hover:border-kenth-brightred/20 rounded-[2.5rem] transition-all pointer-events-none" />
                  </motion.div>
                );
              })
            )}
          </div>
        </AnimatedSection>

        <AnimatedSection className="bg-gradient-to-t from-kenth-red/10 to-transparent">
           <div className="text-center">
              <h2 className="text-4xl md:text-6xl font-black mb-8 italic uppercase tracking-tighter">¿Listo para transformar <br /> tu sonido?</h2>
              <Link to={token ? "/dashboard" : "/login"} className="bg-kenth-brightred hover:bg-white text-white hover:text-kenth-bg px-12 py-6 rounded-full font-black text-xl transition-all duration-500 shadow-2xl shadow-kenth-brightred/20 uppercase italic tracking-tighter inline-block">
                {token ? 'Ir a mi estudio' : 'Comenzar ahora'}
              </Link>
           </div>
        </AnimatedSection>
      </main>
    </div>
  );
}
