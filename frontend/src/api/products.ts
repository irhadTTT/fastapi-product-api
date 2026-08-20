import { apiFetch } from "./api";

export interface Category {
    id: number;
    name: string;
}

export interface Product {
    id: number;
    name: string;
    price: number;
    image_url: string | null;
    stock_quantity: number;
    category: Category;
    created_at: string;
}

export interface ProductsResponse {
    products: Product[];
    page: number;
    limit: number;
    total: number;
    total_pages: number;
}

export interface ProductFilters {
    q?: string;
    min_price?: number;
    max_price?: number;
    sort_by?: "price" | "name" | "created_at";
    order?: "asc" | "desc";
}

export function getProducts(filters: ProductFilters = {}) {
    const params = new URLSearchParams();

    if (filters.q) {
        params.append("q", filters.q);
    }

    if (filters.min_price !== undefined) {
        params.append("min_price", filters.min_price.toString());
    }

    if (filters.max_price !== undefined) {
        params.append("max_price", filters.max_price.toString());
    }

    if (filters.sort_by) {
        params.append("sort_by", filters.sort_by);
    }

    if (filters.order) {
        params.append("order", filters.order);
    }

    const query = params.toString();

    return apiFetch<ProductsResponse>(
        `/products/${query ? `?${query}` : ""}`
    );
}


export interface CreateProductRequest {
  name: string;
  price: number;
  category_id?: number | null;
}

export function createProduct(data: CreateProductRequest) {
  return apiFetch<Product>("/products/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function deleteProduct(id: number) {
  return apiFetch<void>(`/products/${id}`, {
    method: "DELETE",
  });
}

export function getAllProducts() {
  return apiFetch<Product[]>("/products/all");
}