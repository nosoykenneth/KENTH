import React from 'react';
import { useLocation, useOutlet } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '../shared/components/layout/Navbar';

export default function MarketingLayout() {
  const location = useLocation();
  const outlet = useOutlet();

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow">
        <AnimatePresence mode="wait">
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="w-full h-full"
          >
            {outlet}
          </motion.div>
        </AnimatePresence>
      </main>
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
