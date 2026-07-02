import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./hooks/useAuth";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Bookings from "./pages/Bookings";
import Results from "./pages/Results";
import Coordinators from "./pages/Coordinators";
import Broadcast from "./pages/Broadcast";
import BranchSchedules from "./pages/BranchSchedules";
import {
  Staff,
  Patients,
  Customers,
  Tests,
  Branches,
  Payments,
  Users,
  Doctors,
} from "./pages/OtherPages";

function ProtectedRoutes() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#0f1c2e",
          color: "#fff",
          fontSize: 15,
        }}
      >
        Loading…
      </div>
    );
  }

  if (!user) return <Navigate to="/login" replace />;

  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="bookings" element={<Bookings />} />
        <Route path="results" element={<Results />} />
        <Route path="coordinators" element={<Coordinators />} />
        <Route path="broadcast" element={<Broadcast />} />
        <Route path="staff" element={<Staff />} />
        <Route path="patients" element={<Patients />} />
        <Route path="customers" element={<Customers />} />
        <Route path="tests" element={<Tests />} />
        <Route path="branches" element={<Branches />} />
        <Route path="branch-schedules" element={<BranchSchedules />} />
        <Route path="payments" element={<Payments />} />
        <Route path="users" element={<Users />} />
        <Route path="doctors" element={<Doctors />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginGate />} />
        <Route path="/*" element={<ProtectedRoutes />} />
      </Routes>
    </AuthProvider>
  );
}

function LoginGate() {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (user) return <Navigate to="/" replace />;
  return <Login />;
}
