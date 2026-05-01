import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Navbar from '../../shared/components/layout/Navbar';

export default function CheckoutSuccessView() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  const transactionId = searchParams.get('id');
  const clientTransactionId = searchParams.get('clientTransactionId');

  useEffect(() => {
    const confirmEnrollment = async () => {
      if (!clientTransactionId && !transactionId) return;

      try {
        // Llamamos al webhook manualmente para asegurar la matrícula en entorno local
        // ya que PayPhone no puede alcanzar nuestro 'localhost' por sí solo.
        const response = await fetch(`/moodle_api/proyecto_curso/api_persistente/api_webhook_pagos.php`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            status: 'Approved',
            clientTransactionId: clientTransactionId,
            payphoneId: transactionId
          })
        });

        const data = await response.json();
        console.log("Resultado de Matrícula:", data);
        
        if (data.success) {
            // NOTIFICAMOS A LA VENTANA PRINCIPAL
            if (window.opener) {
                window.opener.postMessage('payphone-success', '*');
            }
            
            // Esperamos un segundo para que el usuario vea el check verde y cerramos
            setTimeout(() => {
                setLoading(false);
                // Si no hay opener (entró directo), redirigimos normalmente
                if (!window.opener) {
                    const token = localStorage.getItem('moodle_token');
                    navigate(token ? '/dashboard' : '/login', { 
                        state: { message: '¡Bienvenido! Tu pago fue exitoso.' } 
                    });
                }
            }, 2000);
        }

      } catch (error) {
        console.error("Error confirmando matrícula:", error);
        setLoading(false);
      }
    };

    confirmEnrollment();
  }, [transactionId, clientTransactionId, navigate]);

  return (
    <div className="min-h-screen bg-kenth-bg text-kenth-text flex flex-col items-center justify-center p-6 overflow-hidden">
      <Navbar />
      
      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center max-w-xl relative"
      >
        {/* Decoración de fondo */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-kenth-brightred/10 blur-[120px] rounded-full -z-10" />

        <div className="w-24 h-24 bg-emerald-500 rounded-[2rem] flex items-center justify-center text-white mx-auto mb-10 shadow-[0_20px_50px_rgba(16,185,129,0.3)] rotate-12">
          <svg className="w-12 h-12" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </div>

        <h1 className="text-5xl md:text-7xl font-black uppercase italic tracking-tighter mb-6 leading-none">
          ¡Transacción <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-emerald-600">Completada!</span>
        </h1>

        <p className="text-kenth-subtext text-lg mb-12 font-medium">
          Tu pago ha sido procesado por PayPhone. <br />
          ID de Transacción: <span className="text-kenth-text font-mono bg-kenth-surface/10 px-2 py-1 rounded">{transactionId || 'N/A'}</span>
        </p>

        <div className="space-y-4">
           <p className="text-xs font-black uppercase tracking-[0.3em] text-kenth-brightred animate-pulse">
             Sincronizando con tu Aula Virtual...
           </p>
           <div className="w-48 h-1 bg-kenth-border mx-auto rounded-full overflow-hidden">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: "100%" }}
                transition={{ duration: 6, ease: "linear" }}
                className="h-full bg-kenth-brightred"
              />
           </div>
        </div>
      </motion.div>
    </div>
  );
}
