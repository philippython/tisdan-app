import { useState, useEffect } from "react";
import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { useAuth } from "../hooks/useAuth";
import { useToast } from "../hooks/useToast";
import { Badge, Toast } from "../components/ui";
import { fmtDate, shortId } from "../lib/theme";

const BOOKING_STATUS = ["PENDING", "CONFIRMED", "CANCELLED", "COMPLETED"];

export default function Bookings() {
  const { request } = useApi();
  const { user } = useAuth();
  const { toast, show, hide } = useToast();
  const [tests, setTests] = useState([]);
  const canManage = user?.role === "ADMIN" || user?.role === "STAFF";

  useEffect(() => {
    request("GET", "/tests/")
      .then((data) => setTests(Array.isArray(data) ? data : []))
      .catch(() => {});
  }, [request]);

  const handleBookingCreated = async (booking) => {
    const test = tests.find((item) => item.id === booking.test_id);
    // payment links are tied to a registered user (Paystack needs an email)
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
      show(
        result?.whatsapp_sent
          ? "Payment link created and sent via WhatsApp."
          : "Payment created, but the WhatsApp message could not be sent.",
        result?.whatsapp_sent ? "success" : "error",
      );
      if (result?.authorization_url) {
        window.open(result.authorization_url, "_blank");
      }
    } catch (ex) {
      show(`Unable to create payment link: ${ex.message}`, "error");
    }
  };

  return (
    <>
      {toast && <Toast msg={toast.msg} type={toast.type} onClose={hide} />}
      <CrudPage
        title="Bookings"
        endpoint="/bookings/"
        request={request}
        canCreate={canManage}
        canEdit={canManage}
        canDelete={canManage}
        onCreated={handleBookingCreated}
        searchKeys={["patient_name", "patient_phone", "test_name", "branch_name", "status", "id"]}
        columns={[
          {
            key: "id",
            label: "Reference",
            render: (v) => (
              <code style={{ fontSize: 11 }} title={v}>
                {shortId(v)}
              </code>
            ),
          },
          { key: "booking_date", label: "Date", render: (v) => fmtDate(v) },
          { key: "status", label: "Status", render: (v) => <Badge status={v} /> },
          {
            key: "patient_name",
            label: "Patient",
            render: (v, row) => (
              <div>
                <div>{v || "—"}</div>
                {row.patient_phone && (
                  <div style={{ fontSize: 11, color: "#64748b" }}>
                    {row.patient_phone}
                    {row.customer_id && !row.user_id ? " · WhatsApp" : ""}
                  </div>
                )}
              </div>
            ),
          },
          {
            key: "test_name",
            label: "Test",
            render: (v, row) => v || <code style={{ fontSize: 11 }}>{shortId(row.test_id)}</code>,
          },
          {
            key: "branch_name",
            label: "Branch",
            render: (v, row) => v || <code style={{ fontSize: 11 }}>{shortId(row.branch_id)}</code>,
          },
        ]}
        formFields={[
          {
            name: "customer_id",
            label: "Customer (WhatsApp / walk-in)",
            type: "select-search",
            endpoint: "/customers/",
            labelKey: (item) => `${item.full_name} (${item.phone_number || "no phone"})`,
            nullable: true,
            nullLabel: "— None —",
          },
          {
            name: "user_id",
            label: "…or registered user",
            type: "select-search",
            endpoint: "/users/",
            labelKey: (item) => `${item.full_name} (${item.phone_number || item.email})`,
            nullable: true,
            nullLabel: "— None —",
          },
          {
            name: "test_id",
            label: "Diagnostic Test",
            required: true,
            type: "select-search",
            endpoint: "/tests/",
            labelKey: (item) => `${item.name} — ₦${Number(item.price || 0).toLocaleString()}`,
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
          customer_id: "",
          user_id: "",
          test_id: "",
          branch_id: "",
          booking_date: "",
          status: "",
        }}
      />
    </>
  );
}
