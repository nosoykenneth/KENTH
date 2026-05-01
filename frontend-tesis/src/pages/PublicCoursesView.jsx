import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import logoImg from '../assets/logo-main.png';
import Logo from '../components/ui/Logo';
import { getMyCourses } from '../services/courseService';
import ThemeToggle from '../components/ui/ThemeToggle';
import Navbar from '../components/layout/Navbar';

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
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Para la vista pública, intentamos cargar los cursos. 
    // Si no hay token, usaremos una lista de fallback o un mensaje.
    const token = localStorage.getItem('moodle_token');
    const userid = localStorage.getItem('moodle_userid');

    if (token && userid) {
      getMyCourses(token, userid)
        .then(data => setCursos(data))
        .catch(() => setCursos([]))
        .finally(() => setLoading(false));
    } else {
      // Simulación de cursos para usuarios no logueados (Vista de marketing)
      setTimeout(() => {
        setCursos([
          {
            id: 'public-1',
            fullname: 'Mezcla y Masterización Profesional',
            summary: 'Domina las herramientas de la industria y eleva tu sonido al siguiente nivel.',
            img: null
          },
          {
            id: 'public-2',
            fullname: 'Producción de R&B Moderno',
            summary: 'Aprende las técnicas de composición y arreglo que definen el género hoy.',
            img: null
          }
        ]);
        setLoading(false);
      }, 800);
    }
  }, []);

  return (
    <div className="min-h-screen bg-kenth-bg text-kenth-text font-sans selection:bg-kenth-brightred selection:text-white">
      
      {/* HEADER UNIFICADO */}
      <Navbar />

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

          {/* GRID DE CURSOS */}
          <div className="w-full max-w-7xl px-6 grid grid-cols-1 md:grid-cols-2 gap-10">
            {loading ? (
               <div className="col-span-full flex justify-center py-20">
                  <div className="w-16 h-16 border-4 border-kenth-brightred/20 border-t-kenth-brightred rounded-full animate-spin"></div>
               </div>
            ) : (
              cursos.map((curso, idx) => (
                <motion.div 
                  key={curso.id}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className="group relative bg-kenth-card rounded-[2.5rem] overflow-hidden border border-kenth-border hover:border-kenth-brightred/30 transition-all duration-500 shadow-2xl"
                >
                  <div className="aspect-video bg-kenth-surface/20 relative overflow-hidden">
                    {/* Placeholder de imagen con estilo */}
                    <div className="absolute inset-0 bg-gradient-to-br from-kenth-darkred/20 to-black/60 flex items-center justify-center">
                      <span className="text-kenth-bg font-black text-9xl opacity-10 select-none italic">KENTH</span>
                    </div>
                    
                    {/* Badge de categoría */}
                    <div className="absolute top-6 left-6 bg-kenth-brightred text-white px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest shadow-lg">
                      {idx === 0 ? 'Best Seller' : 'Nuevo'}
                    </div>
                  </div>

                  <div className="p-10 flex flex-col gap-4">
                    <h3 className="text-3xl font-black uppercase tracking-tighter italic leading-none group-hover:text-kenth-brightred transition-colors">
                      {curso.fullname}
                    </h3>
                    <p className="text-kenth-subtext font-medium line-clamp-2 leading-relaxed">
                      {curso.summary || 'Aprende las bases y técnicas avanzadas para destacar en la industria musical actual.'}
                    </p>
                    
                    <div className="mt-6 flex items-center justify-between border-t border-kenth-border pt-8">
                       <div className="flex flex-col">
                          <span className="text-[10px] text-kenth-subtext font-bold uppercase tracking-widest">Inversión única</span>
                          <span className="text-2xl font-black italic text-kenth-text">$20.00</span>
                       </div>
                       <Link 
                         to={`/checkout/${curso.id}`} 
                         className="bg-kenth-text text-kenth-bg hover:bg-kenth-brightred hover:text-white px-8 py-4 rounded-2xl font-black uppercase tracking-tighter italic transition-all duration-300 shadow-xl"
                       >
                         Comprar
                       </Link>
                    </div>
                  </div>
                  
                  {/* Overlay decorativo al hover */}
                  <div className="absolute inset-0 border-2 border-kenth-brightred/0 group-hover:border-kenth-brightred/20 rounded-[2.5rem] transition-all pointer-events-none" />
                </motion.div>
              ))
            )}
          </div>
        </AnimatedSection>

        {/* CTA FINAL */}
        <AnimatedSection className="bg-gradient-to-t from-kenth-red/10 to-transparent">
           <div className="text-center">
              <h2 className="text-4xl md:text-6xl font-black mb-8 italic uppercase tracking-tighter">¿Listo para transformar <br /> tu sonido?</h2>
              <Link to="/login" className="bg-kenth-brightred hover:bg-white text-white hover:text-kenth-bg px-12 py-6 rounded-full font-black text-xl transition-all duration-500 shadow-2xl shadow-kenth-brightred/20 uppercase italic tracking-tighter inline-block">
                Comenzar ahora
              </Link>
           </div>
        </AnimatedSection>
      </main>

      <footer className="py-12 flex flex-col items-center justify-center bg-kenth-footer text-kenth-subtext text-xs md:text-sm border-t border-kenth-border">
        <p className="uppercase tracking-widest font-bold mb-4 italic">KENTH Academy &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}
