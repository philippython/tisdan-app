import { useState, useEffect } from "react";
import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { useToast } from "../hooks/useToast";
import { Badge } from "../components/ui";
import { fmtDate, shortId } from "../lib/theme";

const BOOKING_STATUS = ["PENDING", "CONFIRMED", "CANCELLED", "COMPLETED"];

export default function Bookings() {
  const { request } = useApi();
  const { show } = useToast();
  const [tests, setTests] = useState([]);

  useEffect(() => {
    request("GET", "/tests/")
      .then((data) => setTests(Array.isArray(data) ? data : []))
      .catch(() => {});
  }, [request]);

  const handleBookingCreated = async (booking) => {
    const test = tests.find((item) => item.id === booking.test_id);
    if (!test || !booking.user_id) return;

    const confirmPay = window.confirm(
      `Booking created for ${test.name} at ₦${Number(test.price).toLocaleString()}.\n\nWould you like to send a payment link now?`,
    );
    if (!confirmPay) return;

    try {
      const result = await request("POST", "/payments/initialize/", {
        booking_id: booking.id,
        payer_id: booking.user_id,
        amount: test.price,
        currency: "NGN",
      });
      show("Payment link created and sent via WhatsApp.");
      if (result?.authorization_url) {
        window.open(result.authorization_url, "_blank");
      }
    } catch (ex) {
      show(`Unable to create payment link: ${ex.message}`, "error");
    }
  };

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
          render: (v, row) =>
            row.user_full_name ? (
              row.user_full_name
            ) : (
              <code style={{ fontSize: 11 }}>{shortId(v)}</code>
            ),
        },
        {
          key: "test_id",
          label: "Test",
          render: (v, row) =>
            row.test_name ? (
              row.test_name
            ) : (
              <code style={{ fontSize: 11 }}>{shortId(v)}</code>
            ),
        },
        {
          key: "branch_id",
          label: "Branch",
          render: (v, row) =>
            row.branch_name ? (
              row.branch_name
            ) : (
              <code style={{ fontSize: 11 }}>{shortId(v)}</code>
            ),
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
