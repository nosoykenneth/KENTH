import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion'; 
import logoImg from '../assets/logo-main.png';
import Logo from '../components/ui/Logo';
import profileImg from '../assets/kenth-profile.jpg'; // Asegúrate de tener tu foto aquí
import initialImg from '../assets/initial-image.png';
import Navbar from '../components/layout/Navbar';
import { getCommercialCatalog } from '../services/courseService';

// Componente para envolver secciones con animación suave al hacer scroll
const AnimatedSection = ({ children, className }) => (
  <motion.section
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: false, amount: 0.2 }} 
    transition={{ duration: 0.8, ease: "easeOut" }}
    className={`min-h-[100dvh] w-full flex flex-col items-center justify-center snap-start border-b border-kenth-border py-28 md:py-20 ${className}`}
  >
    {children}
  </motion.section>
);

function LandingPage() {
  return (
    // Contenedor principal con el "imán" de scroll activado
    <div className="h-screen overflow-y-auto overflow-x-hidden snap-y snap-mandatory scroll-smooth bg-kenth-bg text-kenth-text font-sans">

      {/* HEADER / NAVEGACIÓN UNIFICADA */}
      <Navbar />

      <main className="w-full">

        {/* SECCIÓN 1: HERO (Llamado a la acción) */}
        <AnimatedSection className="relative overflow-hidden">
          {/* Fondo de imagen optimizado */}
          <div className="absolute inset-0 z-0">
            <img 
              src={initialImg} 
              alt="Background" 
              className="w-full h-full object-cover opacity-50 grayscale"
            />
            {/* Overlay para oscurecer y mejorar legibilidad */}
            <div className="absolute inset-0 bg-gradient-to-b from-kenth-bg via-kenth-bg/60 to-kenth-bg" />
          </div>

          <div className="text-center px-4 z-10 relative">
            <motion.p
              initial={{ letterSpacing: "0.1em" }}
              animate={{ letterSpacing: "0.4em" }}
              className="text-kenth-subtext font-black text-xs md:text-sm uppercase mb-6"
            >
              ya disponible
            </motion.p>
            <h1 className="text-5xl md:text-8xl font-black mb-6 leading-none tracking-tighter">
              CURSO DE <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-kenth-red to-kenth-brightred">
                MEZCLA Y MASTER
              </span>
            </h1>
            <p className="text-base md:text-xl text-kenth-subtext max-w-2xl mx-auto mb-12 font-medium px-4">
              Eleva tu sonido al nivel profesional. <br className="hidden md:block" />
              Sin importar si eres principiante o avanzado.
            </p>
            <Link to="/login" className="group relative bg-kenth-brightred hover:bg-white text-white hover:text-kenth-bg font-black py-4 px-10 md:px-12 rounded-full text-lg md:text-xl transition-all duration-500 shadow-2xl shadow-kenth-brightred/30 inline-block uppercase tracking-tighter italic overflow-hidden">
              <span className="relative z-10">Probar Plataforma</span>
            </Link>
          </div>

          {/* Indicador animado de scroll */}
          <div className="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce opacity-30">
            <svg className="w-6 h-6 md:w-8 md:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" /></svg>
          </div>
        </AnimatedSection>

        {/* SECCIÓN 2: SOBRE EL AUTOR (Tu perfil) */}
        <AnimatedSection className="bg-gradient-to-b from-transparent to-black/10">
          <div className="flex flex-col md:flex-row items-center justify-center px-6 md:px-10 gap-10 md:gap-24 max-w-6xl w-full">

            {/* CONTENEDOR DE LA FOTO */}
            <div className="relative group shrink-0">
              {/* Resplandor de fondo que reacciona al mouse */}
              <div className="absolute -inset-1 bg-gradient-to-r from-kenth-brightred to-kenth-red rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>

              <div className="relative w-64 h-80 md:w-96 md:h-[500px] bg-kenth-surface rounded-2xl overflow-hidden border border-kenth-border shadow-2xl">
                <img
                  src={profileImg}
                  alt="KENTH"
                  className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700 scale-105 group-hover:scale-100"
                />
                {/* Overlay sutil para oscurecer la base de la foto */}
                <div className="absolute inset-0 bg-gradient-to-t from-kenth-bg/90 via-transparent to-transparent opacity-60"></div>
              </div>
            </div>

            {/* TEXTO DE PRESENTACIÓN */}
            <div className="max-w-xl text-center md:text-left z-10">
              <motion.span
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                className="text-kenth-brightred font-black tracking-[0.3em] text-xs md:text-sm uppercase mb-4 block"
              >
                The Producer
              </motion.span>

              <h2 className="text-5xl md:text-8xl font-black mb-4 md:mb-6 text-kenth-text italic tracking-tighter">
                KENTH
              </h2>

              <p className="text-base md:text-xl text-kenth-subtext leading-relaxed font-light mb-8">
                Artista independiente, productor y compositor, KENTH utiliza el R&B y el Pop como base de una propuesta musical versátil. Especializado en perfeccionar procesos de mezcla y masterización, su enfoque busca transformar la educación musical mediante tecnología y técnica pura, logrando un sonido profesional que redefine el estándar de la producción contemporánea.
              </p>

              <div className="flex flex-col md:flex-row gap-4 md:gap-6 items-center md:items-start">
                <div className="h-1 w-16 md:w-20 bg-kenth-brightred md:mt-4"></div>
                <p className="text-xs md:text-sm text-kenth-subtext font-bold uppercase tracking-widest">
                  Quito, Ecuador <br /> Est. 2021
                </p>
              </div>
            </div>

          </div>
        </AnimatedSection>

        {/* SECCIÓN 3: FEATURES (Características del curso) */}
        <AnimatedSection>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 px-6 max-w-6xl w-full">
            {[
              { title: 'Análisis con IA', icon: '🧠', desc: 'Recibe feedback técnico instantáneo sobre tus mezclas gracias a nuestra integración exclusiva con modelos de IA.' },
              { title: 'Stems Reales', icon: '🎛️', desc: 'Practica con multipistas de producciones reales de R&B y Pop, enfrentando los retos acústicos del mundo profesional.' },
              { title: 'Técnica Pura', icon: '🎚️', desc: 'Olvídate de los "presets mágicos". Aprende el porqué detrás de cada ecualización y compresión para forjar tu propio sonido.' }
            ].map((item, idx) => (
              <div key={idx} className="p-6 md:p-8 rounded-3xl bg-kenth-card border border-kenth-border hover:border-kenth-red/50 transition-colors group">
                <div className="w-12 h-12 bg-kenth-darkred rounded-xl mb-4 md:mb-6 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">{item.icon}</div>
                <h3 className="text-xl md:text-2xl font-bold mb-3 md:mb-4">{item.title}</h3>
                <p className="text-kenth-subtext text-sm md:text-base leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </AnimatedSection>

        {/* NUEVA SECCIÓN 4: CATÁLOGO DINÁMICO (Regla 1) */}
        <LandingCoursesSection />

      </main>

      {/* FOOTER */}
      <footer className="min-h-[20vh] flex flex-col items-center justify-center snap-start bg-kenth-footer text-kenth-subtext text-xs md:text-sm border-t border-kenth-border p-8">
        <p className="uppercase tracking-widest font-bold mb-4">KENTH Academy &copy; {new Date().getFullYear()}</p>
        <div className="flex gap-6">
          <a href="#" className="hover:text-white transition">Instagram</a>
          <a href="#" className="hover:text-white transition">YouTube</a>
          <a href="#" className="hover:text-white transition">Spotify</a>
        </div>
      </footer>

    </div>
  );
}

function LandingCoursesSection() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCatalog = async () => {
      try {
        const data = await getCommercialCatalog();
        setCourses(data.slice(0, 3)); // Mostrar máximo 3 en el landing
      } catch (error) {
        console.error("Error al cargar cursos en landing:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCatalog();
  }, []);

  if (loading || courses.length === 0) return null;

  return (
    <AnimatedSection className="bg-kenth-surface/5">
      <div className="text-center mb-16">
        <span className="text-kenth-brightred font-black tracking-[0.3em] text-xs uppercase mb-4 block">Programas Disponibles</span>
        <h2 className="text-4xl md:text-6xl font-black italic tracking-tighter uppercase">Formación de <span className="text-kenth-brightred">Élite</span></h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 px-6 max-w-7xl w-full">
        {courses.map((curso, idx) => {
          const hasOffer = curso.commercial?.offer_price > 0 && curso.commercial?.offer_price < curso.commercial?.price;
          const finalPrice = hasOffer ? curso.commercial.offer_price : curso.commercial?.price;

          return (
            <motion.div 
              key={curso.id}
              whileHover={{ y: -10 }}
              className="bg-kenth-card border border-kenth-border rounded-[2rem] overflow-hidden flex flex-col group"
            >
              <div className="aspect-video bg-kenth-surface/20 flex items-center justify-center relative">
                 <span className="text-kenth-bg font-black text-6xl opacity-5 italic select-none">KENTH</span>
                 {hasOffer && (
                   <div className="absolute top-4 right-4 bg-emerald-500 text-white px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest shadow-xl">Oferta</div>
                 )}
              </div>
              <div className="p-8 flex flex-col flex-1">
                <h3 className="text-xl font-black uppercase tracking-tighter italic mb-4 group-hover:text-kenth-brightred transition-colors">{curso.fullname}</h3>
                <div className="mt-auto flex items-center justify-between pt-6 border-t border-kenth-border">
                  <div className="flex flex-col">
                    <span className="text-[9px] text-kenth-subtext font-black uppercase tracking-widest">Inversión</span>
                    <span className={`text-xl font-black italic ${hasOffer ? 'text-emerald-500' : 'text-white'}`}>${finalPrice}</span>
                  </div>
                  <Link to={`/checkout/${curso.id}`} className="bg-white text-black hover:bg-kenth-brightred hover:text-white px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-tighter italic transition-all">Comprar</Link>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
      
      <div className="mt-16">
        <Link to="/courses" className="text-kenth-subtext hover:text-white text-xs font-black uppercase tracking-[0.3em] transition-all border-b border-kenth-border hover:border-kenth-brightred pb-1">Ver Catálogo Completo</Link>
      </div>
    </AnimatedSection>
  );
}

export default LandingPage;