import { API } from "./conversation";

export async function sendMessage(
    conversationId: string, question: string,
) {
    const response = await fetch(
        `${API}/chat/${conversationId}`,{
            method: "POST", headers: {
                "Content-Type": "application/json",
            }, body: JSON.stringify({ question }),
        }
    );

    return response.json();
}