import { api } from "./client";

export async function searchTabs(query: string) {
    const response = await api.post(
        "/search", { query }
    );

    return response.data;
}

export async function askRecall(question: string) {
    const response = await api.post(
        "/ask", { question }
    );

    return response.data;
}

export async function getTopics() {
    const response = await api.get("/topics");

    return response.data;
}