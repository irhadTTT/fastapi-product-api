import { exportInventoryCsv, exportInventoryExcel } from "../api/reports";


export default function Reports() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">
          Reports
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          Export inventory reports and analyze your stock data.
        </p>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="font-semibold text-gray-900">
          Inventory Report
        </h2>

        <p className="mt-1 text-sm text-gray-500">
          Download the current inventory report in your preferred format.
        </p>

        <div className="mt-5 flex gap-3">
          <button
            type="button"
            onClick={exportInventoryCsv}
            className="rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700"
          >
            Export CSV
          </button>

          <button
            type="button"
            onClick={exportInventoryExcel}
            className="rounded-lg bg-green-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-green-700"
          >
            Export Excel
          </button>
        </div>
      </div>
    </div>
  );
}