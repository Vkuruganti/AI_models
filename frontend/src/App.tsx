import React, { useEffect, useState } from "react";

type Recommendation = {
  pod: string;
  type: string;
  suggestion: string;
  current_cpu?: number;
  cpu_limit?: number;
  current_qos?: string;
};

function App() {
  const [recs, setRecs] = useState<Recommendation[]>([]);

  useEffect(() => {
    fetch("/recommendations") // Replace with your API Gateway endpoint
      .then(res => res.json())
      .then(setRecs);
  }, []);

  return (
    <div style={{ padding: 32 }}>
      <h1>Kubernetes Advisor Recommendations</h1>
      <table>
        <thead>
          <tr>
            <th>Pod</th>
            <th>Type</th>
            <th>Suggestion</th>
            <th>CPU Usage</th>
            <th>CPU Limit</th>
            <th>QoS</th>
          </tr>
        </thead>
        <tbody>
          {recs.map((rec, i) => (
            <tr key={i}>
              <td>{rec.pod}</td>
              <td>{rec.type}</td>
              <td>{rec.suggestion}</td>
              <td>{rec.current_cpu ?? "-"}</td>
              <td>{rec.cpu_limit ?? "-"}</td>
              <td>{rec.current_qos ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App; 