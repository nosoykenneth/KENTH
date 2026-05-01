import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { getPublicCourse, initiatePaymentIntent, generatePayPhoneLink } from '../services/courseService';
import { showNotification } from '../components/ui/Notification';
import Logo from '../components/ui/Logo';
import Navbar from '../components/layout/Navbar';
import Notification from '../components/ui/Notification';

export default function CheckoutView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [status, setStatus] = useState('idle'); // idle, processing, success, error

  // CLIENT IDs (Sandbox)
  const PAYPAL_CLIENT_ID = import.meta.env.VITE_PAYPAL_CLIENT_ID || "test";

  // Estado para formulario de invitado (Guest Checkout)
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    email: ''
  });

  const token = localStorage.getItem('moodle_token');

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        setLoading(true);
        const data = await getPublicCourse(id);
        setCourse(data);
      } catch (error) {
        console.error("Error al cargar curso:", error);
        showNotification('error', 'No se pudo cargar la información del curso.');
      } finally {
        setLoading(false);
      }
    };
    fetchCourse();
  }, [id]);

  // Función para validar datos de invitado antes de cualquier pago
  // 1. Añadimos esta referencia para que el botón siempre lea lo último que escribiste
  const formDataRef = React.useRef(formData);
  useEffect(() => {
    formDataRef.current = formData;
  }, [formData]);

  // 2. Modificamos la validación para que lea de la referencia
  const validateGuestData = () => {
    if (!token) {
      const currentData = formDataRef.current;
      if (!currentData.firstname || !currentData.lastname || !currentData.email) {
        showNotification('error', 'Por favor, completa tus datos para enviarte el acceso.');
        return false;
      }
      if (!currentData.email.includes('@')) {
        showNotification('error', 'Ingresa un correo electrónico válido.');
        return false;
      }
    }
    return true;
  };

  const handleSuccessFlow = async (gateway, transactionId) => {
    setProcessing(true);
    setStatus('processing');
    try {
      // Notificamos a nuestro backend (Simulado aquí)
      const response = await initiatePaymentIntent(token, id, gateway, !token ? formData : null);

      if (response.success) {
        setStatus('success');
        setTimeout(() => {
          if (!token) {
            navigate('/login', { state: { message: '¡Pago exitoso! Revisa tu correo para tus credenciales.' } });
          } else {
            navigate('/dashboard');
          }
        }, 4000);
      }
    } catch (error) {
      setStatus('error');
      showNotification('error', 'Error al procesar la matrícula.');
    } finally {
      setProcessing(false);
    }
  };


  useEffect(() => {
    if (loading) return;

    const initButton = () => {
      const container = document.getElementById("pp-button");
      if (container && window.payphone) {
        try {
          container.innerHTML = "";

          window.payphone.Button({
            // 1. Conectado a tu .env
            token: import.meta.env.VITE_PAYPHONE_TOKEN, 
            btnHorizontal: true,
            btnCard: true,
            createOrder: function (actions) {
              const hasOffer = course?.offer_price > 0 && course?.offer_price < course?.price;
              const priceToUse = hasOffer ? course.offer_price : (course?.price || 49.99);
              const finalAmount = Math.round(priceToUse * 100);
              
              return actions.prepare({
                amount: finalAmount,
                amountWithoutTax: finalAmount,
                amountWithTax: 0,
                tax: 0,
                currency: "USD",
                clientTransactionId: `KENTH-${Date.now()}`,
                // 2. Conectado a tu .env
                storeId: import.meta.env.VITE_PAYPHONE_STORE_ID, 
                reference: course?.fullname ? `Matricula: ${course.fullname.substring(0, 20)}` : "Matricula KENTH"
              });
            },
            onComplete: function (model, actions) {
              setStatus('success');
              setTimeout(() => {
                navigate(token ? '/dashboard' : '/login', {
                  state: { message: '¡Pago detectado con éxito! Tu curso ya está listo.' }
                });
              }, 4000);
            }
          }).render("#pp-button");

        } catch (error) {
          console.error("Error al inyectar PayPhone:", error);
        }
      }
    };

    if (!window.payphone) {
      const script = document.createElement("script");
      // 3. Conectado a tu .env
      script.src = `https://pay.payphonetodoesposible.com/api/button/js?appId=${import.meta.env.VITE_PAYPHONE_APP_ID}`;
      script.async = true;
      script.onload = () => setTimeout(initButton, 200);
      document.body.appendChild(script);
    } else {
      setTimeout(initButton, 200);
    }
  }, [course, loading]);

  if (loading) {
    return (
      <div className="min-h-screen bg-kenth-bg flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-kenth-brightred/20 border-t-kenth-brightred rounded-full animate-spin"></div>
      </div>
    );
  }

  // Validador en tiempo real
  const isFormValid = token ? true : (formData.firstname && formData.lastname && formData.email.includes('@'));

  return (
    <PayPalScriptProvider options={{
      "client-id": PAYPAL_CLIENT_ID,
      "locale": "es_MX",
      "disable-funding": "card,credit,venmo"
    }}>
      <div className="min-h-screen bg-kenth-bg text-kenth-text font-sans">
        <Navbar />
        <Notification />

        <div className="max-w-6xl mx-auto py-24 md:py-32 px-6">

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">

            {/* IZQUIERDA: RESUMEN Y DATOS */}
            <div className="lg:col-span-7 space-y-8">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-kenth-card border border-kenth-border p-8 md:p-12 rounded-[3rem] shadow-2xl relative overflow-hidden"
              >
                <span className="text-[10px] font-black uppercase tracking-[0.4em] text-kenth-brightred mb-8 block">Inversión Educativa</span>
                <h3 className="text-4xl md:text-6xl font-black uppercase tracking-tighter leading-none mb-6 italic">
                  {course?.fullname}
                </h3>
                <div className="pt-8 border-t border-kenth-border flex justify-between items-end">
                  <div className="flex flex-col">
                    <span className="text-xs font-bold uppercase text-kenth-subtext tracking-widest mb-1">Precio Final</span>
                    <div className="flex items-center gap-4">
                      {course?.offer_price > 0 && course?.offer_price < course?.price && (
                        <span className="text-2xl font-bold text-kenth-subtext line-through opacity-50 decoration-kenth-brightred decoration-2">
                          ${course.price}
                        </span>
                      )}
                      <span className={`text-6xl font-black italic ${course?.offer_price > 0 ? 'text-emerald-500' : 'text-kenth-text'}`}>
                        ${(course?.offer_price > 0 && course?.offer_price < course?.price) ? course.offer_price : (course?.price || '49.99')}
                      </span>
                    </div>
                  </div>
                </div>
              </motion.div>

              {!token && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-kenth-surface/5 border border-kenth-border p-8 md:p-10 rounded-[2.5rem]"
                >
                  <h3 className="text-xl font-black uppercase tracking-tighter italic mb-8">Tus Datos de Acceso</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <input
                      type="text"
                      placeholder="Nombre"
                      value={formData.firstname}
                      onChange={(e) => setFormData({ ...formData, firstname: e.target.value })}
                      className="w-full bg-kenth-bg border border-kenth-border p-4 rounded-2xl outline-none focus:border-kenth-brightred transition-all"
                    />
                    <input
                      type="text"
                      placeholder="Apellido"
                      value={formData.lastname}
                      onChange={(e) => setFormData({ ...formData, lastname: e.target.value })}
                      className="w-full bg-kenth-bg border border-kenth-border p-4 rounded-2xl outline-none focus:border-kenth-brightred transition-all"
                    />
                    <input
                      type="email"
                      placeholder="Correo Electrónico"
                      className="w-full bg-kenth-bg border border-kenth-border p-4 rounded-2xl outline-none focus:border-kenth-brightred transition-all md:col-span-2"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    />
                  </div>
                </motion.div>
              )}
            </div>

            {/* DERECHA: ACCIÓN */}
            <div className="lg:col-span-5 space-y-6 lg:sticky lg:top-32">
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-kenth-card border border-kenth-border p-8 md:p-10 rounded-[2.5rem] shadow-2xl"
              >
                <h3 className="text-xl font-black uppercase tracking-tighter italic mb-8">Confirmar Compra</h3>

                <div className="space-y-6">
                  <div className="relative w-full">
                    {/* 1. El contenedor real donde PayPhone inyecta sus botones */}
                    <div id="pp-button" className="w-full min-h-[60px] flex items-center justify-center transition-all"></div>

                    {/* 2. El escudo invisible protector */}
                    {!isFormValid && (
                      <div
                        className="absolute inset-0 z-10 cursor-pointer"
                        onClick={() => showNotification('error', 'Por favor, completa tus datos arriba para habilitar el pago.')}
                      ></div>
                    )}
                  </div>

                  <div className="relative py-4">
                    <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-kenth-border"></div></div>
                    <div className="relative flex justify-center text-[10px] uppercase font-black tracking-[0.3em]"><span className="bg-kenth-card px-4 text-kenth-subtext">Alternativa</span></div>
                  </div>

                  <div className="relative z-0 opacity-80 hover:opacity-100 transition-opacity">
                    <PayPalButtons
                      style={{ layout: "vertical", shape: "pill", color: "blue", label: "pay" }}
                      createOrder={(data, actions) => {
                        if (!validateGuestData()) return;
                        return actions.order.create({
                          purchase_units: [{
                            description: course?.fullname || "Curso KENTH",
                            amount: { value: (course?.price || 49.99).toString() }
                          }]
                        });
                      }}
                      onApprove={async (data, actions) => {
                        const details = await actions.order.capture();
                        handleSuccessFlow('paypal', details.id);
                      }}
                    />
                  </div>
                </div>

                <div className="mt-8 pt-8 border-t border-kenth-border flex items-center gap-4 opacity-50">
                  <svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                  <span className="text-[10px] font-black uppercase tracking-widest leading-none">Seguridad Bancaria PCI DSS</span>
                </div>
              </motion.div>
            </div>
          </div>

          <AnimatePresence>
            {status === 'processing' && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 bg-kenth-bg/95 backdrop-blur-2xl z-[300] flex flex-col items-center justify-center p-10 text-center">
                <div className="w-20 h-20 border-4 border-emerald-500/20 border-t-emerald-500 rounded-full animate-spin mb-8 shadow-2xl shadow-emerald-500/20"></div>
                <h2 className="text-4xl font-black uppercase italic tracking-tighter mb-4 animate-pulse">Esperando Pago</h2>
                <p className="text-kenth-subtext max-w-xs font-medium uppercase tracking-[0.3em] text-[10px]">Realiza la transacción en la ventana emergente...</p>
              </motion.div>
            )}

            {status === 'success' && (
              <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="fixed inset-0 bg-kenth-bg/95 backdrop-blur-3xl z-[600] flex flex-col items-center justify-center p-10 text-center">
                <div className="w-28 h-28 bg-emerald-500 rounded-full flex items-center justify-center text-white mb-8 shadow-[0_0_60px_rgba(16,185,129,0.3)]">
                  <svg className="w-14 h-14" fill="none" stroke="currentColor" strokeWidth={4} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                </div>
                <h2 className="text-5xl md:text-7xl font-black uppercase italic tracking-tighter mb-6 italic">¡Pago Validado!</h2>
                <p className="text-xl text-kenth-subtext mb-12 max-w-lg font-medium">
                  Hemos detectado tu pago. Redirigiéndote a tu nueva aula virtual.
                </p>
                <div className="w-64 h-1.5 bg-kenth-surface/20 rounded-full overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: '100%' }} transition={{ duration: 4, ease: "easeInOut" }} className="h-full bg-emerald-500" />
                </div>
              </motion.div>
            )}
          </AnimatePresence>

        </div>
      </div>
    </PayPalScriptProvider>
  );
}
