import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { Badge } from "../components/ui";
import { shortId, fmtShort } from "../lib/theme";

const DAYS = [
  "MONDAY",
  "TUESDAY",
  "WEDNESDAY",
  "THURSDAY",
  "FRIDAY",
  "SATURDAY",
  "SUNDAY",
];

// ── Staff ────────────────────────────────────
export function Staff() {
  const { request } = useApi();
  return (
    <CrudPage
      title="Staff"
      endpoint="/staff/"
      request={request}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        { key: "department", label: "Department" },
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
          labelKey: (item) => `${item.full_name} (${item.role})`,
        },
        {
          name: "department",
          label: "Department",
          required: true,
          placeholder: "e.g. Radiology",
        },
      ]}
      defaultForm={{ user_id: "", department: "" }}
    />
  );
}

// ── Patients ─────────────────────────────────
export function Patients() {
  const { request } = useApi();
  return (
    <CrudPage
      title="Patients"
      endpoint="/patients/"
      request={request}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        { key: "gender", label: "Gender" },
        { key: "age", label: "Age" },
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
          labelKey: (item) =>
            `${item.full_name} (${item.phone_number || item.email})`,
        },
        {
          name: "gender",
          label: "Gender",
          options: ["MALE", "FEMALE", "OTHER"],
          required: true,
        },
        { name: "age", label: "Age", type: "number", required: true },
      ]}
      defaultForm={{ user_id: "", gender: "", age: "" }}
    />
  );
}

// ── Customers ────────────────────────────────
export function Customers() {
  const { request } = useApi();
  return (
    <CrudPage
      title="Customers"
      endpoint="/customers/"
      request={request}
      canEdit={true}
      canDelete={true}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        { key: "full_name", label: "Full Name" },
        { key: "phone_number", label: "Phone" },
        { key: "address", label: "Address" },
      ]}
      formFields={[
        { name: "full_name", label: "Full Name", required: true },
        {
          name: "phone_number",
          label: "Phone Number",
          required: true,
          placeholder: "e.g. 08012345678",
        },
        {
          name: "address",
          label: "Address",
          placeholder: "e.g. 5 Broad Street, Lagos",
        },
      ]}
      defaultForm={{ full_name: "", phone_number: "", address: "" }}
    />
  );
}

// ── Tests ─────────────────────────────────────
export function Tests() {
  const { request } = useApi();
  return (
    <CrudPage
      title="Diagnostic Tests"
      endpoint="/tests/"
      request={request}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        { key: "name", label: "Name" },
        {
          key: "description",
          label: "Description",
          render: (v) => v?.slice(0, 60) + (v?.length > 60 ? "…" : ""),
        },
        {
          key: "price",
          label: "Price",
          render: (v) => `₦${Number(v || 0).toLocaleString()}`,
        },
        {
          key: "branch_id",
          label: "Branch",
          render: (v) =>
            v ? (
              <code style={{ fontSize: 11 }}>{shortId(v)}</code>
            ) : (
              <span style={{ color: "#94a3b8" }}>All branches</span>
            ),
        },
      ]}
      formFields={[
        { name: "name", label: "Test Name", required: true },
        { name: "description", label: "Description", required: true, rows: 3 },
        { name: "price", label: "Price (₦)", type: "number", required: true },
        {
          name: "branch_id",
          label: "Branch (leave blank for all branches)",
          type: "select-search",
          endpoint: "/branches/",
          labelKey: (item) => `${item.name} (${item.branch_code})`,
          nullable: true,
          nullLabel: "— All branches —",
        },
      ]}
      defaultForm={{ name: "", description: "", price: "", branch_id: "" }}
    />
  );
}

// ── Branches ──────────────────────────────────
export function Branches() {
  const { request } = useApi();
  return (
    <CrudPage
      title="Branches"
      endpoint="/branches/"
      request={request}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        { key: "name", label: "Branch Name" },
        {
          key: "branch_code",
          label: "Code",
          render: (v) => (
            <span style={{ fontFamily: "monospace", fontWeight: 700 }}>
              {v}
            </span>
          ),
        },
        { key: "address", label: "Address" },
      ]}
      formFields={[
        { name: "name", label: "Branch Name", required: true },
        {
          name: "branch_code",
          label: "Branch Code",
          required: true,
          placeholder: "e.g. LG-01",
        },
        { name: "address", label: "Address", required: true },
        {
          name: "schedule_day",
          label: "Schedule Day",
          type: "select",
          options: DAYS,
          nullable: true,
          nullLabel: "— No schedule —",
        },
        {
          name: "schedule_opening_time",
          label: "Opening Time",
          type: "time",
          nullable: true,
          placeholder: "HH:MM",
        },
        {
          name: "schedule_closing_time",
          label: "Closing Time",
          type: "time",
          nullable: true,
          placeholder: "HH:MM",
        },
      ]}
      defaultForm={{
        name: "",
        branch_code: "",
        address: "",
        schedule_day: "",
        schedule_opening_time: "",
        schedule_closing_time: "",
      }}
    />
  );
}

// ── Payments ──────────────────────────────────
export function Payments() {
  const { request } = useApi();
  return (
    <CrudPage
      title="Payments"
      endpoint="/payments/"
      request={request}
      canCreate={false}
      canEdit={false}
      canDelete={false}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        {
          key: "amount",
          label: "Amount",
          render: (v, row) =>
            `${row.currency || "₦"} ${Number(v || 0).toLocaleString()}`,
        },
        { key: "payment_for", label: "For" },
        { key: "status", label: "Status", render: (v) => <Badge status={v} /> },
        { key: "reference", label: "Reference", render: (v) => v || "—" },
        { key: "created_at", label: "Date", render: (v) => fmtShort(v) },
      ]}
      formFields={[]}
      defaultForm={{}}
    />
  );
}

// ── Users ─────────────────────────────────────
export function Users() {
  const { request } = useApi();
  return (
    <CrudPage
      title="Users"
      endpoint="/users/"
      request={request}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        { key: "full_name", label: "Full Name" },
        { key: "email", label: "Email" },
        { key: "phone_number", label: "Phone" },
        { key: "role", label: "Role", render: (v) => <Badge status={v} /> },
        {
          key: "branch_id",
          label: "Branch",
          render: (v) =>
            v ? (
              <code style={{ fontSize: 11 }}>{shortId(v)}</code>
            ) : (
              <span style={{ color: "#94a3b8" }}>—</span>
            ),
        },
      ]}
      formFields={[
        { name: "full_name", label: "Full Name", required: true },
        { name: "email", label: "Email", type: "email", required: true },
        { name: "phone_number", label: "Phone Number", required: true },
        {
          name: "password",
          label: "Password",
          type: "password",
          required: true,
        },
        {
          name: "role",
          label: "Role",
          options: ["ADMIN", "STAFF", "DOCTOR", "COORDINATOR", "CLIENT"],
          required: true,
        },
        {
          name: "branch_id",
          label: "Branch (optional)",
          type: "select-search",
          endpoint: "/branches/",
          labelKey: (item) => `${item.name} (${item.branch_code})`,
          nullable: true,
          nullLabel: "— No branch —",
        },
      ]}
      defaultForm={{
        full_name: "",
        email: "",
        phone_number: "",
        password: "",
        role: "",
        branch_id: "",
      }}
    />
  );
}

// ── Doctors ───────────────────────────────────
export function Doctors() {
  const { request } = useApi();
  return (
    <CrudPage
      title="Doctors"
      endpoint="/doctors/"
      request={request}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        { key: "specialization", label: "Specialization" },
        { key: "license_number", label: "License No." },
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
          name: "specialization",
          label: "Specialization",
          required: true,
          placeholder: "e.g. Haematology",
        },
        { name: "license_number", label: "License Number", required: true },
      ]}
      defaultForm={{ user_id: "", specialization: "", license_number: "" }}
    />
  );
}
