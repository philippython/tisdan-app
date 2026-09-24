import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { useAuth } from "../hooks/useAuth";
import { Badge } from "../components/ui";
import { fmtDate } from "../lib/theme";

const REFERRAL_STATUS = ["registered", "visited", "completed", "paid", "cancelled"];

export const referralColumns = [
  { key: "created_at", label: "Date", render: (v) => fmtDate(v) },
  { key: "patient_name", label: "Patient" },
  { key: "patient_phone", label: "Phone" },
  { key: "test_name", label: "Test", render: (v) => v || "—" },
  { key: "branch_name", label: "Branch", render: (v) => v || "—" },
  { key: "status", label: "Status", render: (v) => <Badge status={v?.toUpperCase()} /> },
  { key: "commission", label: "Commission", render: (v) => v || "—" },
];

export default function Referrals() {
  const { request } = useApi();
  const { user } = useAuth();
  const isAdmin = user?.role === "ADMIN";

  return (
    <CrudPage
      title="Referrals"
      endpoint="/referrals/"
      request={request}
      canCreate={false}
      canEdit={isAdmin}
      canDelete={isAdmin}
      searchKeys={["patient_name", "patient_phone", "coordinator_name", "coordinator_code", "status"]}
      columns={
        isAdmin
          ? [
              ...referralColumns.slice(0, 1),
              {
                key: "coordinator_name",
                label: "Coordinator",
                render: (v, row) => (
                  <div>
                    <div>{v || "—"}</div>
                    <div style={{ fontSize: 11, color: "#64748b", fontFamily: "monospace" }}>
                      {row.coordinator_code}
                    </div>
                  </div>
                ),
              },
              ...referralColumns.slice(1),
            ]
          : referralColumns
      }
      formFields={[
        { name: "status", label: "Status", required: true, options: REFERRAL_STATUS },
        { name: "commission", label: "Commission", nullable: true, placeholder: "e.g. ₦300" },
        { name: "test_name", label: "Test", nullable: true },
        { name: "branch_name", label: "Branch", nullable: true },
      ]}
      defaultForm={{ status: "", commission: "", test_name: "", branch_name: "" }}
    />
  );
}
