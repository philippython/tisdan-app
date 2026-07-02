import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useApi } from "../hooks/useApi";
import { useAuth } from "../hooks/useAuth";
import { StatCard, Card, CardHeader, Spinner, Badge } from "../components/ui";
import { C, fmtShort } from "../lib/theme";

function EmptyCard({ icon, msg, to, cta }) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "36px 20px",
        gap: 10,
      }}
    >
      <div style={{ fontSize: 36 }}>{icon}</div>
      <p
        style={{ color: C.muted, fontSize: 13, textAlign: "center", margin: 0 }}
      >
        {msg}
      </p>
      <Link
        to={to}
        style={{
          marginTop: 4,
          padding: "7px 16px",
          borderRadius: 6,
          background: C.accent,
          color: "#fff",
          fontSize: 13,
          fontWeight: 600,
          textDecoration: "none",
        }}
      >
        {cta}
      </Link>
    </div>
  );
}

export default function Dashboard() {
  const { request } = useApi();
  const [stats, setStats] = useState(null);
  const [recentBookings, setRecentBookings] = useState([]);
  const [pendingResults, setPendingResults] = useState([]);
  const [loading, setLoading] = useState(true);

  const { user } = useAuth();

  useEffect(() => {
    (async () => {
      try {
        const requests = [
          request("GET", "/bookings/"),
          request("GET", "/results/"),
          request("GET", "/customers/"),
        ];
        if (user?.role === "ADMIN" || user?.role === "COORDINATOR") {
          requests.push(request("GET", "/coordinators/"));
        } else {
          requests.push(Promise.resolve([]));
        }

        const [bookings, results, customers, coordinators] =
          await Promise.allSettled(requests);

        const safeBookings =
          bookings.status === "fulfilled" ? bookings.value : [];
        const safeResults = results.status === "fulfilled" ? results.value : [];
        const safeCustomers =
          customers.status === "fulfilled" ? customers.value : [];
        const safeCoordinators =
          coordinators.status === "fulfilled" ? coordinators.value : [];

        setStats({
          bookings: safeBookings.length,
          results: safeResults.length,
          customers: safeCustomers.length,
          coordinators: safeCoordinators.length,
          pending: safeBookings.filter((b) => b.status === "PENDING").length,
          pendingResults: safeResults.filter((r) => r.status === "PENDING")
            .length,
        });
        setRecentBookings([...safeBookings].reverse().slice(0, 8));
        setPendingResults(
          safeResults.filter((r) => r.status === "PENDING").slice(0, 6),
        );
      } catch (ex) {
        setStats({
          bookings: 0,
          results: 0,
          customers: 0,
          coordinators: 0,
          pending: 0,
          pendingResults: 0,
        });
      }
      setLoading(false);
    })();
  }, [request, user]);

  if (loading) return <Spinner />;

  const isBlank =
    stats.bookings === 0 && stats.results === 0 && stats.customers === 0;

  return (
    <>
      {/* Stats row */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(170px, 1fr))",
          gap: 14,
          marginBottom: 24,
        }}
      >
        <StatCard
          label="Total Bookings"
          value={stats.bookings}
          color={C.accent}
          icon="📋"
        />
        <StatCard
          label="Pending Bookings"
          value={stats.pending}
          color={C.warn}
          icon="⏳"
        />
        <StatCard
          label="Results Uploaded"
          value={stats.results}
          color={C.success}
          icon="🧪"
        />
        <StatCard
          label="Pending Results"
          value={stats.pendingResults}
          color={C.danger}
          icon="🔴"
        />
        <StatCard
          label="Customers"
          value={stats.customers}
          color={C.purple}
          icon="👤"
        />
        <StatCard
          label="Coordinators"
          value={stats.coordinators}
          color="#0891b2"
          icon="🔗"
        />
      </div>

      {/* Getting-started banner shown when DB is empty */}
      {isBlank && (
        <Card
          style={{
            marginBottom: 20,
            background: C.accentLight,
            border: `1px solid #bfdbfe`,
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 16,
              flexWrap: "wrap",
            }}
          >
            <div style={{ fontSize: 32 }}>🚀</div>
            <div style={{ flex: 1 }}>
              <div
                style={{
                  fontWeight: 700,
                  fontSize: 15,
                  color: C.accent,
                  marginBottom: 4,
                }}
              >
                Welcome to Tisdan — let's get set up
              </div>
              <p style={{ fontSize: 13, color: "#1d4ed8", margin: 0 }}>
                Start by adding a branch and diagnostic tests, then create your
                first staff account.
              </p>
            </div>
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <Link
                to="/branches"
                style={{
                  padding: "7px 14px",
                  background: C.accent,
                  color: "#fff",
                  borderRadius: 6,
                  fontSize: 13,
                  fontWeight: 600,
                  textDecoration: "none",
                }}
              >
                Add a Branch
              </Link>
              <Link
                to="/tests"
                style={{
                  padding: "7px 14px",
                  background: "#1d4ed8",
                  color: "#fff",
                  borderRadius: 6,
                  fontSize: 13,
                  fontWeight: 600,
                  textDecoration: "none",
                }}
              >
                Add Tests
              </Link>
              <Link
                to="/users"
                style={{
                  padding: "7px 14px",
                  background: "#fff",
                  color: C.accent,
                  border: `1px solid ${C.accent}`,
                  borderRadius: 6,
                  fontSize: 13,
                  fontWeight: 600,
                  textDecoration: "none",
                }}
              >
                Create Users
              </Link>
            </div>
          </div>
        </Card>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        {/* Recent Bookings */}
        <Card>
          <CardHeader
            title="Recent Bookings"
            action={
              <Link
                to="/bookings"
                style={{
                  fontSize: 12,
                  color: C.accent,
                  textDecoration: "none",
                  fontWeight: 600,
                }}
              >
                View all →
              </Link>
            }
          />
          {recentBookings.length === 0 ? (
            <EmptyCard
              icon="📋"
              msg="No bookings have been made yet."
              to="/bookings"
              cta="Create a Booking"
            />
          ) : (
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                fontSize: 13,
              }}
            >
              <thead>
                <tr>
                  {["ID", "Date", "Status"].map((h) => (
                    <th
                      key={h}
                      style={{
                        textAlign: "left",
                        padding: "8px 10px",
                        borderBottom: `1px solid ${C.border}`,
                        color: C.muted,
                        fontSize: 11,
                        fontWeight: 600,
                        textTransform: "uppercase",
                      }}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {recentBookings.map((b) => (
                  <tr
                    key={b.id}
                    onMouseEnter={(e) =>
                      (e.currentTarget.style.background = C.bg)
                    }
                    onMouseLeave={(e) =>
                      (e.currentTarget.style.background = "transparent")
                    }
                  >
                    <td
                      style={{
                        padding: "8px 10px",
                        borderBottom: `1px solid ${C.border}`,
                      }}
                    >
                      <code style={{ fontSize: 11, color: C.muted }}>
                        {b.id.slice(0, 8)}…
                      </code>
                    </td>
                    <td
                      style={{
                        padding: "8px 10px",
                        borderBottom: `1px solid ${C.border}`,
                      }}
                    >
                      {fmtShort(b.booking_date)}
                    </td>
                    <td
                      style={{
                        padding: "8px 10px",
                        borderBottom: `1px solid ${C.border}`,
                      }}
                    >
                      <Badge status={b.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Card>

        {/* Pending Results */}
        <Card>
          <CardHeader
            title="Pending Results"
            action={
              <Link
                to="/results"
                style={{
                  fontSize: 12,
                  color: C.accent,
                  textDecoration: "none",
                  fontWeight: 600,
                }}
              >
                View all →
              </Link>
            }
          />
          {pendingResults.length === 0 ? (
            stats.results === 0 ? (
              <EmptyCard
                icon="🧪"
                msg="No results uploaded yet. Upload a patient's result to get started."
                to="/results"
                cta="Upload a Result"
              />
            ) : (
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  padding: "36px 20px",
                  gap: 8,
                }}
              >
                <div style={{ fontSize: 32 }}>✅</div>
                <p
                  style={{
                    color: C.success,
                    fontSize: 13,
                    fontWeight: 600,
                    margin: 0,
                  }}
                >
                  All results have been released
                </p>
              </div>
            )
          ) : (
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                fontSize: 13,
              }}
            >
              <thead>
                <tr>
                  {["Booking ID", "Uploaded", "Status"].map((h) => (
                    <th
                      key={h}
                      style={{
                        textAlign: "left",
                        padding: "8px 10px",
                        borderBottom: `1px solid ${C.border}`,
                        color: C.muted,
                        fontSize: 11,
                        fontWeight: 600,
                        textTransform: "uppercase",
                      }}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {pendingResults.map((r) => (
                  <tr
                    key={r.id}
                    onMouseEnter={(e) =>
                      (e.currentTarget.style.background = C.bg)
                    }
                    onMouseLeave={(e) =>
                      (e.currentTarget.style.background = "transparent")
                    }
                  >
                    <td
                      style={{
                        padding: "8px 10px",
                        borderBottom: `1px solid ${C.border}`,
                      }}
                    >
                      <code style={{ fontSize: 11, color: C.muted }}>
                        {r.booking_id?.slice(0, 8)}…
                      </code>
                    </td>
                    <td
                      style={{
                        padding: "8px 10px",
                        borderBottom: `1px solid ${C.border}`,
                      }}
                    >
                      {fmtShort(r.uploaded_at)}
                    </td>
                    <td
                      style={{
                        padding: "8px 10px",
                        borderBottom: `1px solid ${C.border}`,
                      }}
                    >
                      <Badge status={r.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Card>

        {/* Quick links — always visible */}
        <Card style={{ gridColumn: "1 / -1" }}>
          <CardHeader title="Quick Actions" />
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
            {[
              {
                to: "/bookings",
                label: "+ New Booking",
                icon: "📋",
                color: C.accent,
              },
              {
                to: "/results",
                label: "+ Upload Result",
                icon: "🧪",
                color: C.success,
              },
              {
                to: "/broadcast",
                label: "📢 Send Broadcast",
                icon: "",
                color: "#7c3aed",
              },
              {
                to: "/tests",
                label: "+ Add Test",
                icon: "🔬",
                color: "#0891b2",
              },
              { to: "/users", label: "+ Add User", icon: "🔑", color: C.warn },
              {
                to: "/coordinators",
                label: "+ Add Coordinator",
                icon: "🔗",
                color: "#db2777",
              },
            ].map((q) => (
              <Link
                key={q.to}
                to={q.to}
                style={{
                  padding: "10px 18px",
                  borderRadius: 8,
                  border: `1px solid ${C.border}`,
                  background: C.surface,
                  color: C.text,
                  textDecoration: "none",
                  fontSize: 13,
                  fontWeight: 600,
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  transition: "border-color .15s, box-shadow .15s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = q.color;
                  e.currentTarget.style.boxShadow = `0 0 0 3px ${q.color}22`;
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = C.border;
                  e.currentTarget.style.boxShadow = "none";
                }}
              >
                {q.icon && <span>{q.icon}</span>}
                {q.label}
              </Link>
            ))}
          </div>
        </Card>
      </div>
    </>
  );
}
