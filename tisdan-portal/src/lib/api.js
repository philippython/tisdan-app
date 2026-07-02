const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8002";

export function getToken() {
  return localStorage.getItem("tisdan_token") || "";
}

export function saveToken(token) {
  localStorage.setItem("tisdan_token", token);
}

export function clearToken() {
  localStorage.removeItem("tisdan_token");
}

export async function apiFetch(method, path, body = null, token = null) {
  const t = token || getToken();
  const headers = {};
  if (t) headers["Authorization"] = `Bearer ${t}`;

  let fetchOptions = { method, headers };

  if (body) {
    headers["Content-Type"] = "application/json";
    fetchOptions.body = JSON.stringify(body);
  }

  const res = await fetch(`${BASE_URL}${path}`, fetchOptions);

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export async function apiLogin(email, password) {
  const form = new URLSearchParams({ username: email, password });
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Invalid credentials");
  }
  return res.json();
}
