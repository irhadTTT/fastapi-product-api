import { apiFetch } from "./api";

export interface Category {
  id: number;
  name: string;
}

export interface CreateCategoryRequest {
  name: string;
}

export function getCategories() {
  return apiFetch<Category[]>("/categories/");
}

export function deleteCategory(id: number) {
  return apiFetch<void>(`/categories/${id}`, {
    method: "DELETE",
  });
}

export function createCategory(data: CreateCategoryRequest) {
  return apiFetch<Category>("/categories/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}