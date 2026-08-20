import { apiFetch } from "./api";

export interface Category {
  id: number;
  name: string;
  description?: string;
}

export function getCategories() {
  return apiFetch<Category[]>("/categories");
}