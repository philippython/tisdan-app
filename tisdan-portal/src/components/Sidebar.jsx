import { NavLink } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { C } from "../lib/theme";

const NAV = {
  ADMIN: [
    {
      section: "Overview",
      items: [{ to: "/", label: "Dashboard", icon: "⊞" }],
    },
    {
      section: "Operations",
      items: [
        { to: "/bookings", label: "Bookings", icon: "📋" },
        { to: "/results", label: "Results", icon: "🧪" },
        { to: "/patients", label: "Patients", icon: "🧑‍⚕️" },
        { to: "/customers", label: "Customers", icon: "👤" },
      ],
    },
    {
      section: "Financials",
      items: [{ to: "/payments", label: "Payments", icon: "💳" }],
    },
    {
      section: "Catalogue",
      items: [
        { to: "/tests", label: "Diagnostic Tests", icon: "🔬" },
        { to: "/branches", label: "Branches", icon: "🏥" },
      ],
    },
    {
      section: "Team",
      items: [
        { to: "/users", label: "Users", icon: "🔑" },
        { to: "/staff", label: "Staff", icon: "👥" },
        { to: "/doctors", label: "Doctors", icon: "👨‍⚕️" },
        { to: "/coordinators", label: "Coordinators", icon: "🔗" },
      ],
    },
    {
      section: "Communications",
      items: [{ to: "/broadcast", label: "Broadcast", icon: "📢" }],
    },
  ],
  STAFF: [
    {
      section: "Overview",
      items: [{ to: "/", label: "Dashboard", icon: "⊞" }],
    },
    {
      section: "Operations",
      items: [
        { to: "/bookings", label: "Bookings", icon: "📋" },
        { to: "/results", label: "Results", icon: "🧪" },
        { to: "/patients", label: "Patients", icon: "🧑‍⚕️" },
        { to: "/customers", label: "Customers", icon: "👤" },
      ],
    },
    {
      section: "Catalogue",
      items: [{ to: "/tests", label: "Diagnostic Tests", icon: "🔬" }],
    },
    {
      section: "Communications",
      items: [{ to: "/broadcast", label: "Broadcast", icon: "📢" }],
    },
  ],
  DOCTOR: [
    {
      section: "Overview",
      items: [{ to: "/", label: "Dashboard", icon: "⊞" }],
    },
    {
      section: "Operations",
      items: [
        { to: "/bookings", label: "Bookings", icon: "📋" },
        { to: "/results", label: "Results", icon: "🧪" },
        { to: "/patients", label: "Patients", icon: "🧑‍⚕️" },
      ],
    },
  ],
  COORDINATOR: [
    {
      section: "My Account",
      items: [{ to: "/coordinators", label: "My Referrals", icon: "🔗" }],
    },
  ],
};

export default function Sidebar() {
  const { user, logout } = useAuth();
  const nav = NAV[user?.role] || NAV.STAFF;

  return (
    <aside
      style={{
        width: 224,
        background: C.sidebar,
        display: "flex",
        flexDirection: "column",
        flexShrink: 0,
        overflowY: "auto",
      }}
    >
      {/* Logo */}
      <div
        style={{
          padding: "24px 20px 18px",
          borderBottom: "1px solid rgba(255,255,255,.08)",
        }}
      >
        <div
          style={{
            color: "#fff",
            fontWeight: 800,
            fontSize: 20,
            letterSpacing: "-0.5px",
          }}
        >
          Tisdan
        </div>
        <div
          style={{
            color: "rgba(255,255,255,.35)",
            fontSize: 11,
            marginTop: 2,
            fontWeight: 500,
          }}
        >
          Diagnostic Centre
        </div>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: "8px 0" }}>
        {nav.map((section) => (
          <div key={section.section}>
            <div
              style={{
                padding: "14px 18px 5px",
                color: "rgba(255,255,255,.28)",
                fontSize: 10,
                fontWeight: 700,
                letterSpacing: "0.1em",
                textTransform: "uppercase",
              }}
            >
              {section.section}
            </div>
            {section.items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                style={({ isActive }) => ({
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  padding: "8px 12px",
                  margin: "1px 8px",
                  borderRadius: 6,
                  textDecoration: "none",
                  fontSize: 13,
                  color: isActive ? "#fff" : "rgba(255,255,255,.6)",
                  background: isActive ? C.sidebarActive : "transparent",
                  fontWeight: isActive ? 600 : 400,
                  transition: "all .12s",
                })}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      {/* User footer */}
      <div
        style={{
          padding: "14px 16px",
          borderTop: "1px solid rgba(255,255,255,.08)",
        }}
      >
        <div
          style={{
            color: "rgba(255,255,255,.9)",
            fontSize: 13,
            fontWeight: 600,
            marginBottom: 2,
          }}
        >
          {user?.full_name}
        </div>
        <div
          style={{
            color: "rgba(255,255,255,.35)",
            fontSize: 11,
            marginBottom: 10,
          }}
        >
          {user?.role}
        </div>
        <button
          onClick={logout}
          style={{
            width: "100%",
            background: "rgba(255,255,255,.07)",
            border: "none",
            color: "rgba(255,255,255,.55)",
            padding: "6px 10px",
            borderRadius: 5,
            cursor: "pointer",
            fontSize: 12,
            fontWeight: 500,
            textAlign: "left",
          }}
        >
          Sign out →
        </button>
      </div>
    </aside>
  );
}
