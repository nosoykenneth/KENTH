import React, { useEffect, useRef, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function CheckoutSuccessView() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [phase, setPhase] = useState('verifying'); // verifying | confirmed | error
  const [message, setMessage] = useState('');
  const hasVerifiedRef = useRef(false);

  const transactionId = searchParams.get('id');
  const clientTransactionId = searchParams.get('clientTransactionId');

  useEffect(() => {
    const confirmEnrollment = async () => {
      const id = searchParams.get('id');
      const clientTxId =
        searchParams.get('clientTransactionId') ||
        localStorage.getItem('kenth_client_tx');

      if (!id) {
        setPhase('error');
        setMessage('No se encontró el ID de la transacción.');
        return;
      }

      if (hasVerifiedRef.current) return;
      hasVerifiedRef.current = true;

      const verificationKey = `kenth_verified_${clientTxId || id}`;
      if (sessionStorage.getItem(verificationKey) === '1') {
        setPhase('confirmed');
        setMessage('Esta transacción ya fue validada en esta sesión.');
        setTimeout(() => {
          const token = localStorage.getItem('moodle_token');
          navigate(token ? '/dashboard' : '/login', { replace: true });
        }, 3000);
        return;
      }

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

        if (!data.success) {
          setPhase('error');
          setMessage(data.error || 'No se pudo validar la transacción.');
          return;
        }

        if (window.opener) {
          window.opener.postMessage('payphone-success', '*');
        }

        localStorage.removeItem('kenth_guest_data');
        localStorage.removeItem('kenth_client_tx');

        setPhase('confirmed');
        setMessage(
          data.alreadyProcessed
            ? 'Esta transacción ya había sido procesada. Tu acceso sigue activo.'
            : 'Tu pago ha sido procesado con éxito. Hemos preparado tu acceso.'
        );

        sessionStorage.setItem(verificationKey, '1');

        // Mostrar la pantalla confirmada un rato real
        setTimeout(() => {
          const token = localStorage.getItem('moodle_token');
          navigate(token ? '/dashboard' : '/login', {
            replace: true,
            state: {
              message: data.alreadyProcessed
                ? 'Tu pago ya estaba verificado previamente.'
                : '¡Pago verificado! Tu acceso ha sido enviado a tu correo.'
            }
          });
        }, 6000);

      } catch (error) {
        console.error("Error de conexión con el backend:", error);
        setPhase('error');
        setMessage('Hubo un problema al conectar con el servidor.');
      }
    };

    confirmEnrollment();
  }, [navigate, searchParams]);

  const isVerifying = phase === 'verifying';
  const isConfirmed = phase === 'confirmed';

  return (
    <div className="w-full min-h-[80vh] bg-kenth-bg text-kenth-text flex flex-col items-center justify-center p-6 overflow-hidden">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center max-w-xl relative"
      >
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-kenth-brightred/10 blur-[120px] rounded-full -z-10" />

        <div className={`w-24 h-24 ${isVerifying ? 'bg-kenth-brightred' : isConfirmed ? 'bg-emerald-500' : 'bg-yellow-500'
          } rounded-[2rem] flex items-center justify-center text-white mx-auto mb-10 shadow-[0_20px_50px_rgba(16,185,129,0.3)] rotate-12 transition-colors duration-500`}>
          {isVerifying ? (
            <div className="w-10 h-10 border-4 border-white/20 border-t-white rounded-full animate-spin" />
          ) : isConfirmed ? (
            <svg className="w-12 h-12" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          ) : (
            <svg className="w-12 h-12" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M10.29 3.86l-7.5 13A2 2 0 004.53 20h14.94a2 2 0 001.74-3l-7.5-13a2 2 0 00-3.48 0z" />
            </svg>
          )}
        </div>

        <h1 className="text-5xl md:text-7xl font-black uppercase italic tracking-tighter mb-6 leading-none">
          {isVerifying ? (
            <>Validando <br /><span className="text-kenth-brightred">Transacción...</span></>
          ) : isConfirmed ? (
            <>¡Transacción <br /><span className="text-emerald-500">Confirmada!</span></>
          ) : (
            <>Problema al <br /><span className="text-yellow-500">Validar</span></>
          )}
        </h1>

        <p className="text-kenth-subtext text-lg mb-12 font-medium">
          {isVerifying
            ? 'Estamos sincronizando tu pago con PayPhone para activar tu curso.'
            : message}
          <br />
          <span className="text-xs opacity-50 block mt-4 uppercase tracking-widest font-black">
            ID: {transactionId || clientTransactionId || 'Buscando...'}
          </span>
        </p>

        <div className="space-y-4">
          <p className="text-[10px] font-black uppercase tracking-[0.3em] text-kenth-brightred animate-pulse">
            {isVerifying
              ? 'No cierres esta ventana'
              : isConfirmed
                ? 'Sincronización Exitosa'
                : 'Revisión Requerida'}
          </p>

          <div className="w-48 h-1 bg-kenth-border mx-auto rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: isVerifying ? "70%" : "100%" }}
              transition={{ duration: isVerifying ? 8 : 0.6, ease: "easeOut" }}
              className={`h-full ${isVerifying
                  ? 'bg-kenth-brightred'
                  : isConfirmed
                    ? 'bg-emerald-500'
                    : 'bg-yellow-500'
                }`}
            />
          </div>
        </div>
      </motion.div>
    </div>
  );
}