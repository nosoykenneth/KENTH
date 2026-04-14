import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion'; 
import logoImg from '../assets/logo-main.png';
import profileImg from '../assets/kenth-profile.jpg'; // Asegúrate de tener tu foto aquí

// Componente para envolver secciones con animación suave al hacer scroll
const AnimatedSection = ({ children, className }) => (
  <motion.section
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: false, amount: 0.2 }} 
    transition={{ duration: 0.8, ease: "easeOut" }}
    className={`min-h-[100dvh] w-full flex flex-col items-center justify-center snap-start border-b border-kenth-surface/30 py-28 md:py-20 ${className}`}
  >
    {children}
  </motion.section>
);

function LandingPage() {
  return (
    // Contenedor principal con el "imán" de scroll activado
    <div className="h-screen overflow-y-auto overflow-x-hidden snap-y snap-mandatory scroll-smooth bg-kenth-bg text-white font-sans">

      {/* HEADER / NAVEGACIÓN (Fijo en la parte superior) */}
      <header className="fixed top-0 w-full z-50 flex justify-between items-center p-4 md:p-6 bg-kenth-bg/80 backdrop-blur-md border-b border-kenth-surface/20">
        <div className="flex items-center">
          <img src={logoImg} alt="KENTH Logo" className="h-8 md:h-12 w-auto object-contain" />
        </div>
        <nav className="flex gap-4 md:gap-6 font-semibold items-center text-xs md:text-base">
          <a href="#cursos" className="hidden sm:block hover:text-kenth-brightred transition uppercase tracking-wider">cursos</a>
          <a href="#precios" className="hidden sm:block hover:text-kenth-brightred transition uppercase tracking-wider">precios</a>
          <Link to="/login" className="bg-kenth-red hover:bg-kenth-brightred text-white px-5 py-2 md:px-6 md:py-2 rounded-full transition shadow-lg shadow-kenth-red/20 uppercase text-[10px] md:text-xs tracking-widest">
            iniciar sesion
          </Link>
        </nav>
      </header>

      <main className="w-full">

        {/* SECCIÓN 1: HERO (Llamado a la acción) */}
        <AnimatedSection className="relative">
          <div className="text-center px-4 z-10">
            <motion.p
              initial={{ letterSpacing: "0.1em" }}
              animate={{ letterSpacing: "0.4em" }}
              className="text-kenth-surface font-black text-xs md:text-sm uppercase mb-6"
            >
              ya disponible
            </motion.p>
            <h1 className="text-5xl md:text-8xl font-black mb-6 leading-none tracking-tighter">
              CURSO DE <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-kenth-red to-kenth-brightred">
                MEZCLA Y MASTER
              </span>
            </h1>
            <p className="text-base md:text-xl text-gray-400 max-w-2xl mx-auto mb-12 font-medium px-4">
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
        <AnimatedSection className="bg-gradient-to-b from-transparent to-black/40">
          <div className="flex flex-col md:flex-row items-center justify-center px-6 md:px-10 gap-10 md:gap-24 max-w-6xl w-full">

            {/* CONTENEDOR DE LA FOTO */}
            <div className="relative group shrink-0">
              {/* Resplandor de fondo que reacciona al mouse */}
              <div className="absolute -inset-1 bg-gradient-to-r from-kenth-brightred to-kenth-red rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>

              <div className="relative w-64 h-80 md:w-96 md:h-[500px] bg-kenth-surface rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
                <img
                  src={profileImg}
                  alt="KENTH"
                  className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700 scale-105 group-hover:scale-100"
                />
                {/* Overlay sutil para oscurecer la base de la foto */}
                <div className="absolute inset-0 bg-gradient-to-t from-kenth-bg/90 via-transparent to-transparent opacity-80"></div>
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

              <h2 className="text-5xl md:text-8xl font-black mb-4 md:mb-6 text-white italic tracking-tighter">
                KENTH
              </h2>

              <p className="text-base md:text-xl text-gray-300 leading-relaxed font-light mb-8">
                Artista independiente, productor y compositor, KENTH utiliza el R&B y el Pop como base de una propuesta musical versátil. Especializado en perfeccionar procesos de mezcla y masterización, su enfoque busca transformar la educación musical mediante tecnología y técnica pura, logrando un sonido profesional que redefine el estándar de la producción contemporánea.
              </p>

              <div className="flex flex-col md:flex-row gap-4 md:gap-6 items-center md:items-start">
                <div className="h-1 w-16 md:w-20 bg-kenth-brightred md:mt-4"></div>
                <p className="text-xs md:text-sm text-kenth-surface font-bold uppercase tracking-widest">
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
              <div key={idx} className="p-6 md:p-8 rounded-3xl bg-white/5 border border-white/10 hover:border-kenth-red/50 transition-colors group">
                <div className="w-12 h-12 bg-kenth-darkred rounded-xl mb-4 md:mb-6 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">{item.icon}</div>
                <h3 className="text-xl md:text-2xl font-bold mb-3 md:mb-4">{item.title}</h3>
                <p className="text-gray-400 text-sm md:text-base leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </AnimatedSection>

      </main>

      {/* FOOTER */}
      <footer className="min-h-[20vh] flex flex-col items-center justify-center snap-start bg-black text-gray-600 text-xs md:text-sm border-t border-kenth-surface/20 p-8">
        <p className="uppercase tracking-widest font-bold mb-4">KENTH courses &copy; {new Date().getFullYear()}</p>
        <div className="flex gap-6">
          <a href="#" className="hover:text-white transition">Instagram</a>
          <a href="#" className="hover:text-white transition">YouTube</a>
          <a href="#" className="hover:text-white transition">Spotify</a>
        </div>
      </footer>

    </div>
  );
}

export default LandingPage;