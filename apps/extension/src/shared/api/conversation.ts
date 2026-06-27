import { API_BASE_URL } from "../constants"

export const API = `${API_BASE_URL}/api/v1`;

export async function createConversation() {
    const res = await fetch(`${API}/conversations`, {
        method: "POST",
    });

    return res.json();
}

export async function listConversations() {
    const res = await fetch(`${API}/conversations`);

    return res.json();
}

export async function getMessages(id: string) {
    const res = await fetch(`${API}/conversations/${id}/messages`);

    return res.json();
} 