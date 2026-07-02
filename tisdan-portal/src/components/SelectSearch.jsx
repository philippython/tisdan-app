import { useState, useEffect, useRef } from "react";
import { C } from "../lib/theme";

/**
 * SelectSearch — searchable dropdown that resolves to an ID.
 *
 * Props:
 *   label        string
 *   name         string       — form field name (sets hidden value)
 *   value        string       — current ID value
 *   onChange     fn(name, id) — called when selection changes
 *   required     bool
 *   placeholder  string
 *   endpoint     string       — API path to fetch options e.g. '/branches/'
 *   request      fn           — API request function
 *   labelKey     string|fn    — key or fn(item) => display label
 *   nullable     bool         — allow clearing / "none" option
 *   nullLabel    string       — label for null option e.g. "All branches"
 */
export default function SelectSearch({
  label,
  name,
  value,
  onChange,
  required,
  placeholder = "Search…",
  endpoint,
  request,
  labelKey = "name",
  nullable = false,
  nullLabel = "— None —",
}) {
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [open, setOpen] = useState(false);
  const [displayVal, setDisplayVal] = useState("");
  const containerRef = useRef(null);
  const inputRef = useRef(null);

  const getLabel = (item) =>
    typeof labelKey === "function"
      ? labelKey(item)
      : (item[labelKey] ?? item.id);

  // Load options once
  useEffect(() => {
    request("GET", endpoint)
      .then((data) => setOptions(Array.isArray(data) ? data : []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [endpoint]);

  // Sync display value when value prop changes (e.g. opening edit modal)
  useEffect(() => {
    if (!value) {
      setDisplayVal("");
      return;
    }
    const found = options.find((o) => o.id === value);
    if (found) setDisplayVal(getLabel(found));
  }, [value, options]);

  // Close on outside click
  useEffect(() => {
    const handler = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false);
        setSearch("");
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const filtered = options.filter((o) =>
    getLabel(o).toLowerCase().includes(search.toLowerCase()),
  );

  const select = (item) => {
    const id = item ? item.id : null;
    const lbl = item ? getLabel(item) : nullLabel;
    onChange(name, id);
    setDisplayVal(item ? lbl : "");
    setSearch("");
    setOpen(false);
  };

  const handleInputClick = () => {
    setOpen(true);
    setSearch("");
    setTimeout(() => inputRef.current?.focus(), 0);
  };

  const inputStyle = {
    width: "100%",
    padding: "8px 12px",
    borderRadius: 6,
    border: `1px solid ${open ? C.accent : C.border}`,
    fontSize: 13,
    background: C.bg,
    color: C.text,
    outline: "none",
    cursor: "pointer",
    boxSizing: "border-box",
    transition: "border-color .15s",
  };

  return (
    <div style={{ marginBottom: 14, position: "relative" }} ref={containerRef}>
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

      {/* Trigger */}
      <div style={{ position: "relative" }}>
        <input
          readOnly
          value={open ? search : displayVal || ""}
          onChange={() => {}}
          onClick={handleInputClick}
          placeholder={loading ? "Loading…" : displayVal || placeholder}
          style={inputStyle}
        />
        <span
          style={{
            position: "absolute",
            right: 10,
            top: "50%",
            transform: "translateY(-50%)",
            color: C.muted,
            pointerEvents: "none",
            fontSize: 12,
          }}
        >
          {open ? "▲" : "▼"}
        </span>
      </div>

      {/* Dropdown */}
      {open && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            right: 0,
            zIndex: 500,
            background: C.surface,
            border: `1px solid ${C.border}`,
            borderRadius: 6,
            boxShadow: "0 8px 24px rgba(0,0,0,.12)",
            marginTop: 2,
            maxHeight: 260,
            display: "flex",
            flexDirection: "column",
          }}
        >
          {/* Search input */}
          <div
            style={{
              padding: "8px 10px",
              borderBottom: `1px solid ${C.border}`,
            }}
          >
            <input
              ref={inputRef}
              autoFocus
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Type to search…"
              style={{
                width: "100%",
                padding: "6px 10px",
                borderRadius: 5,
                border: `1px solid ${C.border}`,
                fontSize: 13,
                background: C.bg,
                color: C.text,
                outline: "none",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Options list */}
          <div style={{ overflowY: "auto", flex: 1 }}>
            {nullable && (
              <div
                onClick={() => select(null)}
                style={{
                  padding: "9px 14px",
                  fontSize: 13,
                  cursor: "pointer",
                  color: C.muted,
                  fontStyle: "italic",
                  borderBottom: `1px solid ${C.border}`,
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = C.bg)}
                onMouseLeave={(e) =>
                  (e.currentTarget.style.background = "transparent")
                }
              >
                {nullLabel}
              </div>
            )}

            {loading ? (
              <div
                style={{ padding: "12px 14px", color: C.muted, fontSize: 13 }}
              >
                Loading…
              </div>
            ) : filtered.length === 0 ? (
              <div
                style={{ padding: "12px 14px", color: C.muted, fontSize: 13 }}
              >
                No results found
              </div>
            ) : (
              filtered.map((item) => (
                <div
                  key={item.id}
                  onClick={() => select(item)}
                  style={{
                    padding: "9px 14px",
                    fontSize: 13,
                    cursor: "pointer",
                    background:
                      item.id === value ? C.accentLight : "transparent",
                    color: item.id === value ? C.accent : C.text,
                    fontWeight: item.id === value ? 600 : 400,
                  }}
                  onMouseEnter={(e) => {
                    if (item.id !== value)
                      e.currentTarget.style.background = C.bg;
                  }}
                  onMouseLeave={(e) => {
                    if (item.id !== value)
                      e.currentTarget.style.background = "transparent";
                  }}
                >
                  {getLabel(item)}
                  {item.branch_code && (
                    <span
                      style={{
                        marginLeft: 8,
                        fontSize: 11,
                        color: C.muted,
                        fontFamily: "monospace",
                      }}
                    >
                      {item.branch_code}
                    </span>
                  )}
                  {item.referral_code && (
                    <span
                      style={{
                        marginLeft: 8,
                        fontSize: 11,
                        color: C.muted,
                        fontFamily: "monospace",
                      }}
                    >
                      {item.referral_code}
                    </span>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
