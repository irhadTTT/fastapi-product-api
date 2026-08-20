import { apiFetch } from "./api";

export interface InventoryItem {
  id: number;
  product_id: number;
  quantity: number;
}

export function getInventory() {
  return apiFetch<InventoryItem[]>("/inventory");
}