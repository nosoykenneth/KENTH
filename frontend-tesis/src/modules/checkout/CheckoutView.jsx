import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import {
  getPublicCourse,
  initiatePaymentIntent,
  getMyCourses,
  getUserProfile,
  checkGuestEnrollmentByEmail
} from '../../shared/services/courseService';
import { showNotification } from '../../shared/components/ui/Notification';
import Notification from '../../shared/components/ui/Notification';

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export default function CheckoutView() {

  const { courseId: id } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [status, setStatus] = useState('idle'); // idle, processing, success, error
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  const [guestEnrollmentCheck, setGuestEnrollmentCheck] = useState({
    checking: false,
    checked: false,
    exists: false,
    isEnrolled: false,
    fullname: '',
    checkedEmail: ''
  });
  const createClientTxId = () => `KENTH-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;

  // CLIENT IDs (Sandbox)
  const PAYPAL_CLIENT_ID = import.meta.env.VITE_PAYPAL_CLIENT_ID || "test";

  // Estado para formulario de invitado (Guest Checkout)
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    email: ''
  });

  const formDataRef = useRef(formData);


  // Sincronizar la ref con el estado para que sea accesible desde callbacks asíncronos
  useEffect(() => {
    formDataRef.current = formData;
  }, [formData]);


  const token = localStorage.getItem('moodle_token');

  useEffect(() => {
    const fetchCourseAndEnrollment = async () => {
      try {
        setLoading(true);

        // Cargar info del curso
        const data = await getPublicCourse(id);
        setCourse(data);

        // Verificar sesión y cargar perfil
        if (token) {
          try {
            // Cargar perfil para tener datos de email/nombre
            const profile = await getUserProfile(token);
            setUserProfile(profile);

            // Sincronizar formData para consistencia (aunque no se muestre el form)
            setFormData({
              firstname: profile.firstname || '',
              lastname: profile.lastname || '',
              email: profile.email || ''
            });

            const misCursos = await getMyCourses(token);
            const yaMatriculado = misCursos.some(c => String(c.id) === String(id));
            setIsEnrolled(yaMatriculado);
          } catch (e) {
            console.error("Error al verificar perfil/matrícula:", e);
          }
        }

      } catch (error) {
        console.error("Error al cargar curso:", error);
        showNotification('error', 'No se pudo cargar la información del curso.');
      } finally {
        setLoading(false);
      }
    };
    fetchCourseAndEnrollment();
  }, [id, token]);

  const getEffectiveProfile = () => {
    const savedData = JSON.parse(localStorage.getItem('kenth_guest_data') || '{}');

    if (token) {
      return {
        firstname: (userProfile?.firstname || formDataRef.current.firstname || '').trim(),
        lastname: (userProfile?.lastname || formDataRef.current.lastname || '').trim(),
        email: (userProfile?.email || formDataRef.current.email || '').trim()
      };
    }

    return {
      firstname: (savedData.firstname || formDataRef.current.firstname || '').trim(),
      lastname: (savedData.lastname || formDataRef.current.lastname || '').trim(),
      email: (savedData.email || formDataRef.current.email || '').trim()
    };
  };

  const canRenderPayphoneButton = () => {
    if (loading || isEnrolled) return false;
    if (token) return true;

    return (
      formData.firstname.trim() &&
      formData.lastname.trim() &&
      emailRegex.test(formData.email) &&
      !guestEnrollmentCheck.isEnrolled &&
      !guestEnrollmentCheck.checking
    );
  };

  const registerLocalIntent = async (clientTransactionId) => {
    const effectiveProfile = getEffectiveProfile();

    const response = await fetch('/moodle_api/proyecto_curso/api_persistente/api_register_intent.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        clientTransactionId,
        course_id: id,
        email: effectiveProfile.email,
        firstname: effectiveProfile.firstname,
        lastname: effectiveProfile.lastname
      })
    });

    const data = await response.json();

    if (!data.success) {
      throw new Error(data.error || 'No se pudo registrar la intención de pago.');
    }

    return { effectiveProfile };
  };


  const validateGuestData = () => {
    if (!token) {
      const currentData = formDataRef.current;

      if (!currentData.firstname || !currentData.lastname || !currentData.email) {
        showNotification('error', 'Por favor, completa tus datos para enviarte el acceso.');
        return false;
      }

      if (!emailRegex.test(currentData.email)) {
        showNotification('error', 'Ingresa un correo electrónico válido.');
        return false;
      }

      if (guestEnrollmentCheck.isEnrolled) {
        showNotification('error', 'Este correo ya está matriculado en este curso.');
        return false;
      }

      if (guestEnrollmentCheck.checking) {
        showNotification('error', 'Estamos verificando el correo. Intenta de nuevo en un momento.');
        return false;
      }
    }

    return true;
  };

  useEffect(() => {
    if (token) return;

    const email = formData.email.trim();
    const firstname = formData.firstname.trim();
    const lastname = formData.lastname.trim();

    if (!firstname || !lastname || !emailRegex.test(email)) {
      setGuestEnrollmentCheck({
        checking: false,
        checked: false,
        exists: false,
        isEnrolled: false,
        fullname: '',
        checkedEmail: ''
      });

      return;
    }

    const timeout = setTimeout(async () => {
      try {
        setGuestEnrollmentCheck(prev => ({ ...prev, checking: true }));

        const result = await checkGuestEnrollmentByEmail(id, email);

        setGuestEnrollmentCheck({
          checking: false,
          checked: true,
          exists: result.exists,
          isEnrolled: result.isEnrolled,
          fullname: result.fullname || '',
          checkedEmail: email
        });

      } catch (error) {
        console.error('Error verificando matrícula del invitado:', error);
        setGuestEnrollmentCheck({
          checking: false,
          checked: false,
          exists: false,
          isEnrolled: false,
          fullname: '',
          checkedEmail: ''
        });

      }
    }, 500);

    return () => clearTimeout(timeout);
  }, [formData.email, formData.firstname, formData.lastname, id, token]);

  const handleSuccessFlow = async (gateway, transactionId) => {
    setProcessing(true);
    setStatus('processing');
    try {
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

  const isPayphoneBlocked = !token && (
    !formData.firstname.trim() ||
    !formData.lastname.trim() ||
    !emailRegex.test(formData.email) ||
    guestEnrollmentCheck.isEnrolled ||
    guestEnrollmentCheck.checking
  );

  const handlePayphoneRedirect = async () => {
    if (!isGuestEmailApproved) {
      if (guestEnrollmentCheck.checking) {
        showNotification('error', 'Estamos verificando el correo. Espera un momento.');
      } else if (guestEnrollmentCheck.isEnrolled) {
        showNotification('error', 'Este correo ya está matriculado en este curso.');
      } else {
        showNotification('error', 'Completa y valida tus datos antes de continuar.');
      }
      return;
    }

    try {
      setProcessing(true);
      setStatus('processing');

      const clientTxId = createClientTxId();
      localStorage.setItem('kenth_client_tx', clientTxId);

      const { effectiveProfile } = await registerLocalIntent(clientTxId);

      const prepareResponse = await fetch('/moodle_api/proyecto_curso/api_persistente/api_prepare_payphone.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          clientTransactionId: clientTxId,
          course_id: id,
          email: effectiveProfile.email,
          firstname: effectiveProfile.firstname,
          lastname: effectiveProfile.lastname,
          course_name: course?.fullname || 'Curso KENTH',
          amount: (course?.offer_price > 0 && course?.offer_price < course?.price)
            ? course.offer_price
            : (course?.price || 49.99)
        })
      });

      const prepareData = await prepareResponse.json();

      if (!prepareData.success || !prepareData.payUrl) {
        throw new Error(prepareData.error || 'No se pudo generar el enlace de pago.');
      }

      window.location.href = prepareData.payUrl;
    } catch (error) {
      showNotification('error', error.message || 'Error al iniciar el pago.');
      setStatus('idle');
      setProcessing(false);
    }
  };

  const handlePayPalBackendCapture = async (orderID, clientTransactionId) => {
    try {
      setProcessing(true);
      setStatus('processing');

      const effectiveProfile = getEffectiveProfile();

      const response = await fetch('/moodle_api/proyecto_curso/api_persistente/api_capture_paypal_order.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          orderID,
          clientTransactionId,
          course_id: id,
          email: effectiveProfile.email,
          firstname: effectiveProfile.firstname,
          lastname: effectiveProfile.lastname
        })
      });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error || 'No se pudo completar la captura del pago.');
      }

      localStorage.removeItem('kenth_guest_data');

      setStatus('success');

      setTimeout(() => {
        if (!token) {
          navigate('/login', {
            state: {
              message: result.alreadyProcessed
                ? 'Tu pago ya estaba verificado previamente.'
                : '¡Pago verificado! Tu acceso ha sido enviado a tu correo.'
            }
          });
        } else {
          navigate('/dashboard');
        }
      }, 4000);

    } catch (error) {
      setStatus('idle');
      showNotification('error', error.message || 'Error al procesar el pago con PayPal.');
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-kenth-bg flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-kenth-brightred/20 border-t-kenth-brightred rounded-full animate-spin"></div>
      </div>
    );
  }




  const normalizedEmail = formData.email.trim().toLowerCase();

  const isGuestEmailApproved =
    token ||
    (
      formData.firstname.trim() &&
      formData.lastname.trim() &&
      emailRegex.test(normalizedEmail) &&
      guestEnrollmentCheck.checked &&
      !guestEnrollmentCheck.checking &&
      guestEnrollmentCheck.checkedEmail === normalizedEmail &&
      !guestEnrollmentCheck.isEnrolled
    );


  return (
    <PayPalScriptProvider
      options={{
        "client-id": PAYPAL_CLIENT_ID,
        currency: "USD",
        intent: "capture",
        locale: "es_MX",
        "disable-funding": "card,credit,venmo"
      }}
    >
      <div className="w-full bg-kenth-bg text-kenth-text font-sans min-h-screen">
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
                      onChange={(e) => {
                        const val = e.target.value;
                        const next = { ...formData, firstname: val };
                        setFormData(next);
                        localStorage.setItem('kenth_guest_data', JSON.stringify(next));
                        setGuestEnrollmentCheck({
                          checking: false,
                          checked: false,
                          exists: false,
                          isEnrolled: false,
                          fullname: '',
                          checkedEmail: ''
                        });

                      }}
                      className="w-full bg-kenth-bg border border-kenth-border p-4 rounded-2xl outline-none focus:border-kenth-brightred transition-all"
                    />
                    <input
                      type="text"
                      placeholder="Apellido"
                      value={formData.lastname}
                      onChange={(e) => {
                        const val = e.target.value;
                        const next = { ...formData, lastname: val };
                        setFormData(next);
                        localStorage.setItem('kenth_guest_data', JSON.stringify(next));
                        setGuestEnrollmentCheck({
                          checking: false,
                          checked: false,
                          exists: false,
                          isEnrolled: false,
                          fullname: '',
                          checkedEmail: ''
                        });

                      }}
                      className="w-full bg-kenth-bg border border-kenth-border p-4 rounded-2xl outline-none focus:border-kenth-brightred transition-all"
                    />
                    <input
                      type="email"
                      placeholder="Correo Electrónico"
                      className="w-full bg-kenth-bg border border-kenth-border p-4 rounded-2xl outline-none focus:border-kenth-brightred transition-all md:col-span-2"
                      value={formData.email}
                      onChange={(e) => {
                        const val = e.target.value;
                        const next = { ...formData, email: val };
                        setFormData(next);
                        localStorage.setItem('kenth_guest_data', JSON.stringify(next));
                        setGuestEnrollmentCheck({
                          checking: false,
                          checked: false,
                          exists: false,
                          isEnrolled: false,
                          fullname: '',
                          checkedEmail: ''
                        });

                      }}
                    />
                    {!token && guestEnrollmentCheck.checking && (
                      <p className="md:col-span-2 text-xs text-kenth-subtext font-bold uppercase tracking-widest">
                        Verificando matrícula...
                      </p>
                    )}

                    {!token && guestEnrollmentCheck.isEnrolled && (
                      <div className="md:col-span-2 bg-amber-500/10 border border-amber-500/20 text-amber-400 p-4 rounded-2xl text-sm font-bold">
                        Este correo ya está matriculado en este curso. No puedes volver a comprarlo con esta dirección.
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </div>

            {/* DERECHA: ACCIÓN */}
            <div className="lg:col-span-5 space-y-6 lg:sticky lg:top-32">
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-kenth-card border border-kenth-border p-8 md:p-10 rounded-[2.5rem] shadow-2xl overflow-hidden relative"
              >
                {isEnrolled ? (
                  <div className="flex flex-col items-center text-center py-6 animate-in fade-in zoom-in-95 duration-500">
                    <div className="w-20 h-20 bg-emerald-500/10 text-emerald-500 rounded-full flex items-center justify-center mb-6 border border-emerald-500/20 shadow-[0_0_40px_rgba(16,185,129,0.1)]">
                      <svg className="w-10 h-10" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    </div>
                    <h3 className="text-2xl font-black uppercase tracking-tighter italic mb-4">¡Ya eres parte!</h3>
                    <p className="text-kenth-subtext text-sm mb-10 leading-relaxed font-medium">
                      Ya tienes acceso a este curso. No es necesario volver a comprarlo. ¡Ve a tu estudio y comienza a aprender!
                    </p>
                    <Link
                      to="/dashboard"
                      className="w-full bg-kenth-brightred hover:bg-red-700 text-white font-black uppercase tracking-widest text-xs py-5 rounded-2xl transition-all shadow-[0_10px_30px_rgba(225,29,72,0.3)] hover:-translate-y-1 active:translate-y-0.5 text-center"
                    >
                      Ir a mi estudio
                    </Link>
                  </div>
                ) : (
                  <>
                    <h3 className="text-xl font-black uppercase tracking-tighter italic mb-8">Confirmar Compra</h3>

                    <div className="space-y-6">
                      <div className="w-full">
                        <button
                          type="button"
                          onClick={handlePayphoneRedirect}
                          disabled={!isGuestEmailApproved}
                          className={`w-full h-[50px] rounded-full font-black uppercase tracking-widest text-[10px] flex items-center justify-center gap-2 transition-all
                            ${!isGuestEmailApproved
                              ? 'bg-orange-500/30 text-white/50 cursor-not-allowed'
                              : 'bg-[#f97316] hover:bg-orange-400 text-white shadow-[0_10px_30px_rgba(249,115,22,0.35)]'}`}
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                          </svg>
                          Pagar con tarjeta de crédito
                        </button>
                      </div>


                      <div className="relative py-4">
                        <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-kenth-border"></div></div>
                        <div className="relative flex justify-center text-[10px] uppercase font-black tracking-[0.3em]"><span className="bg-kenth-card px-4 text-kenth-subtext">Alternativa</span></div>
                      </div>

                      <div className={`${!isGuestEmailApproved ? 'pointer-events-none opacity-50' : ''}`}>
                        <div className="w-full">
                          <PayPalButtons
                            style={{ layout: "vertical", shape: "pill", color: "blue", label: "pay", height: 50 }}
                            forceReRender={[isGuestEmailApproved, course?.price, course?.offer_price]}
                            disabled={!isGuestEmailApproved}
                            createOrder={async (data, actions) => {
                              if (!validateGuestData()) {
                                showNotification('error', 'Completa y valida tus datos antes de continuar.');
                                throw new Error('Datos inválidos');
                              }

                              try {
                                const clientTxId = createClientTxId();
                                localStorage.setItem('kenth_client_tx', clientTxId);

                                await registerLocalIntent(clientTxId);

                                const priceToUse =
                                  (course?.offer_price > 0 && course?.offer_price < course?.price)
                                    ? course.offer_price
                                    : (course?.price || 49.99);

                                return actions.order.create({
                                  purchase_units: [
                                    {
                                      reference_id: clientTxId,
                                      description: course?.fullname || 'Curso KENTH',
                                      amount: {
                                        currency_code: 'USD',
                                        value: Number(priceToUse).toFixed(2)
                                      }
                                    }
                                  ]
                                });
                              } catch (error) {
                                showNotification('error', error.message || 'No se pudo iniciar el pago con PayPal.');
                                throw error;
                              }
                            }}
                            onApprove={async (data) => {
                              const clientTransactionId = localStorage.getItem('kenth_client_tx');
                              await handlePayPalBackendCapture(data.orderID, clientTransactionId);
                            }}
                            onError={(err) => {
                              console.error('PAYPAL ERROR:', err);
                              showNotification('error', 'Error al procesar el pago con PayPal.');
                            }}
                          />
                        </div>
                      </div>
                    </div>

                    <div className="mt-8 pt-8 border-t border-kenth-border flex items-center gap-4 opacity-50">
                      <svg className="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                      <span className="text-[10px] font-black uppercase tracking-widest leading-none">Seguridad Bancaria PCI DSS</span>
                    </div>
                  </>
                )}
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
