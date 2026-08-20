import { useEffect, useState } from "react";
import { getReport, type InventoryReport } from "../api/reports";
import { useNavigate } from "react-router-dom";

function Dashboard() {
    const [report, setReport] = useState<InventoryReport | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        getReport()
            .then((data) => {
                setReport(data);
            })
            .catch((error) => {
                setError(error.message);
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <p>Loading dashboard...</p>;
    }

    if (error) {
        return <p className="text-red-600">{error}</p>;
    }

    if (!report) {
        return null;
    }

    return (
        <div>
            <h1 className="text-3xl font-bold text-slate-900">
                Dashboard
            </h1>

            <p className="mt-2 text-slate-600">
                Overview of your inventory.
            </p>

            <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-5">
                <div onClick={() => navigate("/products")}
                    className="cursor-pointer rounded-xl bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md">
                    <p className="text-sm font-medium text-slate-500">
                        Total Products
                    </p>

                    <p className="mt-2 text-3xl font-bold text-slate-900">
                        {report.total_products}
                    </p>
                </div>
                <div className="rounded-xl bg-white p-6 shadow-sm">
                    <p className="text-sm font-medium text-slate-500">
                        Stock Units
                    </p>

                    <p className="mt-2 text-3xl font-bold text-slate-900">
                        {report.total_stock_units}
                    </p>
                </div>

                <div
                    onClick={() => navigate("/products")}
                    className="cursor-pointer rounded-xl bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                >
                    <p className="text-sm font-medium text-slate-500">
                        Low Stock
                    </p>

                    <p className="mt-2 text-3xl font-bold text-yellow-600">
                        {report.low_stock_products}
                    </p>
                </div>

                <div
                    onClick={() => navigate("/products")}
                    className="cursor-pointer rounded-xl bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                >
                    <p className="text-sm font-medium text-slate-500">
                        Out of Stock
                    </p>

                    <p className="mt-2 text-3xl font-bold text-red-600">
                        {report.out_of_stock_products}
                    </p>
                </div>

                <div className="rounded-xl bg-white p-6 shadow-sm">
                    <p className="text-sm font-medium text-slate-500">
                        Inventory Value
                    </p>

                    <p className="mt-2 text-3xl font-bold text-blue-600">
                        {report.inventory_value.toLocaleString("bs-BA")} €
                    </p>
                </div>
            </div>
            <div className="mt-8 rounded-xl bg-white p-6 shadow-sm">
                <h2 className="text-lg font-semibold text-slate-900">
                    Inventory Alerts
                </h2>

                <div className="mt-4 space-y-3">
                    <div className="flex items-center justify-between rounded-lg bg-red-50 p-4">
                        <div>
                            <p className="font-medium text-red-700">
                                Out of Stock
                            </p>

                            <p className="text-sm text-red-600">
                                Products with no available stock
                            </p>
                        </div>

                        <span className="text-2xl font-bold text-red-700">
                            {report.out_of_stock_products}
                        </span>
                    </div>

                    <div className="flex items-center justify-between rounded-lg bg-yellow-50 p-4">
                        <div>
                            <p className="font-medium text-yellow-700">
                                Low Stock
                            </p>

                            <p className="text-sm text-yellow-600">
                                Products that need restocking
                            </p>
                        </div>

                        <span className="text-2xl font-bold text-yellow-700">
                            {report.low_stock_products}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;