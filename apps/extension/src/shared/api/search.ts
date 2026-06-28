import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000/api/v1"
});

export async function search(query: string) {
    const response = await api.post("/search", { query });

    return response.data;
}