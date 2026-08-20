import { Navigate, Outlet } from "react-router-dom";
import { getAccessToken } from "../../auth/authStorage";

function PublicRoute() {
  const token = getAccessToken();

  if (token) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
}

export default PublicRoute;