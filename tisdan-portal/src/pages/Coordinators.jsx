import { useState, useEffect } from "react";
import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { useAuth } from "../hooks/useAuth";
import { Card, CardHeader, Spinner } from "../components/ui";
import { C, shortId } from "../lib/theme";

function CoordinatorSelfView({ request }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    request("GET", "/coordinators/")
      .then(setData)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [request]);

  if (loading) return <Spinner />;

  return (
    <Card>
      <CardHeader title="My Referral Information" />
      {data.length === 0 ? (
        <p style={{ color: C.muted, fontSize: 14 }}>
          No referral data found for your account.
        </p>
      ) : (
        data.map((c) => (
          <div
            key={c.id}
            style={{
              background: C.bg,
              borderRadius: 8,
              padding: "20px 24px",
              border: `1px solid ${C.border}`,
              marginBottom: 14,
            }}
          >
            <div
              style={{
                fontSize: 11,
                color: C.muted,
                fontWeight: 600,
                textTransform: "uppercase",
                letterSpacing: "0.06em",
                marginBottom: 6,
              }}
            >
              Your Referral Code
            </div>
            <div
              style={{
                fontSize: 32,
                fontWeight: 800,
                color: C.accent,
                letterSpacing: "0.05em",
                fontFamily: "monospace",
              }}
            >
              {c.referral_code}
            </div>
            <div style={{ marginTop: 14, fontSize: 13, color: C.muted }}>
              Coordinator ID:{" "}
              <code style={{ fontSize: 11 }}>{shortId(c.id)}</code>
            </div>
          </div>
        ))
      )}
    </Card>
  );
}

export default function Coordinators() {
  const { request } = useApi();
  const { user } = useAuth();

  if (user?.role === "COORDINATOR")
    return <CoordinatorSelfView request={request} />;

  return (
    <CrudPage
      title="Coordinators"
      endpoint="/coordinators/"
      request={request}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        {
          key: "referral_code",
          label: "Referral Code",
          render: (v) => (
            <span
              style={{
                fontFamily: "monospace",
                fontWeight: 700,
                color: C.accent,
                fontSize: 14,
              }}
            >
              {v}
            </span>
          ),
        },
        {
          key: "user_id",
          label: "User",
          render: (v, row) =>
            row.user_full_name ? (
              row.user_full_name
            ) : (
              <code style={{ fontSize: 11 }}>{shortId(v)}</code>
            ),
        },
      ]}
      formFields={[
        {
          name: "user_id",
          label: "User",
          required: true,
          type: "select-search",
          endpoint: "/users/",
          labelKey: (item) => `${item.full_name} (${item.email})`,
        },
        {
          name: "referral_code",
          label: "Referral Code",
          required: true,
          placeholder: "e.g. REF-JOHN-001",
        },
      ]}
      defaultForm={{ user_id: "", referral_code: "" }}
    />
  );
}
