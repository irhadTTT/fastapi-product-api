import { useEffect, useState } from "react";
import { getCategories, deleteCategory, createCategory, type Category } from "../api/categories";

export default function Categories() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [categoryName, setCategoryName] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    getCategories()
      .then(setCategories)
      .catch(() => setError("Failed to load categories"))
      .finally(() => setLoading(false));
  }, []);

  async function handleCreate() {
    if (!categoryName.trim()) {
      return;
    }

    try {
      setIsCreating(true);

      const newCategory = await createCategory({
        name: categoryName.trim()
      });

      setSuccess("Category created successfully");

      setCategories((current) => [...current, newCategory]);

      setCategoryName("");
      setIsCreateModalOpen(false);

    } catch {
      setError("Failed to create category");
    } finally {
      setIsCreating(false);
    }
  };


  async function handleDelete(id: number) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this categor?"
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteCategory(id);

      setSuccess("Category deleted successfully");

      setCategories((current) =>
        current.filter((category) => category.id !== id)
      );
    } catch {
      setError("Failed to delete category");
    }
  };

  if (loading) {
    return <p>Loading categories...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold">Categories</h1>

        {success && (
          <div className="mt-4 rounded-lg bg-green-50 px-4 py-3 text-sm font-medium text-green-700">
            ✓ {success}
          </div>
        )}

        <button onClick={() => setIsCreateModalOpen(true)}
          className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700">
          Add Category
        </button>
      </div>

      {isCreateModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
            <h2 className="mb-4 text-xl font-semibold">
              Add Category
            </h2>

            <label className="mb-2 block text-sm font-medium text-gray-700">
              Category name
            </label>

            <input
              type="text"
              value={categoryName}
              onChange={(e) => setCategoryName(e.target.value)}
              placeholder="Enter category name"
              className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none focus:border-blue-500"
            />

            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => {
                  setIsCreateModalOpen(false);
                  setCategoryName("");
                }}
                className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>

              <button
                onClick={handleCreate}
                disabled={isCreating || !categoryName.trim()}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isCreating ? "Creating..." : "Create"}
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="overflow-hidden rounded-lg border border-gray-200">
        <table className="w-full text-left">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">
                ID
              </th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">
                Name
              </th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600 text-right">
                Actions
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-200">
            {categories.map((category) => (
              <tr key={category.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-sm">
                  {category.id}
                </td>

                <td className="px-6 py-4 text-sm font-medium">
                  {category.name}
                </td>

                <td className="px-6 py-4 text-right">
                  <button onClick={() => handleDelete(category.id)}
                    className="rounded-lg border border-red-400 px-3 py-2 text-sm font-medium text-red-600 transition hover:bg-red-200">
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}