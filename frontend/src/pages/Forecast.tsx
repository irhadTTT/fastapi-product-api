import { useEffect, useState } from "react";
import { getAllProducts, type Product } from "../api/products";
import {
    forecastProductDemand,
    type DemandForecastResponse,
} from "../api/forecast";

function Forecast() {
    const [products, setProducts] = useState<Product[]>([]);
    const [selectedProductId, setSelectedProductId] = useState("");
    const [forecast, setForecast] = useState<DemandForecastResponse | null>(null);

    const [loadingProducts, setLoadingProducts] = useState(true);
    const [loadingForecast, setLoadingForecast] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        getAllProducts()
            .then(setProducts)
            .catch((error) => {
                setError(
                    error instanceof Error
                        ? error.message
                        : "Failed to load products"
                );
            })
            .finally(() => {
                setLoadingProducts(false);
            });
    }, []);

    async function handleForecast() {
        if (!selectedProductId) {
            setError("Please select a product.");
            return;
        }

        try {
            setLoadingForecast(true);
            setError(null);
            setForecast(null);

            const data = await forecastProductDemand(
                Number(selectedProductId)
            );

            setForecast(data);
        } catch (error) {
            setError(
                error instanceof Error
                    ? error.message
                    : "Failed to generate forecast"
            );
        } finally {
            setLoadingForecast(false);
        }
    }

    return (
        <div>
            <h1 className="text-3xl font-bold text-slate-900">
                Demand Forecast
            </h1>

            <p className="mt-2 text-slate-600">
                Predict future product demand using historical stock data.
            </p>

            <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">
                <h2 className="text-lg font-semibold text-slate-900">
                    Generate Forecast
                </h2>

                <div className="mt-4 flex flex-wrap gap-3">
                    <select
                        value={selectedProductId}
                        onChange={(e) =>
                            setSelectedProductId(e.target.value)
                        }
                        disabled={loadingProducts}
                        className="min-w-[250px] rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-blue-500"
                    >
                        <option value="">
                            {loadingProducts
                                ? "Loading products..."
                                : "Select a product"}
                        </option>

                        {products.map((product) => (
                            <option
                                key={product.id}
                                value={product.id}
                            >
                                {product.name}
                            </option>
                        ))}
                    </select>

                    <button
                        onClick={handleForecast}
                        disabled={loadingForecast || !selectedProductId}
                        className="rounded-lg bg-blue-600 px-5 py-3 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {loadingForecast
                            ? "Generating..."
                            : "Generate Forecast"}
                    </button>
                </div>
            </div>

            {error && (
                <div className="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
                    {error}
                </div>
            )}

            {forecast && (
                <>
                    <div className="mt-6 grid gap-4 md:grid-cols-3">
                        <div className="rounded-xl bg-white p-6 shadow-sm">
                            <p className="text-sm text-slate-500">
                                Forecast Days
                            </p>

                            <p className="mt-2 text-3xl font-bold text-slate-900">
                                {forecast.forecast_days}
                            </p>
                        </div>

                        <div className="rounded-xl border border-blue-100 bg-blue-50 p-6 shadow-sm">
                            <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">
                                Total Predicted Demand
                            </p>

                            <p className="mt-3 text-4xl font-bold text-blue-700">
                                {forecast.total_predicted_demand}
                            </p>
                        </div>

                        <div className="rounded-xl bg-white p-6 shadow-sm">
                            <p className="text-sm text-slate-500">
                                Product ID
                            </p>

                            <p className="mt-2 text-3xl font-bold text-slate-900">
                                #{forecast.product_id}
                            </p>
                        </div>
                    </div>

                    <div className="mt-6 overflow-hidden rounded-xl bg-white shadow-sm">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead className="border-b border-slate-200 bg-slate-50">
                                    <tr>
                                        <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                                            Date
                                        </th>

                                        <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                                            Predicted Demand
                                        </th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {forecast.predictions.map((prediction) => (
                                        <tr
                                            key={prediction.date}
                                            className="border-b border-slate-100 last:border-0 hover:bg-slate-50"
                                        >
                                            <td className="px-6 py-4 text-slate-600">
                                                {prediction.date}
                                            </td>

                                            <td className="px-6 py-4 font-medium text-slate-900">
                                                {prediction.predicted_demand}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}

export default Forecast;
