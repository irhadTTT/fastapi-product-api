import { apiFetch } from "./api";

export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  is_verified: boolean;
}

export interface UsersResponse {
  users: User[];
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}

export interface CreateUserRequest{
  username: string;
  email: string;
  password: string;
}


export function getAllUsers() {
  return apiFetch<User[]>("/users/all");
}

export function getUsers(
  page: number = 1, 
  limit: number = 10
) {
  return apiFetch<UsersResponse>(
    `/users/?page=${page}&limit=${limit}`
  );
}

export function createUser(data: CreateUserRequest) {
  return apiFetch<User>("/users/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function deleteUser(id: number) {
    return apiFetch<void>(`/users/${id}`, {
        method: "DELETE",
    });
}

export function changeRole(userId: number, role: string) {
  return apiFetch<User>(
    `/users/${userId}/role?role=${encodeURIComponent(role)}`,
    {
      method: "PUT"
    }
  );
}

export function resetPassword(
  userId: number,
  newPassword: string
) {
  return apiFetch<User>(
    `/users/${userId}/reset-password`,
    {
      method: "PUT",
      body: JSON.stringify({
        new_password: newPassword,
      }),
    }
  );
}