import { useEffect } from "react";
import { C, statusColor } from "../lib/theme";

// ── Badge ────────────────────────────────────
export function Badge({ status }) {
  const color = statusColor[status] || C.muted;
  return (
    <span
      style={{
        display: "inline-block",
        padding: "2px 9px",
        borderRadius: 12,
        fontSize: 11,
        fontWeight: 600,
        background: color + "22",
        color,
      }}
    >
      {status}
    </span>
  );
}

// ── Toast ────────────────────────────────────
export function Toast({ msg, type = "success", onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 4000);
    return () => clearTimeout(t);
  }, [onClose]);
  if (!msg) return null;
  const bg = type === "error" ? C.danger : C.success;
  return (
    <div
      style={{
        position: "fixed",
        top: 20,
        right: 20,
        zIndex: 9999,
        background: bg,
        color: "#fff",
        padding: "12px 18px",
        borderRadius: 8,
        boxShadow: "0 4px 20px rgba(0,0,0,.2)",
        fontSize: 13,
        maxWidth: 340,
        display: "flex",
        alignItems: "center",
        gap: 10,
      }}
    >
      <span style={{ flex: 1 }}>{msg}</span>
      <button
        onClick={onClose}
        style={{
          background: "none",
          border: "none",
          color: "#fff",
          cursor: "pointer",
          fontSize: 18,
          lineHeight: 1,
        }}
      >
        ×
      </button>
    </div>
  );
}

// ── Modal ────────────────────────────────────
export function Modal({ open, title, onClose, children, width = 480 }) {
  useEffect(() => {
    const handler = (e) => {
      if (e.key === "Escape") onClose();
    };
    if (open) window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, onClose]);

  if (!open) return null;
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        style={{
          background: C.surface,
          borderRadius: 12,
          padding: 28,
          width: "100%",
          maxWidth: width,
          maxHeight: "90vh",
          overflowY: "auto",
          boxShadow: "0 24px 64px rgba(0,0,0,.25)",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 22,
          }}
        >
          <h2 style={{ fontSize: 17, fontWeight: 700, color: C.text }}>
            {title}
          </h2>
          <button
            onClick={onClose}
            style={{
              background: "none",
              border: "none",
              fontSize: 22,
              cursor: "pointer",
              color: C.muted,
              lineHeight: 1,
            }}
          >
            ×
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}

// ── Field ────────────────────────────────────
export function Field({
  label,
  name,
  value,
  onChange,
  type = "text",
  options,
  required,
  placeholder,
  rows,
}) {
  const inputStyle = {
    width: "100%",
    padding: "8px 12px",
    borderRadius: 6,
    border: `1px solid ${C.border}`,
    fontSize: 13,
    background: C.bg,
    color: C.text,
    outline: "none",
    transition: "border-color .15s",
  };
  return (
    <div style={{ marginBottom: 14 }}>
      <label
        style={{
          display: "block",
          fontSize: 12,
          fontWeight: 600,
          color: C.muted,
          marginBottom: 5,
        }}
      >
        {label}
        {required && <span style={{ color: C.danger }}> *</span>}
      </label>
      {options ? (
        <select
          name={name}
          value={value || ""}
          onChange={onChange}
          style={inputStyle}
        >
          <option value="">Select…</option>
          {options.map((o) => (
            <option key={o.value ?? o} value={o.value ?? o}>
              {o.label ?? o}
            </option>
          ))}
        </select>
      ) : rows ? (
        <textarea
          name={name}
          value={value || ""}
          onChange={onChange}
          required={required}
          rows={rows}
          placeholder={placeholder}
          style={{ ...inputStyle, resize: "vertical" }}
        />
      ) : (
        <input
          type={type}
          name={name}
          value={value || ""}
          onChange={onChange}
          required={required}
          placeholder={placeholder}
          style={inputStyle}
        />
      )}
    </div>
  );
}

// ── Button ───────────────────────────────────
export function Btn({
  children,
  onClick,
  variant = "primary",
  type = "button",
  disabled,
  size = "md",
  style: extra,
}) {
  const bg = {
    primary: C.accent,
    danger: C.danger,
    ghost: "transparent",
    secondary: C.border,
  }[variant];
  const color = ["primary", "danger"].includes(variant) ? "#fff" : C.text;
  const pad = size === "sm" ? "5px 10px" : "8px 16px";
  const fs = size === "sm" ? 12 : 13;
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      style={{
        padding: pad,
        borderRadius: 6,
        border: "none",
        cursor: disabled ? "not-allowed" : "pointer",
        fontSize: fs,
        fontWeight: 600,
        background: bg,
        color,
        opacity: disabled ? 0.6 : 1,
        transition: "opacity .15s",
        ...extra,
      }}
    >
      {children}
    </button>
  );
}

// ── Spinner / Empty ──────────────────────────
export function Spinner() {
  return (
    <div
      style={{
        padding: "40px 0",
        textAlign: "center",
        color: C.muted,
        fontSize: 14,
      }}
    >
      Loading…
    </div>
  );
}

export function EmptyState({ msg = "No records found", action }) {
  return (
    <div style={{ padding: "48px 0", textAlign: "center", color: C.muted }}>
      <div style={{ fontSize: 32, marginBottom: 10 }}>📭</div>
      <div style={{ fontSize: 14 }}>{msg}</div>
      {action && <div style={{ marginTop: 14 }}>{action}</div>}
    </div>
  );
}

// ── Table ────────────────────────────────────
export function Table({
  columns,
  rows,
  onEdit,
  onDelete,
  canEdit = true,
  canDelete = true,
  emptyAction,
  emptyMsg,
}) {
  if (!rows || rows.length === 0)
    return <EmptyState msg={emptyMsg} action={emptyAction} />;
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
              style={{ transition: "background .1s" }}
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

// ── Card ─────────────────────────────────────
export function Card({ children, style: extra }) {
  return (
    <div
      style={{
        background: C.surface,
        borderRadius: 10,
        border: `1px solid ${C.border}`,
        padding: 22,
        marginBottom: 20,
        ...extra,
      }}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, action }) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 18,
      }}
    >
      <h3 style={{ fontSize: 15, fontWeight: 700, color: C.text }}>{title}</h3>
      {action && <div>{action}</div>}
    </div>
  );
}

// ── Tabs ─────────────────────────────────────
export function Tabs({ tabs, active, onChange }) {
  return (
    <div
      style={{
        display: "flex",
        borderBottom: `1px solid ${C.border}`,
        marginBottom: 20,
      }}
    >
      {tabs.map((t) => (
        <button
          key={t.id}
          onClick={() => onChange(t.id)}
          style={{
            padding: "12px 18px",
            border: "none",
            background: "none",
            cursor: "pointer",
            fontSize: 13,
            fontWeight: active === t.id ? 700 : 400,
            color: active === t.id ? C.accent : C.muted,
            borderBottom:
              active === t.id
                ? `2px solid ${C.accent}`
                : "2px solid transparent",
            marginBottom: -1,
            transition: "color .15s",
          }}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}

// ── StatCard ─────────────────────────────────
export function StatCard({ label, value, color, icon }) {
  return (
    <div
      style={{
        background: C.surface,
        border: `1px solid ${C.border}`,
        borderRadius: 10,
        padding: "18px 20px",
        borderLeft: `4px solid ${color}`,
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
        }}
      >
        <div>
          <div style={{ fontSize: 28, fontWeight: 800, color, lineHeight: 1 }}>
            {value}
          </div>
          <div
            style={{
              fontSize: 12,
              color: C.muted,
              marginTop: 5,
              fontWeight: 500,
            }}
          >
            {label}
          </div>
        </div>
        {icon && <div style={{ fontSize: 24 }}>{icon}</div>}
      </div>
    </div>
  );
}
