import { useLocation } from "react-router-dom";


function Header() {
  const location = useLocation();

  const pageTitles: Record<string, string> = {
    "/dashboard": "Dashboard",
    "/products": "Products",
    "/inventory": "Inventory",
    "/categories": "Categories",
    "/reports": "Reports",
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
          IK
        </div>

        <div className="hidden sm:block">
          <p className="text-sm font-medium text-slate-900">
            Irhad
          </p>
          <p className="text-xs text-slate-500">
            Administrator
          </p>
        </div>
      </div>
    </header>
  );
}

export default Header;