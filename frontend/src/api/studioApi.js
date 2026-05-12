/**
 * Studio API client — authenticated CRUD operations.
 */

const API_BASE = import.meta.env.VITE_API_BASE || "/api";

function getToken() {
  return localStorage.getItem("studio_token");
}

function authHeaders() {
  const token = getToken();
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function apiFetch(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: { ...authHeaders(), ...options.headers },
  });
  if (res.status === 401) {
    localStorage.removeItem("studio_token");
    window.location.href = "/studio/login";
    return null;
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

// ── Auth ──
export async function login(username, password) {
  const res = await fetch(`${API_BASE}/auth/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error("Invalid credentials");
  const data = await res.json();
  localStorage.setItem("studio_token", data.access);
  localStorage.setItem("studio_refresh", data.refresh);
  return data;
}

export function logout() {
  localStorage.removeItem("studio_token");
  localStorage.removeItem("studio_refresh");
}

export function isLoggedIn() {
  return !!getToken();
}

export async function getMe() {
  return apiFetch("/auth/me/");
}

// ── Series ──
export const fetchSeries = () => apiFetch("/studio/series/");
export const createSeries = (data) =>
  apiFetch("/studio/series/", { method: "POST", body: JSON.stringify(data) });
export const updateSeries = (id, data) =>
  apiFetch(`/studio/series/${id}/`, { method: "PATCH", body: JSON.stringify(data) });
export const deleteSeries = (id) =>
  apiFetch(`/studio/series/${id}/`, { method: "DELETE" });
export const reorderSeries = (items) =>
  apiFetch("/studio/series/reorder/", { method: "POST", body: JSON.stringify({ items }) });

// ── Modules ──
export const fetchModules = (seriesId) =>
  apiFetch(`/studio/modules/${seriesId ? `?series=${seriesId}` : ""}`);
export const createModule = (data) =>
  apiFetch("/studio/modules/", { method: "POST", body: JSON.stringify(data) });
export const updateModule = (id, data) =>
  apiFetch(`/studio/modules/${id}/`, { method: "PATCH", body: JSON.stringify(data) });
export const deleteModule = (id) =>
  apiFetch(`/studio/modules/${id}/`, { method: "DELETE" });
export const reorderModules = (items) =>
  apiFetch("/studio/modules/reorder/", { method: "POST", body: JSON.stringify({ items }) });

// ── Topics ──
export const fetchTopics = (moduleId) =>
  apiFetch(`/studio/topics/${moduleId ? `?module=${moduleId}` : ""}`);
export const fetchTopic = (id) => apiFetch(`/studio/topics/${id}/`);
export const createTopic = (data) =>
  apiFetch("/studio/topics/", { method: "POST", body: JSON.stringify(data) });
export const updateTopic = (id, data) =>
  apiFetch(`/studio/topics/${id}/`, { method: "PATCH", body: JSON.stringify(data) });
export const deleteTopic = (id) =>
  apiFetch(`/studio/topics/${id}/`, { method: "DELETE" });
export const publishTopic = (id) =>
  apiFetch(`/studio/topics/${id}/publish/`, { method: "POST" });
export const unpublishTopic = (id) =>
  apiFetch(`/studio/topics/${id}/unpublish/`, { method: "POST" });
export const reorderTopics = (items) =>
  apiFetch("/studio/topics/reorder/", { method: "POST", body: JSON.stringify({ items }) });

// ── Content Blocks ──
export const fetchBlocks = (topicId) =>
  apiFetch(`/studio/blocks/?topic=${topicId}`);
export const bulkSaveBlocks = (topicId, blocks) =>
  apiFetch("/studio/blocks/bulk_save/", {
    method: "POST",
    body: JSON.stringify({ topic: topicId, blocks }),
  });

// ── Problems ──
export const fetchProblems = (topicId) =>
  apiFetch(`/studio/problems/?topic=${topicId}`);
export const createProblem = (data) =>
  apiFetch("/studio/problems/", { method: "POST", body: JSON.stringify(data) });
export const updateProblem = (id, data) =>
  apiFetch(`/studio/problems/${id}/`, { method: "PATCH", body: JSON.stringify(data) });
export const deleteProblem = (id) =>
  apiFetch(`/studio/problems/${id}/`, { method: "DELETE" });
