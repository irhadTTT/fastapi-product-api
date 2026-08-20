import { apiFetch } from "./api";

export interface InventoryItem {
  id: number;
  product_id: number;
  quantity: number;
}

export function getInventory() {
  return apiFetch<InventoryItem[]>("/inventory");
}


export interface StockMovement {
  id: number;
  product_id: number;
  product: {
    id: number;
    name: string;
  };
  user_id: number;
  type: "IN" | "OUT";
  quantity: number;
  note: string | null;
  created_at: string;
}

export function getStockMovements() {
  return apiFetch<StockMovement[]>("/stock-movements/");
}

export interface CreateStockMovementRequest {
  product_id: number;
  type: "IN" | "OUT";
  quantity: number;
  note: string;
}

export function createStockMovement(
  data: CreateStockMovementRequest,
  idempotencyKey: string
) {
  return apiFetch<StockMovement>("/stock-movements/", {
    method: "POST",
    headers: {
      "Idempotency-Key": idempotencyKey,
    },
    body: JSON.stringify(data),
  });
}

export function getStockMovementsByProduct(productId: number) {
  return apiFetch<StockMovement[]>(
    `/stock-movements/product/${productId}`
  );
}

export function getStockMovementsByUser(userId: number) {
  return apiFetch<StockMovement[]>(
    `/stock-movements/user/${userId}`
  );
}

export interface User {
  id: number;
  username: string;
}

export function getAllUsers() {
  return apiFetch<User[]>("/users/");
}