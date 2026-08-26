import { useEffect, useState } from "react";
import {
  getUsers,
  createUser,
  deleteUser,
  changeRole,
  resetPassword,
  type User
} from "../api/users";

export default function Users() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [deleteUserId, setDeleteUserId] = useState<number | null>(null);
  const [newPassword, setNewPassword] = useState("");
  const [showResetModal, setShowResetModal] = useState(false);
  const [resetUser, setResetUser] = useState<User | null>(null);
  const [resetting, setResetting] = useState(false);
  const [resetError, setResetError] = useState<string | null>(null);

  const pageSize = 10;

  function loadUsers(page: number) {
    setLoading(true);
    setError(null);

    getUsers(page, pageSize)
      .then((data) => {
        setUsers(data.users)
        setCurrentPage(data.page);
        setTotalPages(data.total_pages);
      })
      .catch(() => setError("Failed to load users"))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadUsers(1)
  }, []);

  async function handleCreateUser() {

    if (!username.trim()) {
      return;
    }
    if (!email.trim()) {
      return;
    }
    if (!password.trim()) {
      return;
    }

    try {
      setCreating(true);
      setCreateError(null);

      await createUser({
        username: username.trim(),
        email: email.trim(),
        password: password.trim()
      });

      setShowCreateModal(false);

      setUsername("");
      setEmail("");
      setPassword("");

      loadUsers(currentPage);
    } catch (error) {
      setCreateError(error instanceof Error ? error.message : "Failed to create user");
    } finally {
      setCreating(false);
    }
  }

  async function handleDeleteUser() {
    if (deleteUserId === null) {
      return;
    }

    try {
      await deleteUser(deleteUserId);

      const remainingUsers = users.filter(
        (user) => user.id !== deleteUserId
      );

      setUsers(remainingUsers);
      setSuccess("User deleted successfully");

      setDeleteUserId(null);

      if (remainingUsers.length === 0 && currentPage > 1)
        loadUsers(currentPage - 1);
      else
        loadUsers(currentPage);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to delete this user");
    }
  }

  async function handleChangeRole(userId: number, role: string) {
    try {
      await changeRole(userId, role);

      setSuccess("User role updated successfully");

      loadUsers(currentPage);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to change user role");
    }
  }

  async function handleResetPassword() {
    if (!resetUser || !newPassword.trim()) {
      return;
    }

    try {
      setResetting(true);
      setResetError(null);

      await resetPassword(
        resetUser.id,
        newPassword.trim()
      );

      setSuccess("Password reset successfully");

      setNewPassword("");
      setResetUser(null);
      setShowResetModal(false);
    } catch (error) {
      setResetError(error instanceof Error ? error.message : "Failed to reset password");
    } finally {
      setResetting(false);
    }
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold text-gray-900">
            Users
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Manage users and their roles
          </p>
        </div>

        <button
          onClick={() => {
            setCreateError(null);
            setShowCreateModal(true);
          }}
          className="relative z-10 cursor-pointer rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700"
        >
          + Create User
        </button>
      </div>
      {error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-600">
          {error}
        </div>
      )}

      {success && (
        <div className="mb-4 rounded-lg border border-green-200 bg-green-50 p-4 text-sm text-green-600">
          {success}
        </div>
      )}

      <div className="rounded-xl border border-gray-200 bg-white shadow-sm">
        {loading ? (
          <div className="p-6 text-sm text-gray-500">
            Loading users...
          </div>
        ) : (
          <>
            {users.length === 0 ? (
              <div className="px-6 py-12 text-center">
                <p className="font-medium text-gray-900">
                  No users found
                </p>

                <p className="mt-1 text-sm text-gray-500">
                  Users will appear here.
                </p>
              </div>
            ) : (
              <>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="border-b border-gray-200 bg-gray-50">
                      <tr>
                        <th className="px-6 py-4 font-medium text-gray-600">
                          User
                        </th>

                        <th className="px-6 py-4 font-medium text-gray-600">
                          Email
                        </th>

                        <th className="px-6 py-4 font-medium text-gray-600">
                          Role / Change
                        </th>

                        <th className="px-6 py-4 font-medium text-gray-600">
                          Is verified
                        </th>
                        <th className="px-6 py-4 font-medium text-gray-600">
                          Actions
                        </th>
                      </tr>
                    </thead>

                    <tbody className="divide-y divide-gray-100">
                      {users.map((user) => (
                        <tr
                          key={user.id}
                          className="hover:bg-gray-50"
                        >
                          <td className="px-6 py-4 font-medium text-gray-900">
                            {user.username ?? "—"}
                          </td>

                          <td className="px-6 py-4 text-gray-600">
                            {user.email}
                          </td>

                          <td className="px-6 py-4">
                            <select
                              value={user.role}
                              onChange={(event) => handleChangeRole(user.id, event.target.value)}
                              className="rounded-full border border-gray-200 bg-gray-50 px-3 py-1.5 text-xs font-medium text-gray-700 outline-none transition hover:bg-green-300 focus:border-blue-400 focus:ring-2 focus:ring-blue-200"
                            >
                              <option value="user">User</option>
                              <option value="admin">Admin</option>
                            </select>
                          </td>

                          <td className="px-6 py-4 text-gray-500">
                            {user.is_verified ? (
                              <span className="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
                                ✓ Verified
                              </span>
                            ) : (
                              <span className="inline-flex items-center rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-500">
                                Not verified
                              </span>
                            )}
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-2">
                              <button
                                onClick={() => setDeleteUserId(user.id)}
                                className="flex h-9 w-9 items-center justify-center rounded-full bg-red-100 text-red-600 transition-all hover:scale-110 hover:bg-red-600 hover:text-white"
                                title="Delete user"
                              >
                                <span className="text-lg">🗑</span>
                              </button>
                              <button
                                onClick={() => {
                                  setResetUser(user);
                                  setResetError(null);
                                  setNewPassword("");
                                  setShowResetModal(true);
                                }}
                                className="mr-2 rounded-full bg-blue-100 px-3 py-2 text-blue-600 transition hover:bg-blue-600 hover:text-white"
                                title="Reset password"
                              >
                                🔑
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {deleteUserId !== null && (
                  <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
                    <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">

                      <h2 className="text-lg font-semibold text-gray-900">
                        Delete User?
                      </h2>

                      <p className="mt-2 text-sm text-gray-500">
                        Are you sure you want to delete this user?
                        This action cannot be undone.
                      </p>

                      <div className="mt-6 flex justify-end gap-3">
                        <button
                          onClick={() => setDeleteUserId(null)}
                          className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                        >
                          Cancel
                        </button>

                        <button
                          onClick={handleDeleteUser}
                          className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
                        >
                          Delete
                        </button>
                      </div>

                    </div>
                  </div>
                )}

                <div className="flex items-center justify-between border-t border-gray-200 px-6 py-4">
                  <button
                    onClick={() => loadUsers(currentPage - 1)}
                    disabled={currentPage === 1 || loading}
                    className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    Previous
                  </button>

                  <span className="text-sm text-gray-600">
                    Page {currentPage} of {totalPages}
                  </span>

                  <button
                    onClick={() => loadUsers(currentPage + 1)}
                    disabled={
                      currentPage === totalPages || loading
                    }
                    className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    Next
                  </button>
                </div>

                {showCreateModal && (
                  <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
                    <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
                      <div className="mb-6 flex items-center justify-between">
                        <div>
                          <h2 className="text-lg font-semibold text-gray-900">
                            Create User
                          </h2>

                          <p className="mt-1 text-sm text-gray-500">
                            Add a new user to the system.
                          </p>
                        </div>

                        <button
                          type="button"
                          onClick={() => setShowCreateModal(false)}
                          disabled={creating}
                          className="text-2xl leading-none text-gray-400 transition hover:text-gray-600 disabled:opacity-50"
                        >
                          ×
                        </button>
                      </div>

                      {createError && (
                        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
                          {createError}
                        </div>
                      )}

                      <form onSubmit={(event) => {
                        event.preventDefault();
                        handleCreateUser();
                      }}>
                        <div className="space-y-4">
                          <div>
                            <label className="mb-1 block text-sm font-medium text-gray-700">
                              Username
                            </label>

                            <input
                              type="text"
                              value={username}
                              onChange={(event) => setUsername(event.target.value)}
                              placeholder="Enter username"
                              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
                              disabled={creating}
                            />
                          </div>

                          <div>
                            <label className="mb-1 block text-sm font-medium text-gray-700">
                              Email
                            </label>

                            <input
                              type="email"
                              value={email}
                              onChange={(event) => setEmail(event.target.value)}
                              placeholder="Enter email"
                              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
                              disabled={creating}
                            />
                          </div>

                          <div>
                            <label className="mb-1 block text-sm font-medium text-gray-700">
                              Password
                            </label>

                            <input
                              type="password"
                              value={password}
                              onChange={(event) => setPassword(event.target.value)}
                              placeholder="Enter password"
                              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
                              disabled={creating}
                            />
                          </div>
                        </div>

                        <div className="mt-6 flex justify-end gap-3">
                          <button
                            type="button"
                            onClick={() => setShowCreateModal(false)}
                            disabled={creating}
                            className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50 disabled:opacity-50"
                          >
                            Cancel
                          </button>

                          <button
                            type="submit"
                            disabled={creating}
                            className="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
                          >
                            {creating ? "Creating..." : "Create User"}
                          </button>
                        </div>
                      </form>
                    </div>
                  </div>
                )}

                {showResetModal && resetUser && (
                  <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
                    <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">

                      <div className="mb-6 flex items-center justify-between">
                        <div>
                          <h2 className="text-lg font-semibold text-gray-900">
                            Reset Password
                          </h2>

                          <p className="mt-1 text-sm text-gray-500">
                            Set a new password for {resetUser.username}.
                          </p>
                        </div>

                        <button
                          type="button"
                          onClick={() => {
                            setShowResetModal(false);
                            setResetUser(null);
                            setNewPassword("");
                            setResetError(null);
                          }}
                          disabled={resetting}
                          className="text-2xl leading-none text-gray-400 transition hover:text-gray-600 disabled:opacity-50"
                        >
                          ×
                        </button>
                      </div>

                      {resetError && (
                        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
                          {resetError}
                        </div>
                      )}

                      <form
                        onSubmit={(event) => {
                          event.preventDefault();
                          handleResetPassword();
                        }}
                      >
                        <div>
                          <label className="mb-1 block text-sm font-medium text-gray-700">
                            New password
                          </label>

                          <input
                            type="password"
                            value={newPassword}
                            onChange={(event) =>
                              setNewPassword(event.target.value)
                            }
                            placeholder="Enter new password"
                            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
                            disabled={resetting}
                          />
                        </div>

                        <div className="mt-6 flex justify-end gap-3">
                          <button
                            type="button"
                            onClick={() => {
                              setShowResetModal(false);
                              setResetUser(null);
                              setNewPassword("");
                              setResetError(null);
                            }}
                            disabled={resetting}
                            className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50 disabled:opacity-50"
                          >
                            Cancel
                          </button>

                          <button
                            type="submit"
                            disabled={resetting || !newPassword.trim()}
                            className="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
                          >
                            {resetting ? "Resetting..." : "Reset Password"}
                          </button>
                        </div>
                      </form>
                    </div>
                  </div>
                )}
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}