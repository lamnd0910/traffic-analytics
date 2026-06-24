import { useState, useEffect } from "react";
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, ResponsiveContainer,
} from "recharts";

function App() {
  const [count, setCount] = useState(0);
  const [history, setHistory] = useState([]);       // dữ liệu sống (WebSocket)
  const [perMinute, setPerMinute] = useState([]);   // lịch sử (database)

  // --- dữ liệu sống qua WebSocket ---
  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/stats");
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setCount(data.count);
      setHistory((prev) => {
        const time = new Date().toLocaleTimeString();
        return [...prev, { time, count: data.count }].slice(-30);
      });
    };
    return () => ws.close();
  }, []);

  // --- lịch sử qua HTTP, gọi lại mỗi 5 giây ---
  useEffect(() => {
    const fetchHistory = () => {
      fetch("http://127.0.0.1:8000/stats/history")
        .then((res) => res.json())
        .then((data) => setPerMinute(data))
        .catch((err) => console.error("Lỗi tải lịch sử:", err));
    };

    fetchHistory();                              // gọi ngay lần đầu
    const id = setInterval(fetchHistory, 5000);  // rồi lặp mỗi 5s
    return () => clearInterval(id);              // dọn dẹp khi gỡ
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1>Traffic Analytics 🚦</h1>
      <p style={{ fontSize: 28, fontWeight: "bold" }}>Count: {count}</p>

      <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
        <img src="http://127.0.0.1:8000/video_feed" width="600" alt="live feed" />

        <div style={{ width: 500, height: 320 }}>
          <h3>Số đếm trực tiếp</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={history}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Line type="monotone" dataKey="count" stroke="#2563eb" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ width: 500, height: 320 }}>
          <h3>Lưu lượng theo phút (lịch sử)</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={perMinute}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="minute" />
              <YAxis />
              <Bar dataKey="count" fill="#16a34a" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default App;