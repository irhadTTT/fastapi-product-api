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


export async function downloadReport(endpoint: string) {
  const token = getAccessToken();

  const response = await fetch(`${API_URL}${endpoint}`, {
    headers: {
      ...(token
        ? {
            Authorization: `Bearer ${token}`,
          }
        : {}),
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to download report: ${response.status}`);
  }

  const blob = await response.blob();

  const url = window.URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;

  const contentDisposition = response.headers.get("Content-Disposition");

  const fileName = contentDisposition?.match(/filename=([^;]+)/)?.[1] ?? "download";

  console.log("Content-Disposition:", response.headers.get("Content-Disposition"));

  link.download = fileName;
  document.body.appendChild(link);
  link.click();

  link.remove();
  window.URL.revokeObjectURL(url);
}
