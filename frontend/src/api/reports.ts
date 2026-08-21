import { apiFetch, downloadReport } from "./api";

export interface InventoryReport {
  total_products: number;
  total_stock_units: number;
  low_stock_products: number;
  out_of_stock_products: number;
  inventory_value: number;
}

export function getReport() {
  return apiFetch<InventoryReport>("/reports/");
}

export function exportInventoryCsv() {
  return downloadReport(
    "/reports/export/csv"
  );
}

export function exportInventoryExcel() {
  return downloadReport(
    "/reports/report/export"
  );
}