/**
 * Dispara una notificación global desde cualquier parte del app.
 *
 * Vive separado del componente Notification para no romper React Fast Refresh:
 * un archivo que exporta un componente no debe exportar además utilidades.
 *
 * @param {('success'|'error')} type
 * @param {string} text
 */
export const showNotification = (type, text) => {
  window.dispatchEvent(
    new CustomEvent('kenth-notification', {
      detail: { type, text, id: Date.now() },
    }),
  );
};
