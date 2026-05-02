import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { getCommercialCatalog } from '../../shared/services/courseService';

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

export default function PricingView() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCatalog = async () => {
      try {
        setLoading(true);
        const data = await getCommercialCatalog();
        setCourses(data);
      } catch (error) {
        console.error("Error al cargar precios:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCatalog();
  }, []);

  return (
    <div className="w-full bg-kenth-bg text-kenth-text font-sans selection:bg-kenth-brightred selection:text-white">
      <main className="pt-20">
        <AnimatedSection>
          <div className="text-center mb-16 px-4">
            <motion.span 
              initial={{ opacity: 0, letterSpacing: "0.2em" }}
              animate={{ opacity: 1, letterSpacing: "0.5em" }}
              className="text-kenth-brightred font-black text-xs md:text-sm uppercase mb-4 block"
            >
              inversión profesional
            </motion.span>
            <h1 className="text-5xl md:text-8xl font-black mb-6 tracking-tighter italic uppercase">
              Planes y <span className="text-transparent bg-clip-text bg-gradient-to-r from-kenth-red to-kenth-brightred">Precios</span>
            </h1>
            <p className="text-kenth-subtext max-w-xl mx-auto font-medium">
              Acceso ilimitado a la plataforma, feedback con IA y contenido exclusivo de por vida.
            </p>
          </div>

          <div className="w-full max-w-7xl px-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
            {loading ? (
               <div className="col-span-full flex justify-center py-20">
                  <div className="w-16 h-16 border-4 border-kenth-brightred/20 border-t-kenth-brightred rounded-full animate-spin"></div>
               </div>
            ) : courses.length === 0 ? (
               <div className="col-span-full text-center py-20 border border-dashed border-kenth-border rounded-3xl bg-kenth-surface/5">
                 <p className="text-kenth-subtext font-bold uppercase tracking-widest text-xs">No hay planes configurados.</p>
               </div>
            ) : (
              courses.map((curso, idx) => {
                const hasOffer = curso.commercial?.offer_price > 0 && curso.commercial?.offer_price < curso.commercial?.price;
                const finalPrice = hasOffer ? curso.commercial.offer_price : curso.commercial?.price;

                return (
                  <motion.div 
                    key={curso.id}
                    whileHover={{ y: -10 }}
                    className="relative group bg-kenth-card border border-kenth-border p-10 rounded-[2.5rem] shadow-2xl flex flex-col items-center text-center"
                  >
                    <div className="absolute -inset-0.5 bg-gradient-to-r from-kenth-brightred to-kenth-red rounded-[2.5rem] blur opacity-0 group-hover:opacity-20 transition duration-500"></div>
                    
                    <div className="relative z-10 w-full flex flex-col items-center">
                      <div className="bg-kenth-brightred/10 text-kenth-brightred px-4 py-1 rounded-full text-[9px] font-black tracking-[0.2em] uppercase mb-8 border border-kenth-brightred/20">
                        {hasOffer ? 'Descuento Activo' : 'Acceso Vitalicio'}
                      </div>

                      <h3 className="text-2xl font-black mb-2 uppercase italic tracking-tighter text-kenth-text leading-none">{curso.fullname}</h3>
                      <p className="text-kenth-subtext text-xs font-bold uppercase tracking-widest mb-10">Pago Único</p>

                      <div className="flex flex-col items-center mb-10">
                        {hasOffer && (
                          <span className="text-lg font-bold text-kenth-subtext line-through opacity-50 mb-1">
                            ${curso.commercial.price}
                          </span>
                        )}
                        <div className="flex items-baseline gap-2">
                          <span className={`text-6xl font-black italic tracking-tighter ${hasOffer ? 'text-emerald-500' : 'text-kenth-text'}`}>
                            ${finalPrice}
                          </span>
                          <span className="text-kenth-subtext font-bold uppercase text-[10px] tracking-widest">USD</span>
                        </div>
                      </div>

                      <ul className="w-full space-y-4 mb-12 text-left text-kenth-text font-medium border-t border-kenth-border pt-8 text-sm">
                        <li className="flex items-center gap-3">
                          <svg className="w-4 h-4 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                          <span>Acceso ilimitado</span>
                        </li>
                        <li className="flex items-center gap-3">
                          <svg className="w-4 h-4 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                          <span>Tutor KENTH (IA)</span>
                        </li>
                        <li className="flex items-center gap-3">
                          <svg className="w-4 h-4 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                          <span>Stems y Proyectos</span>
                        </li>
                      </ul>

                      <Link 
                        to={`/checkout/${curso.id}`}
                        className="w-full bg-white text-black hover:bg-kenth-brightred hover:text-white font-black py-4 rounded-2xl text-md transition-all duration-500 uppercase tracking-tighter italic shadow-xl active:scale-95"
                      >
                        Inscribirme Ahora
                      </Link>
                    </div>
                  </motion.div>
                );
              })
            )}
          </div>
        </AnimatedSection>
      </main>
    </div>
  );
}
