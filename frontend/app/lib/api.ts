const API = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function api(path: string, options: RequestInit = {}) {
  const token = localStorage.getItem('access_token');
  const res = await fetch(`${API}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (res.status === 401) {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_id')
    window.location.href = '/';
   // throw new Error('unauthorized');
  }

  return res;
}