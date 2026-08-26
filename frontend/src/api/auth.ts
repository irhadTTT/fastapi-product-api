import { apiFetch } from "./api";

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export function login(credentials: LoginRequest) {
  const body = new URLSearchParams();

  body.append("username", credentials.username);
  body.append("password", credentials.password);
  body.append("grant_type", "password");

  return apiFetch<LoginResponse>("/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });
}

export interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
}

const API_URL = import.meta.env.VITE_API_URL;

export async function refreshAccessToken(
  refreshToken: string
): Promise<RefreshTokenResponse> {
  const response = await fetch(
    `${API_URL}/refresh-access-token/refresh`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refresh_token: refreshToken,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Refresh token failed");
  }

  return response.json();
}

export function verifyEmail(token: string) {
  return apiFetch<{ message: string }>(
    `/auth/verify-email?token=${encodeURIComponent(token)}`
  );
}