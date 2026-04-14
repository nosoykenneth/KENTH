import { motion } from 'framer-motion';

export default function AnimatedSection({ children, className = '' }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: false, amount: 0.2 }}
      transition={{ duration: 0.8, ease: 'easeOut' }}
      className={`min-h-[100dvh] w-full flex flex-col items-center justify-center snap-start border-b border-kenth-surface/30 py-28 md:py-20 ${className}`}
    >
      {children}
    </motion.section>
  );
}
