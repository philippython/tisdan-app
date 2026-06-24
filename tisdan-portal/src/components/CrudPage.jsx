import { useState, useEffect, useCallback } from "react";
import {
  Card,
  CardHeader,
  Modal,
  Field,
  Btn,
  Spinner,
  Toast,
  EmptyState,
} from "./ui";
import { useToast } from "../hooks/useToast";
import { C } from "../lib/theme";
import SelectSearch from "./SelectSearch";

function DataTable({ columns, rows, onEdit, onDelete, canEdit, canDelete }) {
  return (
    <div style={{ overflowX: "auto" }}>
      <table
        style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}
      >
        <thead>
          <tr>
            {columns.map((c) => (
              <th
                key={c.key}
                style={{
                  textAlign: "left",
                  padding: "10px 12px",
                  borderBottom: `2px solid ${C.border}`,
                  color: C.muted,
                  fontWeight: 600,
                  fontSize: 11,
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                  whiteSpace: "nowrap",
                }}
              >
                {c.label}
              </th>
            ))}
            {(canEdit || canDelete) && (
              <th
                style={{
                  textAlign: "left",
                  padding: "10px 12px",
                  borderBottom: `2px solid ${C.border}`,
                  color: C.muted,
                  fontWeight: 600,
                  fontSize: 11,
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                }}
              >
                Actions
              </th>
            )}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr
              key={row.id}
              onMouseEnter={(e) => (e.currentTarget.style.background = C.bg)}
              onMouseLeave={(e) =>
                (e.currentTarget.style.background = "transparent")
              }
            >
              {columns.map((c) => (
                <td
                  key={c.key}
                  style={{
                    padding: "10px 12px",
                    borderBottom: `1px solid ${C.border}`,
                    verticalAlign: "middle",
                  }}
                >
                  {c.render
                    ? c.render(row[c.key], row)
                    : String(row[c.key] ?? "—")}
                </td>
              ))}
              {(canEdit || canDelete) && (
                <td
                  style={{
                    padding: "10px 12px",
                    borderBottom: `1px solid ${C.border}`,
                    whiteSpace: "nowrap",
                  }}
                >
                  <div style={{ display: "flex", gap: 8 }}>
                    {canEdit && (
                      <Btn
                        size="sm"
                        variant="secondary"
                        onClick={() => onEdit(row)}
                      >
                        Edit
                      </Btn>
                    )}
                    {canDelete && (
                      <Btn
                        size="sm"
                        variant="danger"
                        onClick={() => onDelete(row.id)}
                      >
                        Delete
                      </Btn>
                    )}
                  </div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function CrudPage({
  title,
  endpoint,
  columns,
  formFields,
  defaultForm,
  request,
  canCreate = true,
  canEdit = true,
  canDelete = true,
  extraActions,
  beforeTable,
}) {
  const [rows, setRows] = useState([]);
  const [status, setStatus] = useState("loading"); // 'loading' | 'ok' | 'error'
  const [errorMsg, setErrorMsg] = useState("");
  const [modal, setModal] = useState(null);
  const [form, setForm] = useState(defaultForm);
  const [saving, setSaving] = useState(false);
  const { toast, show, hide } = useToast();

  const load = useCallback(async () => {
    setStatus("loading");
    try {
      const data = await request("GET", endpoint);
      setRows(Array.isArray(data) ? data : []);
      setStatus("ok");
    } catch (e) {
      setErrorMsg(e.message);
      setStatus("error");
    }
  }, [request, endpoint]);

  useEffect(() => {
    load();
  }, [load]);

  const openCreate = () => {
    setForm(defaultForm);
    setModal({ mode: "create" });
  };

  const openEdit = (row) => {
    setForm({ ...defaultForm, ...row });
    setModal({ mode: "edit", data: row });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (modal.mode === "create") {
        await request("POST", endpoint, form);
        show("Created successfully");
      } else {
        await request("PUT", `${endpoint}${modal.data.id}/`, form);
        show("Updated successfully");
      }
      setModal(null);
      load();
    } catch (ex) {
      show(ex.message, "error");
    }
    setSaving(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this record? This cannot be undone.")) return;
    try {
      await request("DELETE", `${endpoint}${id}/`);
      show("Deleted");
      load();
    } catch (ex) {
      show(ex.message, "error");
    }
  };

  const singularTitle = title.replace(/s$/, "");

  const renderBody = () => {
    if (status === "loading") return <Spinner />;

    if (status === "error")
      return (
        <div
          style={{
            padding: "40px 20px",
            textAlign: "center",
            background: "#fef2f2",
            borderRadius: 8,
            border: "1px solid #fecaca",
          }}
        >
          <div style={{ fontSize: 28, marginBottom: 8 }}>⚠️</div>
          <div style={{ color: "#991b1b", fontWeight: 600, marginBottom: 4 }}>
            Failed to load {title.toLowerCase()}
          </div>
          <div style={{ color: "#b91c1c", fontSize: 13, marginBottom: 16 }}>
            {errorMsg}
          </div>
          <Btn variant="secondary" onClick={load}>
            Try again
          </Btn>
        </div>
      );

    if (rows.length === 0)
      return (
        <EmptyState
          msg={`No ${title.toLowerCase()} yet.`}
          action={
            canCreate ? (
              <Btn onClick={openCreate}>
                + Add your first {singularTitle.toLowerCase()}
              </Btn>
            ) : null
          }
        />
      );

    return (
      <DataTable
        columns={columns}
        rows={rows}
        onEdit={openEdit}
        onDelete={handleDelete}
        canEdit={canEdit}
        canDelete={canDelete}
      />
    );
  };

  return (
    <>
      {toast && <Toast msg={toast.msg} type={toast.type} onClose={hide} />}

      <Card>
        <CardHeader
          title={title}
          action={
            <div style={{ display: "flex", gap: 10 }}>
              {extraActions}
              {canCreate && (
                <Btn onClick={openCreate}>+ New {singularTitle}</Btn>
              )}
            </div>
          }
        />
        {beforeTable}
        {renderBody()}
      </Card>

      <Modal
        open={!!modal}
        title={
          modal?.mode === "create"
            ? `New ${singularTitle}`
            : `Edit ${singularTitle}`
        }
        onClose={() => setModal(null)}
      >
        <form onSubmit={handleSave}>
          {formFields.map((f) =>
            f.type === "select-search" ? (
              <SelectSearch
                key={f.name}
                label={f.label}
                name={f.name}
                value={form[f.name]}
                onChange={(name, id) =>
                  setForm((prev) => ({ ...prev, [name]: id }))
                }
                required={f.required}
                placeholder={f.placeholder}
                endpoint={f.endpoint}
                request={request}
                labelKey={f.labelKey}
                nullable={f.nullable}
                nullLabel={f.nullLabel}
              />
            ) : (
              <Field
                key={f.name}
                label={f.label}
                name={f.name}
                value={form[f.name]}
                onChange={handleChange}
                type={f.type}
                options={f.options}
                required={f.required}
                placeholder={f.placeholder}
                rows={f.rows}
              />
            ),
          )}
          <div style={{ display: "flex", gap: 10, marginTop: 22 }}>
            <Btn type="submit" disabled={saving}>
              {saving ? "Saving…" : "Save"}
            </Btn>
            <Btn variant="ghost" onClick={() => setModal(null)}>
              Cancel
            </Btn>
          </div>
        </form>
      </Modal>
    </>
  );
}
