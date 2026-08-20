import { apiFetch } from "./api";

export interface User {
  id: number;
  username: string;
}

export function getAllUsers() {
  return apiFetch<User[]>("/users/");
}