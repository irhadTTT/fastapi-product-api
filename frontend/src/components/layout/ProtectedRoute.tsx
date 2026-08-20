import { Navigate, Outlet } from "react-router-dom";
import { getAccessToken } from "../../auth/authStorage";

function ProtectedRoute() {
  const token = getAccessToken();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}

export default ProtectedRoute;