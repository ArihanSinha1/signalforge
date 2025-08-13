import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import 'tailwindcss/tailwind.css';

// Import and register required Chart.js modules
import {
  Chart as ChartJS,
  CategoryScale,  // This is for the X-axis categories
  LinearScale,    // This is for the Y-axis numbers
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function PricesPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    async function fetchPrices() {
      const res = await fetch("http://localhost:8000/api/prices?symbol=MSFT&limit=180");
      const json = await res.json();
      setData(json);
    }
    fetchPrices();
  }, []);

  if (!data) return <div className="p-8">Loading...</div>;

  const labels = data.prices.map(p => new Date(p.ts).toLocaleDateString());
  const close = data.prices.map(p => p.close);

  const chartData = {
    labels,
    datasets: [
      {
        label: `${data.symbol} Close`,
        data: close,
        borderColor: 'rgb(75, 192, 192)',
        fill: false,
      },
    ],
  };

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">SignalForge</h1>
        <p className="text-gray-600">Your go-to platform for financial data visualization.</p>
      </div>
      <h1 className="text-2xl font-semibold mb-4">Price chart — {data.symbol}</h1>
      <div className="bg-white rounded shadow p-4">
        <h2 className="text-xl mb-2">Last 180 days</h2>
        <p className="text-gray-600 mb-4">Data fetched from the backend API.</p>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Symbol:
          </label>
          <input
            type="text"
            value={data.symbol}
            readOnly
            className="block w-full p-2 border border-gray-300 rounded"
          />
        </div>
        <Line data={chartData} />
      </div>
    </div>
  );
}
