import React from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

function AnalyticsChart({ emails }) {
  const sentimentData = [
    { name: "Positive", value: emails.filter(e => e.sentiment === "Positive").length },
    { name: "Neutral", value: emails.filter(e => e.sentiment === "Neutral").length },
    { name: "Negative", value: emails.filter(e => e.sentiment === "Negative").length },
  ];

  const COLORS = ["#4CAF50", "#FFC107", "#F44336"];

  return (
    <div style={{ marginTop: "30px", textAlign: "center" }}>
      <h3>Sentiment Analytics</h3>

      {/* Print counts */}
      <div style={{ marginBottom: "15px" }}>
        {sentimentData.map((item, index) => (
          <p key={index} style={{ margin: "4px 0" }}>
            <strong style={{ color: COLORS[index] }}>{item.name}:</strong> {item.value}
          </p>
        ))}
      </div>

      <PieChart width={400} height={300}>
        <Pie
          data={sentimentData}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={80}
        >
          {sentimentData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
}

export default AnalyticsChart;
