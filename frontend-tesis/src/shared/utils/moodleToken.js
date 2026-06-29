export const getMoodleToken = () => {
  const raw = localStorage.getItem('moodle_token');
  const token = typeof raw === 'string' ? raw.trim() : '';
  return token && token !== 'null' && token !== 'undefined' ? token : '';
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
