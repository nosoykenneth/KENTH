// Fuente unica de verdad para el token de sesion de Moodle.
// Centralizar aqui evita que un valor invalido (p. ej. el string "null"
// guardado por error) se cuele en unas comprobaciones y no en otras, que es
// lo que producia el falso "Sesion expirada" en los recursos.

const STORAGE_KEY = 'moodle_token';

const sanitize = (value) => {
  const token = typeof value === 'string' ? value.trim() : '';
  return token && token !== 'null' && token !== 'undefined' ? token : '';
};

// Devuelve el token valido o '' (lectura pura, sin efectos secundarios).
export const getMoodleToken = () => sanitize(localStorage.getItem(STORAGE_KEY));

// Boolean de "hay sesion valida". Lo usan los guards de rutas.
export const hasMoodleSession = () => Boolean(getMoodleToken());

// Persiste el token SOLO si es valido; cualquier basura limpia la sesion.
// Devuelve el token guardado o '' si no se guardo nada.
export const persistMoodleToken = (value) => {
  const token = sanitize(value);
  if (!token) {
    localStorage.removeItem(STORAGE_KEY);
    return '';
  }
  localStorage.setItem(STORAGE_KEY, token);
  return token;
};

export const buildMoodleViewUrl = ({ token, cmid, modname, extra = {} }) => {
  if (!token || !cmid || !modname) return '';

  const params = new URLSearchParams({
    token,
    cmid: String(cmid),
    modname: String(modname),
  });

  Object.entries(extra).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.set(key, String(value));
    }
  });

  return `/api/lms/proyecto_curso/api_persistente/tesis_view.php?${params.toString()}`;
};
