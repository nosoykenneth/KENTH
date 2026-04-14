const REST_API_BASE_URL = '/moodle_api/webservice/rest/server.php';

export async function requestMoodleRestJson(params, options = {}) {
  const searchParams = new URLSearchParams(params);
  const response = await fetch(`${REST_API_BASE_URL}?${searchParams.toString()}`, {
    method: 'POST',
    ...options,
  });

  return response.json();
}

export async function requestMoodleRestText(params, options = {}) {
  const searchParams = new URLSearchParams(params);
  const response = await fetch(`${REST_API_BASE_URL}?${searchParams.toString()}`, {
    method: 'POST',
    ...options,
  });

  return response.text();
}

export { REST_API_BASE_URL };
