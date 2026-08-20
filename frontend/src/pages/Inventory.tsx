import { useEffect, useState } from "react";
import {
  getStockMovements,
  createStockMovement,
  getStockMovementsByProduct,
  getStockMovementsByUser,
  type StockMovement,
} from "../api/inventory";

import {
  getAllProducts,
  type Product,
} from "../api/products";

import {
  getAllUsers,
  type User,
} from "../api/users";

export default function Inventory() {
  const [movements, setMovements] = useState<StockMovement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [productId, setProductId] = useState<number | "">("");
  const [movementType, setMovementType] = useState<"IN" | "OUT">("IN");
  const [quantity, setQuantity] = useState("");
  const [note, setNote] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<number | "">("");
  const [filterLoading, setFilterLoading] = useState(false);
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<number | "">("");

  useEffect(() => {
    getAllProducts()
      .then(setProducts)
      .catch(() => setError("Failed to load products"));
  }, []);

  useEffect(() => {
    getStockMovements()
      .then(setMovements)
      .catch(() => setError("Failed to load inventory"))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    getAllUsers()
      .then(setUsers)
      .catch(() => setError("Failed to load users"));
  }, []);

  async function handleCreate() {
    if (!productId) {
      setError("Please select a product.");
      return;
    }

    if (!quantity || Number(quantity) <= 0) {
      setError("Quantity must be greater than 0.");
      return;
    }

    try {
      setIsCreating(true);
      setError(null);

      const idempotencyKey = crypto.randomUUID();

      const newMovement = await createStockMovement({
        product_id: Number(productId),
        type: movementType,
        quantity: Number(quantity),
        note: note.trim()
      },
        idempotencyKey
      );

      setMovements((current) => [newMovement, ...current]);

      setProductId("");
      setMovementType("IN");
      setQuantity("");
      setNote("");

      setIsCreateModalOpen(false);
    } catch {
      setError("Failed to create stock movement.");
    } finally {
      setIsCreating(false);
    }
  };

  async function handleProductFilter(productId: number | "") {
    setSelectedProduct(productId);

    if (productId === "") {
      const data = await getStockMovements();
      setMovements(data);
      setFilterLoading(false);
      return;
    }

    setFilterLoading(true);
    setError(null);

    try {
      const data = await getStockMovementsByProduct(productId);
      setMovements(data);
    } catch {
      setError("Failed to load product movements");
    } finally {
      setFilterLoading(false);
    }
  }

  async function handleUserFilter(userId: number | "") {
    setSelectedUser(userId);
    setFilterLoading(true);
    setError(null);

    try {
      if (userId === "") {
        const data = await getStockMovements();
        setMovements(data);
      } else {
        const data = await getStockMovementsByUser(userId);
        setMovements(data);
      }
    } catch {
      setError(
        userId === ""
          ? "Failed to load inventory"
          : "Failed to load user movements"
      );
    } finally {
      setFilterLoading(false);
    }
  }

  if (loading) {
    return <div>Loading inventory...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            Inventory
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Track stock movements and inventory changes.
          </p>
        </div>

        <button
          type="button"
          onClick={() => {
            setFormError(null);
            setIsCreateModalOpen(true);
          }}
          className="rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm transition hover:bg-blue-700"
        >
          Add Stock Movement
        </button>
      </div>

      {isCreateModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
          <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                Add Stock Movement
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Record a new inventory movement.
              </p>
            </div>

            {formError && (
              <div className="mb-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
                {formError}
              </div>
            )}

            <div className="mb-4">
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Product
              </label>

              <select
                value={productId}
                onChange={(e) =>
                  setProductId(
                    e.target.value ? Number(e.target.value) : ""
                  )
                }
                className="w-full rounded-lg border border-gray-300 bg-white px-3 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              >
                <option value="">Select product</option>

                {products.map((product) => (
                  <option key={product.id} value={product.id}>
                    {product.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="mb-4">
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Movement Type
              </label>

              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setMovementType("IN")}
                  className={`rounded-lg border px-4 py-2.5 text-sm font-medium transition ${movementType === "IN"
                    ? "border-green-500 bg-green-50 text-green-700"
                    : "border-gray-300 text-gray-600 hover:bg-gray-50"
                    }`}>
                  Stock In
                </button>

                <button
                  type="button"
                  onClick={() => setMovementType("OUT")}
                  className={`rounded-lg border px-4 py-2.5 text-sm font-medium transition ${movementType === "OUT"
                    ? "border-red-500 bg-red-50 text-red-700"
                    : "border-gray-300 text-gray-600 hover:bg-gray-50"
                    }`}
                >
                  Stock Out
                </button>
              </div>
            </div>

            <div className="mb-4">
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Quantity
              </label>

              <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                placeholder="Enter quantity"
                className="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <div className="mb-6">
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Note
              </label>

              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="Optional note"
                rows={3}
                className="w-full resize-none rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <div className="flex justify-end gap-3">
              <button
                type="button"
                onClick={() => {
                  setIsCreateModalOpen(false);
                  setFormError(null);
                  setProductId("");
                  setMovementType("IN");
                  setQuantity("");
                  setNote("");
                }}
                className="rounded-lg border border-gray-300 px-4 py-2.5 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
              >
                Cancel
              </button>

              <button
                type="button"
                onClick={handleCreate}
                disabled={
                  isCreating ||
                  !productId ||
                  !quantity ||
                  Number(quantity) <= 0
                }
                className="rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isCreating ? "Creating..." : "Create"}
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-gray-500">
            Total Movements
          </p>

          <p className="mt-2 text-2xl font-semibold text-gray-900">
            {movements.length}
          </p>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-gray-500">
            Stock In
          </p>

          <p className="mt-2 text-2xl font-semibold text-green-600">
            {movements.filter((movement) => movement.type === "IN").length}
          </p>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
          <p className="text-sm text-gray-500">
            Stock Out
          </p>

          <p className="mt-2 text-2xl font-semibold text-red-600">
            {movements.filter((movement) => movement.type === "OUT").length}
          </p>
        </div>
      </div>

      <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4">
        <div>
          <h2 className="font-semibold text-gray-900">
            Stock Movements
          </h2>

          <p className="mt-1 text-sm text-gray-500">
            Recent inventory activity.
          </p>
        </div>

        <select
          value={selectedProduct}
          onChange={(e) =>
            handleProductFilter(
              e.target.value ? Number(e.target.value) : ""
            )
          }
          disabled={filterLoading}
          className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 outline-none transition focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
        >
          <option value="">All Products</option>

          {products.map((product) => (
            <option key={product.id} value={product.id}>
              {product.name}
            </option>
          ))}
        </select>

                <select
          value={selectedUser}
          onChange={(e) =>
            handleUserFilter(
              e.target.value ? Number(e.target.value) : ""
            )
          }
          disabled={filterLoading}
          className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 outline-none transition focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
        >
          <option value="">All Users</option>

          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.username}
            </option>
          ))}
        </select>
      </div>
      <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
        <div className="border-b border-gray-200 px-6 py-4">
          <h2 className="font-semibold text-gray-900">
            Stock Movements
          </h2>

          <p className="mt-1 text-sm text-gray-500">
            Recent inventory activity.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Product
                </th>

                <th className="px-6 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Type
                </th>

                <th className="px-6 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Quantity
                </th>

                <th className="px-6 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Note
                </th>

                <th className="px-6 py-3 text-xs font-semibold uppercase tracking-wide text-gray-500">
                  Date
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-gray-100">
              {movements.map((movement) => (
                <tr
                  key={movement.id}
                  className="transition hover:bg-gray-50"
                >

                  <td className="px-6 py-4">
                    <div>
                      <p className="font-medium text-gray-900">
                        {movement.product.name}
                      </p>

                      <p className="text-xs text-gray-500">
                        Product #{movement.product.id}
                      </p>
                    </div>
                  </td>

                  <td className="px-6 py-4">
                    {movement.type === "IN" ? (
                      <span className="inline-flex items-center rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700">
                        IN
                      </span>
                    ) : (
                      <span className="inline-flex items-center rounded-full bg-red-50 px-2.5 py-1 text-xs font-medium text-red-700">
                        OUT
                      </span>
                    )}
                  </td>

                  <td className="px-6 py-4">
                    <span
                      className={
                        movement.type === "IN"
                          ? "font-semibold text-green-600"
                          : "font-semibold text-red-600"
                      }
                    >
                      {movement.type === "IN" ? "+" : "-"}
                      {movement.quantity}
                    </span>
                  </td>

                  <td className="max-w-xs px-6 py-4">
                    <span className="text-sm text-gray-600">
                      {movement.note || "-"}
                    </span>
                  </td>

                  <td className="px-6 py-4 text-sm text-gray-500">
                    {new Date(
                      movement.created_at
                    ).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {movements.length === 0 && (
          <div className="px-6 py-12 text-center">
            <p className="font-medium text-gray-900">
              No stock movements
            </p>

            <p className="mt-1 text-sm text-gray-500">
              Stock movements will appear here.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}