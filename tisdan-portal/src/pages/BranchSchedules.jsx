import CrudPage from "../components/CrudPage";
import { useApi } from "../hooks/useApi";
import { shortId } from "../lib/theme";

const DAYS = [
  "MONDAY",
  "TUESDAY",
  "WEDNESDAY",
  "THURSDAY",
  "FRIDAY",
  "SATURDAY",
  "SUNDAY",
];

export default function BranchSchedules() {
  const { request } = useApi();

  return (
    <CrudPage
      title="Branch Schedules"
      endpoint="/branch-schedules/"
      request={request}
      columns={[
        {
          key: "id",
          label: "ID",
          render: (v) => <code style={{ fontSize: 11 }}>{shortId(v)}</code>,
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
        { key: "day", label: "Day" },
        { key: "opening_time", label: "Opening", render: (v) => v || "—" },
        { key: "closing_time", label: "Closing", render: (v) => v || "—" },
      ]}
      formFields={[
        {
          name: "branch_id",
          label: "Branch",
          required: true,
          type: "select-search",
          endpoint: "/branches/",
          labelKey: (item) => `${item.name} (${item.branch_code})`,
        },
        {
          name: "day",
          label: "Day",
          required: true,
          type: "select",
          options: DAYS,
        },
        {
          name: "opening_time",
          label: "Opening Time",
          type: "time",
          required: true,
        },
        {
          name: "closing_time",
          label: "Closing Time",
          type: "time",
          required: true,
        },
      ]}
      defaultForm={{
        branch_id: "",
        day: "",
        opening_time: "",
        closing_time: "",
      }}
    />
  );
}
