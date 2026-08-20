import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { clearTokens } from "../../auth/authStorage";


function Sidebar() {
    const navigate = useNavigate();

    function handleLogout() {
        const confirmed = window.confirm(
            "Are you sure you want to logout?"
        );

        if (!confirmed) {
            return;
        }
        clearTokens();
        navigate("/login");
    }

    const navItems = [
        { name: "Dashboard", path: "/dashboard" },
        { name: "Products", path: "/products" },
        { name: "Inventory", path: "/inventory" },
        { name: "Categories", path: "/categories" },
        { name: "Reports", path: "/reports" }
    ];

    return (
        <aside className="flex w-64 min-h-screen flex-col bg-slate-900 p-4 text-white">
            <div className="mb-8">
                <h1 className="text-2xl font-bold">StockFlow</h1>
                <p className="text-sm text-slate-400">Inventory Management</p>
            </div>

            <nav className="flex-1 space-y-2">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `block rounded-lg px-4 py-3 transition ${isActive
                                ? "bg-blue-600 text-white"
                                : "text-slate-300 hover:bg-slate-800"
                            }`
                        }
                    >
                        {item.name}
                    </NavLink>
                ))}
            </nav>
            <button onClick={handleLogout}
                className="mt-4 rounded-lg px-4 py-3 text-left text-slate-300 transition hover:bg-slate-800 hover:text-white">
                Logout
            </button>
        </aside>
    );
}

export default Sidebar;