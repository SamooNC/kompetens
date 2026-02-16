/**
 * Lightweight fetch wrapper for the Kompetens API.
 *
 * All calls go through the Vite dev-server proxy (/api → backend)
 * so we never need an absolute URL in dev, and in production the
 * VITE_API_URL env var points to the NC server.
 */

const API_URL: string = import.meta.env.VITE_API_URL ?? "";

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const text = await response.text().catch(() => "Unknown error");
    throw new ApiError(response.status, `API ${response.status}: ${text}`);
  }
  return response.json() as Promise<T>;
}

/**
 * Perform a GET request against the backend.
 *
 * @param path - API path, e.g. "/api/health"
 */
export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });
  return handleResponse<T>(response);
}

/**
 * Perform a POST request against the backend.
 *
 * @param path - API path, e.g. "/api/inventory/start"
 * @param body - JSON-serialisable payload
 */
export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(body),
  });
  return handleResponse<T>(response);
}

/**
 * Quick health-check against the backend.
 * Returns `{ status: "ok" }` when the API is reachable.
 */
export async function checkHealth(): Promise<{ status: string }> {
  return apiGet<{ status: string }>("/api/health");
}
