import { useEffect, useState } from "react";
import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { useAuth } from "../hooks/useAuth";
import { Badge } from "../components/ui";
import { shortId, fmtShort } from "../lib/theme";

// id -> name map for showing related records (e.g. branch names) in tables
function useNames(request, endpoint, labelKey = "name") {
  const [names, setNames] = useState({});
  useEffect(() => {
    request("GET", endpoint)
      .then((data) =>
        setNames(Object.fromEntries((data || []).map((d) => [d.id, d[labelKey]]))),
      )
      .catch(() => {});
  }, [request, endpoint, labelKey]);
  return names;
}

const idColumn = {
  key: "id",
  label: "ID",
  render: (v) => (
    <code style={{ fontSize: 11 }} title={v}>
      {shortId(v)}
    </code>
  ),
};

const userColumn = {
  key: "user_id",
  label: "User",
  render: (v, row) =>
    row.user_full_name ? row.user_full_name : <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
};

// ── Staff ────────────────────────────────────
export function Staff() {
  const { request } = useApi();
  const { user } = useAuth();
  const isAdmin = user?.role === "ADMIN";
  return (
    <CrudPage
      title="Staff"
      endpoint="/staff/"
      request={request}
      canCreate={isAdmin}
      canEdit={isAdmin}
      canDelete={isAdmin}
      searchKeys={["user_full_name", "department"]}
      columns={[idColumn, userColumn, { key: "department", label: "Department" }]}
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
  const { user } = useAuth();
  const canManage = user?.role === "ADMIN" || user?.role === "STAFF";
  return (
    <CrudPage
      title="Patients"
      endpoint="/patients/"
      request={request}
      canCreate={canManage}
      canEdit={canManage}
      canDelete={canManage}
      searchKeys={["user_full_name", "gender"]}
      columns={[
        idColumn,
        userColumn,
        { key: "gender", label: "Gender" },
        { key: "age", label: "Age" },
      ]}
      formFields={[
        {
          name: "user_id",
          label: "User",
          required: true,
          type: "select-search",
          endpoint: "/users/",
          labelKey: (item) => `${item.full_name} (${item.phone_number || item.email})`,
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
  const { user } = useAuth();
  const canManage = user?.role === "ADMIN" || user?.role === "STAFF";
  return (
    <CrudPage
      title="Customers"
      endpoint="/customers/"
      request={request}
      canCreate={canManage}
      canEdit={canManage}
      canDelete={user?.role === "ADMIN"}
      searchKeys={["full_name", "phone_number", "address"]}
      columns={[
        idColumn,
        { key: "full_name", label: "Full Name" },
        { key: "phone_number", label: "Phone", render: (v) => v || "—" },
        { key: "address", label: "Address", render: (v) => v || "—" },
      ]}
      formFields={[
        { name: "full_name", label: "Full Name", required: true },
        {
          name: "phone_number",
          label: "WhatsApp Number",
          required: true,
          placeholder: "e.g. 08012345678",
        },
        {
          name: "address",
          label: "Address",
          nullable: true,
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
  const { user } = useAuth();
  const branches = useNames(request, "/branches/");
  const isAdmin = user?.role === "ADMIN";
  return (
    <CrudPage
      title="Diagnostic Tests"
      endpoint="/tests/"
      request={request}
      canCreate={isAdmin}
      canEdit={isAdmin || user?.role === "STAFF"}
      canDelete={isAdmin}
      searchKeys={["name", "description"]}
      columns={[
        { key: "name", label: "Name" },
        {
          key: "description",
          label: "Description",
          render: (v) => (v ? v.slice(0, 60) + (v.length > 60 ? "…" : "") : "—"),
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
              branches[v] || <code style={{ fontSize: 11 }}>{shortId(v)}</code>
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
  const { user } = useAuth();
  const canManage = user?.role === "ADMIN" || user?.role === "STAFF";
  return (
    <CrudPage
      title="Branches"
      endpoint="/branches/"
      request={request}
      canCreate={canManage}
      canEdit={canManage}
      canDelete={canManage}
      searchKeys={["name", "branch_code", "address"]}
      columns={[
        { key: "name", label: "Branch Name" },
        {
          key: "branch_code",
          label: "Code",
          render: (v) => (
            <span style={{ fontFamily: "monospace", fontWeight: 700 }}>{v}</span>
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
      ]}
      defaultForm={{
        name: "",
        branch_code: "",
        address: "",
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
      canEdit={true}
      canDelete={false}
      searchKeys={["payer_name", "reference", "status", "payment_for"]}
      columns={[
        { key: "payer_name", label: "Payer", render: (v) => v || "—" },
        {
          key: "amount",
          label: "Amount",
          render: (v, row) =>
            `${row.currency === "NGN" ? "₦" : `${row.currency} `}${Number(v || 0).toLocaleString()}`,
        },
        { key: "payment_for", label: "For" },
        { key: "status", label: "Status", render: (v) => <Badge status={v} /> },
        { key: "reference", label: "Reference", render: (v) => v || "—" },
        { key: "created_at", label: "Date", render: (v) => fmtShort(v) },
      ]}
      formFields={[
        {
          name: "status",
          label: "Status (set COMPLETED for cash payments; the payer gets a receipt)",
          required: true,
          options: ["PENDING", "COMPLETED", "FAILED"],
        },
      ]}
      defaultForm={{ status: "" }}
    />
  );
}

// ── Users ─────────────────────────────────────
export function Users() {
  const { request } = useApi();
  const { user } = useAuth();
  const branches = useNames(request, "/branches/");
  const isAdmin = user?.role === "ADMIN";
  return (
    <CrudPage
      title="Users"
      endpoint="/users/"
      request={request}
      canCreate={isAdmin}
      canEdit={isAdmin}
      canDelete={isAdmin}
      searchKeys={["full_name", "email", "phone_number", "role"]}
      columns={[
        { key: "full_name", label: "Full Name" },
        { key: "email", label: "Email" },
        { key: "phone_number", label: "Phone" },
        { key: "role", label: "Role", render: (v) => <Badge status={v} /> },
        {
          key: "branch_id",
          label: "Branch",
          render: (v) =>
            v ? (
              branches[v] || <code style={{ fontSize: 11 }}>{shortId(v)}</code>
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
          editLabel: "New Password (leave blank to keep the current one)",
          type: "password",
          required: true,
          omitIfEmpty: true,
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
  const { user } = useAuth();
  const isAdmin = user?.role === "ADMIN";
  return (
    <CrudPage
      title="Doctors"
      endpoint="/doctors/"
      request={request}
      canCreate={isAdmin}
      canEdit={isAdmin}
      canDelete={isAdmin}
      searchKeys={["user_full_name", "specialization", "license_number"]}
      columns={[
        idColumn,
        userColumn,
        { key: "specialization", label: "Specialization" },
        { key: "license_number", label: "License No." },
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
