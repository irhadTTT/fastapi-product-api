import {
    getAccessToken,
    getRefreshToken,
    updateAccessToken,
} from "../auth/authStorage";

import { refreshAccessToken } from "./auth";

const API_URL = import.meta.env.VITE_API_URL;

async function request(
    endpoint: string,
    options?: RequestInit
) {
    const token = getAccessToken();

    return fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",

            ...(token
                ? {
                    Authorization: `Bearer ${token}`,
                }
                : {}),

            ...options?.headers,
        },
    });
}

export async function apiFetch<T>(
    endpoint: string,
    options?: RequestInit
): Promise<T> {
    let response = await request(endpoint, options);

    console.log("FIRST REQUEST:", response.status);

    if (response.status === 401) {
        console.log("401 - REFRESHING TOKEN");

        const refreshToken = getRefreshToken();

        if (!refreshToken) {
            throw new Error("No refresh token available");
        }

        const refreshResponse =
            await refreshAccessToken(refreshToken);

        console.log("NEW ACCESS TOKEN RECEIVED");

        updateAccessToken(refreshResponse.access_token);

        response = await request(endpoint, options);

        console.log("RETRY REQUEST:", response.status);
    }

    if (!response.ok) {
        throw new Error(
            `API request failed: ${response.status}`
        );
    }

    if (response.status === 204) {
        return undefined as T;
    }

    return response.json();
}