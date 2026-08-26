import { apiFetch } from "./api";


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

export interface StockMovementsResponse {
  movements: StockMovement[];
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}

export function getStockMovements(
  page: number = 1, 
  limit: number = 10
) {
  return apiFetch<StockMovementsResponse>(
    `/stock-movements/?page=${page}&limit=${limit}`
  );
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
