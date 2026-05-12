/**
 * API client — single source for all backend requests.
 *
 * In development, Vite proxies /api → Django.
 * In production, set VITE_API_BASE to the backend URL.
 */

const BASE = import.meta.env.VITE_API_BASE || "/api";

async function fetchJSON(path) {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${path}`);
  }
  return res.json();
}

// ── Series endpoints ──
export const getSeriesList = () => fetchJSON("/series/");
export const getSeries = (slug) => fetchJSON(`/series/${slug}/`);

// ── Module endpoints ──
export const getModules = () => fetchJSON("/modules/");
export const getModule = (slug) => fetchJSON(`/modules/${slug}/`);
export const getModuleRevision = (slug) => fetchJSON(`/modules/${slug}/revision/`);

// ── Topic endpoints ──
export const getTopic = (slug) => fetchJSON(`/topics/${slug}/`);
export const getTopicProblems = (slug) => fetchJSON(`/topics/${slug}/problems/`);
