import React, { useEffect, useRef, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function CheckoutSuccessView() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const hasVerifiedRef = useRef(false);

  const transactionId = searchParams.get('id');
  const clientTransactionId = searchParams.get('clientTransactionId');

  useEffect(() => {
    const confirmEnrollment = async () => {
      const id = searchParams.get('id');
      const clientTxId =
        searchParams.get('clientTransactionId') ||
        localStorage.getItem('kenth_client_tx');

      console.log("Verificando pago en backend:", {
        id,
        clientTransactionId: clientTxId
      });

      if (!id) {
        console.error("No se encontró ID de transacción para verificar.");
        setLoading(false);
        return;
      }

      if (hasVerifiedRef.current) {
        return;
      }

      hasVerifiedRef.current = true;

      try {
        const BACKEND_BASE = "http://localhost/proyecto_curso/api_persistente";
        const SYNC_URL = `${BACKEND_BASE}/api_webhook_pagos.php`;

        const response = await fetch(SYNC_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id,
            transactionId: id,
            clientTransactionId: clientTxId
          })
        });

        const data = await response.json();
        console.log("Respuesta backend:", data);

        if (data.success) {
          if (window.opener) {
            window.opener.postMessage('payphone-success', '*');
          }

          setTimeout(() => {
            setLoading(false);
            localStorage.removeItem('kenth_guest_data');
            localStorage.removeItem('kenth_client_tx');

            const token = localStorage.getItem('moodle_token');
            navigate(token ? '/dashboard' : '/login', {
              state: { message: '¡Pago verificado! Tu acceso ha sido enviado a tu correo.' }
            });
          }, 4000);
        } else {
          console.error("Error en validación backend:", data.error);
          setLoading(false);
        }

      } catch (error) {
        console.error("Error de conexión con el backend:", error);
        setLoading(false);
      }
    };

    confirmEnrollment();
  }, []);

  return (
    <div className="w-full min-h-[80vh] bg-kenth-bg text-kenth-text flex flex-col items-center justify-center p-6 overflow-hidden">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center max-w-xl relative"
      >
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-kenth-brightred/10 blur-[120px] rounded-full -z-10" />

        <div className={`w-24 h-24 ${loading ? 'bg-kenth-brightred' : 'bg-emerald-500'} rounded-[2rem] flex items-center justify-center text-white mx-auto mb-10 shadow-[0_20px_50px_rgba(16,185,129,0.3)] rotate-12 transition-colors duration-500`}>
          {loading ? (
            <div className="w-10 h-10 border-4 border-white/20 border-t-white rounded-full animate-spin" />
          ) : (
            <svg className="w-12 h-12" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          )}
        </div>

        <h1 className="text-5xl md:text-7xl font-black uppercase italic tracking-tighter mb-6 leading-none">
          {loading ? (
            <>Validando <br /><span className="text-kenth-brightred">Transacción...</span></>
          ) : (
            <>¡Transacción <br /><span className="text-emerald-500">Confirmada!</span></>
          )}
        </h1>

        <p className="text-kenth-subtext text-lg mb-12 font-medium">
          {loading
            ? "Estamos sincronizando tu pago con PayPhone para activar tu curso."
            : "Tu pago ha sido procesado con éxito. Redirigiéndote a tu aula virtual..."
          }
          <br />
          <span className="text-xs opacity-50 block mt-4 uppercase tracking-widest font-black">
            ID: {transactionId || clientTransactionId || 'Buscando...'}
          </span>
        </p>

        <div className="space-y-4">
          <p className="text-[10px] font-black uppercase tracking-[0.3em] text-kenth-brightred animate-pulse">
            {loading ? "No cierres esta ventana" : "Sincronización Exitosa"}
          </p>
          <div className="w-48 h-1 bg-kenth-border mx-auto rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: loading ? "70%" : "100%" }}
              transition={{ duration: loading ? 10 : 0.5, ease: "easeOut" }}
              className={`h-full ${loading ? 'bg-kenth-brightred' : 'bg-emerald-500'}`}
            />
          </div>
        </div>
      </motion.div>
    </div>
  );
}