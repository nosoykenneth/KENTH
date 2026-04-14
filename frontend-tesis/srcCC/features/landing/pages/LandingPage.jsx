import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import AnimatedSection from '@/features/landing/components/AnimatedSection';
import { heroIllustration, kenthProfilePhoto, logoMain } from '@/shared/assets';

function LandingPage() {
  return (
    // snap-y snap-mandatory activa el "iman" del scroll
    <div className="h-screen overflow-y-auto overflow-x-hidden snap-y snap-mandatory scroll-smooth bg-kenth-bg text-white font-sans">

      {/* HEADER / NAVEGACIÓN - Lo hacemos fixed para que no se pierda al scrolear */}
      <header className="fixed top-0 w-full z-50 flex justify-between items-center p-6 bg-kenth-bg/80 backdrop-blur-md border-b border-kenth-surface/20">
        <div className="flex items-center">
          <img src={logoMain} alt="KENTH Logo" className="h-10 md:h-12 w-auto object-contain" />
        </div>
        <nav className="flex gap-6 font-semibold items-center text-sm md:text-base">
          <a href="#cursos" className="hover:text-kenth-brightred transition uppercase tracking-wider">cursos</a>
          <a href="#precios" className="hover:text-kenth-brightred transition uppercase tracking-wider">precios</a>
          <Link to="/login" className="bg-kenth-red hover:bg-kenth-brightred text-white px-6 py-2 rounded-full transition shadow-lg shadow-kenth-red/20 uppercase text-xs tracking-widest">
            iniciar sesion
          </Link>
        </nav>
      </header>

      <main className="w-full">

        {/* SECCIÓN 1: HERO */}
        <AnimatedSection className="relative">
          <img
            src={heroIllustration}
            alt=""
            className="absolute inset-y-0 right-0 hidden xl:block h-full object-contain opacity-10 pointer-events-none"
          />
          <div className="text-center px-4">
            <motion.p
              initial={{ letterSpacing: "0.1em" }}
              animate={{ letterSpacing: "0.4em" }}
              className="text-kenth-surface font-black text-xs md:text-sm uppercase mb-6"
            >
              ya disponible
            </motion.p>
            <h1 className="text-6xl md:text-8xl font-black mb-6 leading-none tracking-tighter">
              CURSO DE <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-kenth-red to-kenth-brightred">
                MEZCLA Y MASTER
              </span>
            </h1>
            <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-12 font-medium">
              Eleva tu sonido al nivel profesional. <br />
              Sin importar si eres principiante o avanzado.
            </p>
            <Link to="/login" className="group relative bg-kenth-brightred hover:bg-white text-white hover:text-kenth-bg font-black py-4 px-12 rounded-full text-xl transition-all duration-500 shadow-2xl shadow-kenth-brightred/30 inline-block uppercase tracking-tighter italic overflow-hidden">
              <span className="relative z-10">Probar Plataforma</span>
            </Link>
          </div>

          {/* Indicador de scroll */}
          <div className="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce opacity-20">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" /></svg>
          </div>
        </AnimatedSection>

        {/* SECCIÓN 2: SOBRE EL AUTOR */}
        <AnimatedSection className="bg-gradient-to-b from-transparent to-black/40">
          <div className="flex flex-col md:flex-row items-center justify-center px-10 gap-12 md:gap-24 max-w-6xl w-full">

            {/* CONTENEDOR DE LA FOTO */}
            <div className="relative group">
              {/* Resplandor de fondo que reacciona al mouse */}
              <div className="absolute -inset-1 bg-gradient-to-r from-kenth-brightred to-kenth-red rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>

              <div className="relative w-72 h-96 md:w-96 md:h-[500px] bg-kenth-surface rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
                {/* REEMPLAZA LA URL DE ABAJO POR TU FOTO REAL */}
                <img
                  src={kenthProfilePhoto}
                  alt="KENTH"
                  className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700 scale-105 group-hover:scale-100"
                />

                {/* Overlay sutil para que la foto no brille de más */}
                <div className="absolute inset-0 bg-gradient-to-t from-kenth-bg/80 via-transparent to-transparent opacity-60"></div>
              </div>
            </div>

            {/* TEXTO DE PRESENTACIÓN */}
            <div className="max-w-xl text-center md:text-left">
              <motion.span
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                className="text-kenth-brightred font-black tracking-[0.3em] text-sm uppercase mb-4 block"
              >
                The Producer
              </motion.span>

              <h2 className="text-6xl md:text-8xl font-black mb-6 text-white italic tracking-tighter">
                KENTH
              </h2>

              <p className="text-xl text-gray-300 leading-relaxed font-light mb-8">
                Artista independiente, productor y compositor, KENTH utiliza el R&B y el Pop como base de una propuesta musical versátil. Especializado en perfeccionar procesos de mezcla y masterización, su enfoque busca transformar la educación musical mediante tecnología y técnica pura, logrando un sonido profesional que redefine el estándar de la producción contemporánea.
              </p>

              <div className="flex flex-col md:flex-row gap-6 items-center md:items-start">
                <div className="h-1 w-20 bg-kenth-brightred mt-4"></div>
                <p className="text-sm text-kenth-surface font-bold uppercase tracking-widest">
                  Quito, Ecuador <br /> Est. 2021
                </p>
              </div>
            </div>

          </div>
        </AnimatedSection>

        {/* SECCIÓN 3: PRÓXIMAMENTE / FEATURES */}
        <AnimatedSection>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 px-6 max-w-6xl w-full">
            {['Análisis con IA', 'Stems Reales', 'Feedback 1:1'].map((item, idx) => (
              <div key={idx} className="p-8 rounded-3xl bg-white/5 border border-white/10 hover:border-kenth-red/50 transition-colors group">
                <div className="w-12 h-12 bg-kenth-darkred rounded-xl mb-6 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">⚡</div>
                <h3 className="text-2xl font-bold mb-4">{item}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">Contenido optimizado para que cada minuto de estudio se traduzca en una mejora real en tus mezclas.</p>
              </div>
            ))}
          </div>
        </AnimatedSection>

      </main>

      {/* FOOTER - Se muestra al final, snap-start también */}
      <footer className="h-[20vh] flex flex-col items-center justify-center snap-start bg-black text-gray-600 text-sm border-t border-kenth-surface/20">
        <p className="uppercase tracking-widest font-bold mb-2">KENTH courses &copy; {new Date().getFullYear()}</p>
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
