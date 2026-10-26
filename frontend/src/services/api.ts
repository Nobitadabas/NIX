export type ApiCase = {
  case_id: string;
  transaction_id: string;
  amount: number;
  currency: string;
  risk_score: number;
  risk_band: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  reasons: string[];
  warnings: string[];
  status: "NEW" | "UNDER_REVIEW" | "ACKNOWLEDGED" | "RESOLVED";
  scoring_version: string;
  data_mode: string;
  ledger_status: string;
  verification_status: string;
  ledger_reference: string | null;
  created_at: string;
  updated_at: string;
};

const mode = (import.meta.env.VITE_TRUSTRAIL_MODE ?? "demo").toLowerCase();
export const isRealMode = mode === "real";
const baseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, { headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) }, ...init });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? `API request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<{ status: string; mode: string; scoring: string; ledger: string }>("/health"),
  score: (payload: object) => request<{ score: number; risk_band: ApiCase["risk_band"]; reasons: string[]; warnings: string[] }>("/api/v1/transactions/score", { method: "POST", body: JSON.stringify(payload) }),
  listCases: () => request<{ items: ApiCase[] }>("/api/v1/cases"),
  createCase: (payload: object) => request<ApiCase>("/api/v1/cases", { method: "POST", body: JSON.stringify(payload) }),
  transition: (caseId: string, toStatus: string) => request<ApiCase>(`/api/v1/cases/${caseId}/transitions`, { method: "POST", body: JSON.stringify({ to_status: toStatus }) }),
};
