const STORAGE_KEYS = {
  fullName: 'moodle_userfullname',
  role: 'moodle_rol',
  token: 'moodle_token',
  userId: 'moodle_userid',
};

const SESSION_EVENT_NAME = 'moodle-session-updated';

function notifySessionChange() {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new Event(SESSION_EVENT_NAME));
  }
}

export function getMoodleToken() {
  return localStorage.getItem(STORAGE_KEYS.token) || '';
}

export function getMoodleUserId() {
  return localStorage.getItem(STORAGE_KEYS.userId) || '';
}

export function getMoodleFullName() {
  return localStorage.getItem(STORAGE_KEYS.fullName) || '';
}

export function setMoodleToken(token) {
  localStorage.setItem(STORAGE_KEYS.token, token);
  notifySessionChange();
}

export function setMoodleUserProfile({ fullName, userId }) {
  if (typeof userId !== 'undefined' && userId !== null && userId !== '') {
    localStorage.setItem(STORAGE_KEYS.userId, userId);
  }

  if (typeof fullName === 'string' && fullName.trim()) {
    localStorage.setItem(STORAGE_KEYS.fullName, fullName);
  }

  notifySessionChange();
}

export function clearMoodleSession() {
  Object.values(STORAGE_KEYS).forEach((key) => localStorage.removeItem(key));
  notifySessionChange();
}

export function subscribeToMoodleSession(listener) {
  if (typeof window === 'undefined') {
    return () => {};
  }

  window.addEventListener(SESSION_EVENT_NAME, listener);
  window.addEventListener('storage', listener);

  return () => {
    window.removeEventListener(SESSION_EVENT_NAME, listener);
    window.removeEventListener('storage', listener);
  };
}
