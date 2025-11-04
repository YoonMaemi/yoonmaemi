import { API_BASE_URL } from "./config";

export type Role = "user" | "assistant";

export interface Message {
  role: Role;
  content: string;
}

export interface ChatResponse {
  summary: string;
  history: Message[];
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const message = (errorBody as { detail?: string }).detail ?? response.statusText;
    throw new Error(`API request failed: ${message}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchHistory(): Promise<Message[]> {
  const response = await fetch(`${API_BASE_URL}/api/history`);
  return handleResponse<Message[]>(response);
}

export async function sendMessage(message: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });
  return handleResponse<ChatResponse>(response);
}

