import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";

function Layout() {
  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />
      <div className="flex flex-1 flex-col">
        <Header />

        <main className="flex-1 p-8">
            <Outlet />
        </main>
      </div>
    </div>
  );
}

export default Layout;