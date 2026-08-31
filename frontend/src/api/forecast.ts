import { apiFetch } from "./api";

export interface DemandForecastItem {
    date: string;
    predicted_demand: number;
}

export interface DemandForecastResponse {
    product_id: number;
    forecast_days: number;
    predictions: DemandForecastItem[];
    total_predicted_demand: number;
}

export async function forecastProductDemand(
    productId: number
){
    return apiFetch<DemandForecastResponse>(
        `/forecast/products/${productId}`
    );
}



