/**
 * courseService.js
 * Servicio para gestionar la comunicación con la API de Moodle de KENTH Academy.
 */

// ==========================================
// 1. OBTENER EL CONTENIDO COMPLETO DE UN CURSO (PROXIED PARA SEGURIDAD)
// ==========================================
export const getCourseContents = async (token, secureCourseId) => {
  if (!token) throw new Error('No hay sesión activa.');
  
  // Usamos el proxy seguro para no exponer el ID numérico al llamar a Moodle
  const url = `/moodle_api/proyecto_curso/api_persistente/sec_contenidos.php?token=${encodeURIComponent(token)}&courseid=${encodeURIComponent(secureCourseId)}`;
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.error) throw new Error(data.error);
    return data;
  } catch (error) {
    console.error('Error en getCourseContents:', error);
    throw error;
  }
};

// ==========================================
// 1.1 OBTENER TODAS LAS CATEGORÍAS (LISTA COMPLETA)
// ==========================================
export const getCategories = async (token) => {
  if (!token) throw new Error('Se requiere token.');
  const url = `/moodle_api/webservice/rest/server.php?wstoken=${token}&wsfunction=core_course_get_categories&moodlewsrestformat=json`;
  
  try {
    const response = await fetch(url, { method: 'POST' });
    const data = await response.json();
    if (data.exception) throw new Error(data.message);
    return data;
  } catch (err) {
    console.error('Error en getCategories:', err);
    throw err;
  }
};

// ==========================================
// 2. OBTENER EL PERFIL DEL USUARIO
// ==========================================
export const getUserProfile = async (token) => {
  if (!token) throw new Error('No hay sesión activa.');

  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_profile.php?token=${token}&action=get`;

  try {
    const response = await fetch(url);
    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'No se pudo cargar el perfil.');
    }

    return result.data;
  } catch (error) {
    console.error('Error en getUserProfile:', error);
    throw error;
  }
};

// ==========================================
// 3. ACTUALIZAR EL PERFIL DEL USUARIO
// ==========================================
export const updateUserProfile = async (token, profileData) => {
  if (!token) throw new Error('No hay sesión activa.');

  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_profile.php?token=${token}&action=update`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profileData)
    });

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'Hubo un error al guardar el perfil.');
    }

    return result;
  } catch (error) {
    console.error('Error en updateUserProfile:', error);
    throw error;
  }
};

// ==========================================
// 4. EJECUTAR ACCIÓN SOBRE UN MÓDULO (Ocultar, Mostrar, Borrar, Duplicar)
// ==========================================
export const executeModuleAction = async (token, action, cmid) => {
  if (!token) throw new Error('No hay sesión activa.');

  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_actions.php?token=${token}&action=${action}&cmid=${cmid}`;

  try {
    const response = await fetch(url);
    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || `Error al ejecutar la acción: ${action}`);
    }

    return true;
  } catch (error) {
    console.error(`Error en executeModuleAction (${action}):`, error);
    throw error;
  }
};

// ==========================================
// 5. OBTENER MIS CURSOS (CATÁLOGO) CON SEGURIDAD (IDs FIRMADOS)
// ==========================================
export const getMyCourses = async (token) => {
  if (!token) throw new Error('Se requiere sesión activa.');

  const url = `/moodle_api/proyecto_curso/api_persistente/secure_lista.php?token=${encodeURIComponent(token)}`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (data.error) throw new Error(data.error);

    return data;
  } catch (error) {
    console.error('Error en getMyCourses:', error);
    throw error;
  }
};

// ==========================================
// 6. OBTENER AJUSTES DE UN CURSO (API PERSISTENTE)
// ==========================================
export const getCourseSettings = async (token, courseId) => {
  if (!token) throw new Error('No hay sesión activa.');

  // EL SECRETO: Añadir &t=${Date.now()} al final para destruir el caché del navegador
  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_course_settings.php?token=${encodeURIComponent(token)}&courseid=${encodeURIComponent(courseId)}&action=get&t=${Date.now()}`;

  try {
    const response = await fetch(url);
    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'No se pudieron cargar los ajustes del curso.');
    }

    return result.data;
  } catch (error) {
    console.error('Error en getCourseSettings:', error);
    throw error;
  }
};

// ==========================================
// 6.1 PREPARAR PAGO PAYPHONE
// ==========================================
export const preparePayPhonePayment = async (payPhoneToken, orderDetails) => {
  const url = 'https://pay.payphonetodoesposible.com/api/button/Prepare';
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${payPhoneToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderDetails)
    });

    if (!response.ok) throw new Error('Error al preparar el pago con PayPhone');
    
    return await response.json();
  } catch (error) {
    console.error('Error en preparePayPhonePayment:', error);
    throw error;
  }
};

// ==========================================
// 7. ACTUALIZAR AJUSTES DE UN CURSO
// ==========================================
export const updateCourseSettings = async (token, courseId, settingsData) => {
  if (!token) throw new Error('No hay sesión activa.');

  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_course_settings.php?token=${token}&courseid=${courseId}&action=update`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(settingsData)
    });

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || 'Hubo un error al guardar los ajustes del curso.');
    }

    return result;
  } catch (error) {
    console.error('Error en updateCourseSettings:', error);
    throw error;
  }
};

// ==========================================
// 8. INICIAR INTENCIÓN DE PAGO (GUEST SUPPORTED)
// ==========================================
export const initiatePaymentIntent = async (token, courseId, gateway, userInfo = null) => {
  // Ahora permitimos el inicio sin token para el flujo de invitados
  
  // Simulamos una latencia de red de pasarela
  await new Promise(resolve => setTimeout(resolve, 1500));

  console.log(`Iniciando pago para el curso ${courseId} vía ${gateway}...`);
  
  // Si es invitado, logueamos los datos que se enviarán como metadata
  if (userInfo) {
    console.log("Metadata de Invitado:", userInfo);
  }

  // Mock de respuesta exitosa de la pasarela
  return {
    success: true,
    transactionId: `SANDBOX_${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
    checkoutUrl: gateway === 'paypal' ? 'https://www.sandbox.paypal.com' : 'https://payphone.sandbox.com'
  };
};

// ==========================================
// 10. GENERAR LINK DE PAGO PAYPHONE (VÍA PROXY PHP PARA EVITAR CORS)
// ==========================================
export const generatePayPhoneLink = async (formData, courseName, courseId) => {
  const url = "/moodle_api/proyecto_curso/api_persistente/api_payphone_proxy.php";

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        courseName: courseName,
        courseId: courseId,
        email: formData?.email,
        firstname: formData?.firstname,
        lastname: formData?.lastname
      })
    });

    const data = await response.json();

    if (!response.ok) {
        // Volcado completo para ver qué rayos está enviando PayPhone
        const errorMsg = JSON.stringify(data);
        throw new Error(errorMsg);
    }

    return data.url || data.paymentUrl || data.payPhoneUri;
  } catch (error) {
    console.error("Error en generatePayPhoneLink:", error);
    throw error;
  }
};

// ==========================================
// 11. OBTENER CATÁLOGO COMERCIAL COMPLETO (PÚBLICO/ADMIN)
// ==========================================
export const getCommercialCatalog = async (token = null) => {
  // Ahora el endpoint GET es público, el token solo se usa para ver cursos ocultos si eres admin
  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_commercial.php${token ? `?token=${token}` : ''}`;
  
  try {
    const response = await fetch(url);
    const result = await response.json();
    if (!result.success) throw new Error(result.error);
    return result.data;
  } catch (error) {
    console.error('Error en getCommercialCatalog:', error);
    throw error;
  }
};

// ==========================================
// 12. ACTUALIZAR DATA COMERCIAL (ADMIN)
// ==========================================
export const updateCommercialData = async (token, courseId, commercialData) => {
  if (!token) throw new Error('Se requiere sesión activa.');
  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_commercial.php?token=${token}`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ courseid: courseId, ...commercialData })
    });
    const result = await response.json();
    if (!result.success) throw new Error(result.error);
    return result;
  } catch (error) {
    console.error('Error en updateCommercialData:', error);
    throw error;
  }
};

// ==========================================
// 13. OBTENER INFO PÚBLICA DE UN CURSO (DINÁMICO - REGLA 1)
// ==========================================
export const getPublicCourse = async (courseId) => {
  const url = `/moodle_api/proyecto_curso/api_persistente/tesis_commercial.php?courseid=${courseId}`;
  
  try {
    const response = await fetch(url);
    const result = await response.json();
    
    if (!result.success) throw new Error(result.error);

    // Moodle nos devuelve la data comercial y básica del curso
    return result.data;
  } catch (error) {
    console.error('Error en getPublicCourse:', error);
    // Fallback de seguridad por si falla la API
    return {
      id: courseId,
      fullname: "Curso KENTH",
      price: 49.99
    };
  }
};