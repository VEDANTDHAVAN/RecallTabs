import axios from "axios";
const API_BASE_URL="http://localhost:8000";

export const api = axios.create({
    baseURL: `${API_BASE_URL}/api/v1`,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
    }
});

export async function apiFetch(
    path: string, options?: RequestInit 
) {
    const response = await fetch(
        `${API_BASE_URL}${path}`, {
            ...options, headers: {
                "Content-Type": "application/json",
                ...(options?.headers || {}),
            },
        }
    );

    if (!response.ok) {
        const text = await response.text();

        throw new Error(
            `API Error ${response.status}: ${text}`
        );
    }

    return response.json();
}