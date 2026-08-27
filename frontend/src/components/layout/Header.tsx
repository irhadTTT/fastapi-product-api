import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { getMe } from "../../api/auth";


function Header() {
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [role, setRole] = useState("");

  useEffect(() => {
  getMe()
    .then((user) => {
      setUsername(user.username);
      setRole(user.role);
    })
    .catch((error) => {
      console.error("Failed to get current user:", error);
    });
}, []);

  const pageTitles: Record<string, string> = {
    "/dashboard": "Dashboard",
    "/products": "Products",
    "/inventory": "Inventory",
    "/categories": "Categories",
    "/reports": "Reports",
    "/users": "Users"
  };

  const pageTitle = pageTitles[location.pathname] ?? "StockFlow";
  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
      <div>
        <h2 className="text-lg font-semibold text-slate-900">
           {pageTitle}
        </h2>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white">
          {username.charAt(0).toUpperCase()}
        </div>

        <div className="hidden sm:block">
          <p className="text-sm font-medium text-slate-900">
            {username}
          </p>
          <p className="text-xs text-slate-500">
            {role}
          </p>
        </div>
      </div>
    </header>
  );
}

export default Header;