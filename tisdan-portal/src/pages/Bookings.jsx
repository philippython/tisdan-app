import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { Badge } from "../components/ui";
import { fmtDate, shortId } from "../lib/theme";

const BOOKING_STATUS = ["PENDING", "CONFIRMED", "CANCELLED", "COMPLETED"];

export default function Bookings() {
  const { request } = useApi();

  return (
    <CrudPage
      title="Bookings"
      endpoint="/bookings/"
      request={request}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        { key: "booking_date", label: "Date", render: (v) => fmtDate(v) },
        { key: "status", label: "Status", render: (v) => <Badge status={v} /> },
        {
          key: "user_id",
          label: "User",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        {
          key: "test_id",
          label: "Test",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
        {
          key: "branch_id",
          label: "Branch",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
        },
      ]}
      formFields={[
        {
          name: "user_id",
          label: "Customer",
          required: true,
          type: "select-search",
          endpoint: "/users/",
          labelKey: (item) =>
            `${item.full_name} (${item.phone_number || item.email})`,
        },
        {
          name: "test_id",
          label: "Diagnostic Test",
          required: true,
          type: "select-search",
          endpoint: "/tests/",
          labelKey: (item) =>
            `${item.name} — ₦${Number(item.price || 0).toLocaleString()}`,
        },
        {
          name: "branch_id",
          label: "Branch",
          required: true,
          type: "select-search",
          endpoint: "/branches/",
          labelKey: (item) => `${item.name} (${item.branch_code})`,
        },
        {
          name: "booking_date",
          label: "Booking Date & Time",
          type: "datetime-local",
          required: true,
        },
        { name: "status", label: "Status", options: BOOKING_STATUS },
      ]}
      defaultForm={{
        user_id: "",
        test_id: "",
        branch_id: "",
        booking_date: "",
        status: "",
      }}
    />
  );
}
