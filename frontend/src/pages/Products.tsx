import { useEffect, useState } from "react";
import { getProducts, createProduct, deleteProduct, type Product } from "../api/products";



function Products() {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [search, setSearch] = useState("");
    const [minPrice, setMinPrice] = useState("");
    const [maxPrice, setMaxPrice] = useState("");
    const [sortBy, setSortBy] = useState<"price" | "name" | "created_at">("name");
    const [order, setOrder] = useState<"asc" | "desc">("asc");
    const [showAddForm, setShowAddForm] = useState(false);
    const [name, setName] = useState("");
    const [price, setPrice] = useState("");
    const [categoryId, setCategoryId] = useState("");
    const [creating, setCreating] = useState(false);
    const [success, setSuccess] = useState<string | null>(null);

    function loadProducts() {
        setLoading(true);
        setError(null);

        getProducts({
            q: search,
            min_price: minPrice
                ? Number(minPrice)
                : undefined,
            max_price: maxPrice
                ? Number(maxPrice)
                : undefined,
            sort_by: sortBy,
            order: order,
        })
            .then((data) => {
                setProducts(data.products);
            })
            .catch((error) => {
                setError(error.message);
            })
            .finally(() => {
                setLoading(false);
            });
    }

    function resetFilters() {
        setSearch("");
        setMinPrice("");
        setMaxPrice("");
        setSortBy("name");
        setOrder("asc");

        getProducts({
            q: undefined,
            min_price: undefined,
            max_price: undefined,
            sort_by: "name",
            order: "asc",
        })
            .then((data) => {
                setProducts(data.products);
            })
            .catch((error) => {
                setError(error.message);
            });
    }

    function getStockStatus(quantity: number) {
        if (quantity === 0) {
            return {
                label: "Out of Stock",
                className: "bg-red-100 text-red-700",
            };
        }

        if (quantity <= 10) {
            return {
                label: "Low Stock",
                className: "bg-yellow-100 text-yellow-700",
            };
        }

        return {
            label: "In Stock",
            className: "bg-green-100 text-green-700",
        };
    }

    useEffect(() => {
        loadProducts();
    }, []);

    async function handleCreateProduct() {
        try {
            setCreating(true);

            await createProduct({
                name,
                price: Number(price),
                category_id: categoryId ? Number(categoryId) : null,
            });

            setSuccess("Product created successfully");

            setName("");
            setPrice("");
            setCategoryId("");
            setShowAddForm(false);

            const data = await getProducts();
            setProducts(data.products);
        } catch (error) {
            setError(error instanceof Error ? error.message : "Failed to create product");
        } finally {
            setCreating(false);
        }
    }

    async function handleDeleteProduct(id: number) {
        const confirmed = window.confirm(
            "Are you sure you want to delete this product?"
        );

        if (!confirmed) {
            return;
        }

        try {
            await deleteProduct(id);

            setProducts((currentProducts) =>
                currentProducts.filter((product) => product.id !== id)
            );

            setSuccess("Product deleted successfully");
        } catch (error) {
            setError(
                error instanceof Error
                    ? error.message
                    : "Failed to delete product"
            );
        }
    }

    if (loading) {
        return <p>Loading products...</p>;
    }

    if (error) {
        return <p className="text-red-600">{error}</p>;
    }

    return (
        <div>
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-slate-900">
                    Products
                </h1>

                <button
                    onClick={() => setShowAddForm(true)}
                    className="relative z-10 cursor-pointer rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700"
                >
                    + Add Product
                </button>
            </div>

            <p className="mt-2 text-slate-600">
                Manage your products.
            </p>

            {success && (
                <div className="mt-4 rounded-lg bg-green-50 px-4 py-3 text-sm font-medium text-green-700">
                    ✓ {success}
                </div>
            )}

            {showAddForm && (
                <div className="mt-6 rounded-xl bg-white p-6 shadow-sm">
                    <h2 className="text-lg font-semibold text-slate-900">
                        Add Product
                    </h2>

                    <div className="mt-4 grid gap-4 md:grid-cols-3">
                        <input
                            type="text"
                            placeholder="Product name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="rounded-lg border border-slate-300 px-4 py-2 outline-none focus:border-blue-500"
                        />

                        <input
                            type="number"
                            placeholder="Price"
                            value={price}
                            onChange={(e) => setPrice(e.target.value)}
                            className="rounded-lg border border-slate-300 px-4 py-2 outline-none focus:border-blue-500"
                        />

                        <input
                            type="number"
                            placeholder="Category ID"
                            value={categoryId}
                            onChange={(e) => setCategoryId(e.target.value)}
                            className="rounded-lg border border-slate-300 px-4 py-2 outline-none focus:border-blue-500"
                        />
                    </div>

                    <div className="mt-4 flex gap-3">
                        <button
                            onClick={handleCreateProduct}
                            disabled={creating}
                            className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 disabled:opacity-50"
                        >
                            {creating ? "Creating..." : "Create Product"}
                        </button>

                        <button
                            onClick={() => setShowAddForm(false)}
                            className="rounded-lg bg-slate-200 px-4 py-2 font-medium text-slate-700 hover:bg-slate-300"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            )}

            <div className="mt-6 flex flex-wrap gap-3">
                <input
                    type="text"
                    placeholder="Search products..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="min-w-[250px] flex-1 rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-blue-500"
                />

                <input
                    type="number"
                    placeholder="Min price"
                    value={minPrice}
                    onChange={(e) => setMinPrice(e.target.value)}
                    className="w-32 rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-blue-500"
                />

                <input
                    type="number"
                    placeholder="Max price"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                    className="w-32 rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-blue-500"
                />

                <select
                    value={sortBy}
                    onChange={(e) =>
                        setSortBy(
                            e.target.value as "price" | "name" | "created_at"
                        )
                    }
                    className="rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-blue-500"
                >
                    <option value="name">Name</option>
                    <option value="price">Price</option>
                    <option value="created_at">Created date</option>
                </select>

                <select
                    value={order}
                    onChange={(e) =>
                        setOrder(e.target.value as "asc" | "desc")
                    }
                    className="rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-blue-500"
                >
                    <option value="asc">Ascending</option>
                    <option value="desc">Descending</option>
                </select>

                <button
                    onClick={loadProducts}
                    className="rounded-lg bg-blue-600 px-5 py-3 font-medium text-white transition hover:bg-blue-700"
                >
                    Search
                </button>
                <button
                    onClick={resetFilters}
                    className="rounded-lg border border-slate-300 bg-white px-5 py-3 font-medium text-slate-700 transition hover:bg-slate-50"
                >
                    Reset
                </button>
            </div>

            <div className="mt-6">
                {products.length === 0 ? (
                    <div className="mt-8 rounded-xl bg-white p-10 text-center shadow-sm">
                        <div className="text-5xl">
                            📦
                        </div>

                        <h2 className="mt-4 text-lg font-semibold text-slate-900">
                            No products found
                        </h2>

                        <p className="mt-2 text-slate-500">
                            Try changing your search or filters.
                        </p>

                        <button
                            onClick={resetFilters}
                            className="mt-5 rounded-lg bg-blue-600 px-5 py-2.5 font-medium text-white transition hover:bg-blue-700"
                        >
                            Reset Filters
                        </button>
                    </div>
                ) : (
                    <div className="overflow-hidden rounded-lg bg-white shadow-sm">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead className="border-b border-slate-200 bg-slate-50">
                                    <tr>
                                        <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                                            Product
                                        </th>

                                        <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                                            Category
                                        </th>

                                        <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                                            Price
                                        </th>

                                        <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                                            Stock
                                        </th>

                                        <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                                            Status
                                        </th>

                                        <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                                            Created at
                                        </th>
                                        <th className="px-6 py-4 text-sm font-semibold text-slate-700">
                                            Actions
                                        </th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {products.map((product) => {
                                        const stockStatus = getStockStatus(product.stock_quantity);

                                        return (
                                            <tr
                                                key={product.id}
                                                className="border-b border-slate-100 last:border-0 hover:bg-slate-50"
                                            >
                                                <td className="px-6 py-4 font-medium text-slate-900">
                                                    {product.name}
                                                </td>

                                                <td className="px-6 py-4 text-slate-600">
                                                    {product.category?.name ?? "Uncategorized"}
                                                </td>

                                                <td className="px-6 py-4 text-slate-600">
                                                    {product.price} €
                                                </td>

                                                <td className="px-6 py-4 text-slate-600">
                                                    {product.stock_quantity}
                                                </td>

                                                <td className="px-6 py-4">
                                                    <span
                                                        className={`rounded-full px-3 py-1 text-xs font-medium ${stockStatus.className}`}
                                                    >
                                                        {stockStatus.label}
                                                    </span>
                                                </td>

                                                <td className="px-6 py-4 text-slate-600">
                                                    {new Date(product.created_at).toLocaleString("bs-BA", {
                                                        dateStyle: "short",
                                                        timeStyle: "medium",
                                                    })}
                                                </td>
                                                <td className="px-6 py-4">
                                                    <button
                                                        onClick={() => handleDeleteProduct(product.id)}
                                                        className="flex h-9 w-9 items-center justify-center rounded-full bg-red-100 text-red-600 transition-all hover:scale-110 hover:bg-red-600 hover:text-white"
                                                        title="Delete product"
                                                    >
                                                        <span className="text-lg">🗑</span>
                                                    </button>
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Products;
