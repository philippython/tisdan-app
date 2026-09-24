import { useState } from "react";
import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { Badge, Card, CardHeader, Btn, Toast, Table } from "../components/ui";
import { useToast } from "../hooks/useToast";
import { fmtDate, fmtShort, shortId, truncate } from "../lib/theme";

const RESULT_STATUS = [
  { value: "RELEASED", label: "Released — send to patient on WhatsApp now" },
  { value: "PENDING", label: "Pending — keep internal for review" },
];

export default function Results() {
  const { request } = useApi();
  const [searchName, setSearchName] = useState("");
  const [searchRows, setSearchRows] = useState(null);
  const [searching, setSearching] = useState(false);
  const { toast, show, hide } = useToast();

  const doSearch = async () => {
    if (!searchName.trim()) {
      setSearchRows(null);
      return;
    }
    setSearching(true);
    try {
      const data = await request(
        "GET",
        `/results/by-customer-name/?name=${encodeURIComponent(searchName.trim())}`,
      );
      setSearchRows(data);
    } catch (e) {
      show(e.message, "error");
    }
    setSearching(false);
  };

  const resultColumns = [
    { key: "patient_name", label: "Patient", render: (v) => v || "—" },
    { key: "test_name", label: "Test", render: (v) => v || "—" },
    {
      key: "booking_id",
      label: "Booking",
      render: (v, row) => (
        <span title={v}>
          <code style={{ fontSize: 11 }}>{shortId(v)}</code>
          {row.booking_date && (
            <span style={{ fontSize: 11, color: "#64748b" }}> · {fmtShort(row.booking_date)}</span>
          )}
        </span>
      ),
    },
    { key: "status", label: "Status", render: (v) => <Badge status={v} /> },
    { key: "uploaded_at", label: "Uploaded", render: (v) => fmtDate(v) },
    {
      key: "result_text",
      label: "Result",
      render: (v) => <span title={v}>{truncate(v, 70)}</span>,
    },
  ];

  return (
    <>
      {toast && <Toast msg={toast.msg} type={toast.type} onClose={hide} />}

      <Card style={{ marginBottom: 20 }}>
        <CardHeader title="Search Results by Patient Name" />
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <input
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && doSearch()}
            placeholder="Type patient name and press Enter…"
            style={{
              flex: 1,
              minWidth: 240,
              padding: "8px 12px",
              borderRadius: 6,
              border: "1px solid #e2e8f0",
              fontSize: 13,
              outline: "none",
            }}
          />
          <Btn onClick={doSearch} disabled={searching}>
            {searching ? "Searching…" : "Search"}
          </Btn>
          {searchRows && (
            <Btn
              variant="secondary"
              onClick={() => {
                setSearchRows(null);
                setSearchName("");
              }}
            >
              Clear
            </Btn>
          )}
        </div>
        {searchRows !== null && (
          <div style={{ marginTop: 16 }}>
            <Table
              columns={resultColumns}
              rows={searchRows}
              canEdit={false}
              canDelete={false}
              emptyMsg={`No results found for "${searchName}".`}
            />
          </div>
        )}
      </Card>

      <CrudPage
        title="Results"
        endpoint="/results/"
        request={request}
        columns={resultColumns}
        searchKeys={["patient_name", "test_name", "status", "booking_id"]}
        formFields={[
          {
            name: "booking_id",
            label: "Booking",
            required: true,
            type: "select-search",
            endpoint: "/bookings/",
            labelKey: (item) =>
              `${item.patient_name || "Unknown patient"} — ${item.test_name || "test"} — ${
                item.booking_date ? new Date(item.booking_date).toLocaleDateString() : ""
              } (${shortId(item.id)})`,
          },
          {
            name: "result_text",
            label: "Result Text",
            required: true,
            rows: 5,
            placeholder: "Enter the diagnostic result…",
          },
          {
            name: "status",
            label: "Status",
            required: true,
            options: RESULT_STATUS,
          },
        ]}
        defaultForm={{ booking_id: "", result_text: "", status: "RELEASED" }}
      />
    </>
  );
}
