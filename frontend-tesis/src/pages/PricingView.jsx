import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import logoImg from '../assets/logo-main.png';
import Logo from '../components/ui/Logo';
import ThemeToggle from '../components/ui/ThemeToggle';
import Navbar from '../components/layout/Navbar';

// Reutilizamos el componente de sección animada de la landing
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
  return (
    <div className="min-h-screen bg-kenth-bg text-kenth-text font-sans selection:bg-kenth-brightred selection:text-white">
      
      {/* HEADER UNIFICADO */}
      <Navbar />

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
            <h1 className="text-5xl md:text-8xl font-black mb-6 tracking-tighter italic">
              PLANES Y <span className="text-transparent bg-clip-text bg-gradient-to-r from-kenth-red to-kenth-brightred">PRECIOS</span>
            </h1>
            <p className="text-kenth-subtext max-w-xl mx-auto font-medium">
              Acceso ilimitado a la plataforma, feedback con IA y contenido exclusivo de por vida.
            </p>
          </div>

          {/* TARJETA DE PRECIO (Mezcla y Masterización) */}
          <div className="w-full max-w-4xl px-4 flex justify-center">
            <motion.div 
              whileHover={{ scale: 1.02 }}
              className="relative group w-full md:w-[500px]"
            >
              {/* Efecto de resplandor trasero */}
              <div className="absolute -inset-1 bg-gradient-to-r from-kenth-brightred to-kenth-red rounded-[2.5rem] blur opacity-25 group-hover:opacity-60 transition duration-1000"></div>
              
              <div className="relative bg-kenth-card border border-kenth-border p-10 md:p-14 rounded-[2.5rem] shadow-2xl flex flex-col items-center text-center">
                
                <div className="bg-kenth-brightred/10 text-kenth-brightred px-4 py-1 rounded-full text-[10px] font-black tracking-[0.2em] uppercase mb-8 border border-kenth-brightred/20">
                  Acceso Total
                </div>

                <h3 className="text-3xl font-black mb-2 uppercase italic tracking-tighter text-kenth-text">Mezcla y Masterización</h3>
                <p className="text-kenth-subtext text-sm font-medium mb-8">Domina el sonido profesional de principio a fin.</p>

                <div className="flex items-baseline gap-2 mb-10">
                  <span className="text-6xl md:text-8xl font-black text-kenth-text italic tracking-tighter">$20</span>
                  <span className="text-kenth-subtext font-bold uppercase text-xs tracking-widest">USD</span>
                </div>

                <ul className="w-full space-y-4 mb-12 text-left text-kenth-text font-medium border-t border-kenth-border pt-8">
                  <li className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                    <span>Acceso de por vida a los módulos</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                    <span>Feedback técnico con IA</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                    <span>Descarga de Stems y Multipistas</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-kenth-brightred" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                    <span>Certificado de finalización</span>
                  </li>
                </ul>

                <button className="w-full bg-white text-black hover:bg-kenth-brightred hover:text-white font-black py-5 rounded-2xl text-lg transition-all duration-500 uppercase tracking-tighter italic shadow-[0_10px_30px_rgba(0,0,0,0.5)] active:scale-95">
                  Comprar Curso Ahora
                </button>
                
                <p className="mt-6 text-[10px] text-gray-600 font-bold uppercase tracking-widest">Pago único • Sin suscripciones</p>
              </div>
            </motion.div>
          </div>
        </AnimatedSection>
      </main>

      {/* FOOTER */}
      <footer className="py-12 flex flex-col items-center justify-center bg-kenth-footer text-kenth-subtext text-xs md:text-sm border-t border-kenth-border">
        <p className="uppercase tracking-widest font-bold mb-4 italic">KENTH Academy &copy; {new Date().getFullYear()}</p>
        <div className="flex gap-8">
          <a href="#" className="hover:text-white transition">Instagram</a>
          <a href="#" className="hover:text-white transition">Discord</a>
        </div>
      </footer>
    </div>
  );
}
