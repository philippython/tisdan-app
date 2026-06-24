import { useState } from "react";
import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { Badge, Card, CardHeader, Btn, Toast, Table } from "../components/ui";
import { useToast } from "../hooks/useToast";
import { fmtDate, shortId, truncate } from "../lib/theme";

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
    {
      key: "id",
      label: "ID",
      render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
    },
    {
      key: "booking_id",
      label: "Booking",
      render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
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
        formFields={[
          {
            name: "booking_id",
            label: "Booking",
            required: true,
            type: "select-search",
            endpoint: "/bookings/",
            labelKey: (item) =>
              `Booking ${shortId(item.id)} — ${item.status} — ${item.booking_date ? new Date(item.booking_date).toLocaleDateString() : ""}`,
          },
          {
            name: "result_text",
            label: "Result Text",
            required: true,
            rows: 5,
            placeholder: "Enter the diagnostic result…",
          },
        ]}
        defaultForm={{ booking_id: "", result_text: "" }}
      />
    </>
  );
}
