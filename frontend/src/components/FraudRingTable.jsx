function FraudRingTable({ rings }) {
  if (!rings || rings.length === 0) {
    return <div style={{ padding: "16px", color: "#999" }}>No fraud rings detected</div>;
  }

  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{
        width: "100%",
        borderCollapse: "collapse",
        fontSize: "12px",
        fontFamily: "monospace"
      }}>
        <thead>
          <tr style={{ backgroundColor: "#f5f5f5", borderBottom: "2px solid #ddd" }}>
            <th style={{ padding: "8px", textAlign: "left", fontWeight: "600" }}>Ring ID</th>
            <th style={{ padding: "8px", textAlign: "left", fontWeight: "600" }}>Pattern</th>
            <th style={{ padding: "8px", textAlign: "center", fontWeight: "600" }}>Members</th>
            <th style={{ padding: "8px", textAlign: "center", fontWeight: "600" }}>Risk Score</th>
            <th style={{ padding: "8px", textAlign: "left", fontWeight: "600" }}>Accounts</th>
          </tr>
        </thead>
        <tbody>
          {rings.map((ring, idx) => (
            <tr 
              key={ring.ring_id}
              style={{
                backgroundColor: idx % 2 === 0 ? "#fafafa" : "#ffffff",
                borderBottom: "1px solid #e0e0e0",
              }}
            >
              <td style={{ padding: "8px", fontWeight: "500", color: "#d32f2f" }}>
                {ring.ring_id}
              </td>
              <td style={{ padding: "8px" }}>
                <span style={{
                  backgroundColor: ring.pattern_type === "cycle" ? "#ffcdd2" :
                                  ring.pattern_type === "smurfing_fan_in" ? "#c8e6c9" :
                                  ring.pattern_type === "smurfing_fan_out" ? "#c8e6c9" :
                                  "#b3e5fc",
                  padding: "2px 6px",
                  borderRadius: "3px",
                  fontSize: "11px",
                  fontWeight: "600"
                }}>
                  {ring.pattern_type}
                </span>
              </td>
              <td style={{ padding: "8px", textAlign: "center", fontWeight: "500" }}>
                {ring.member_accounts.length}
              </td>
              <td style={{ padding: "8px", textAlign: "center", fontWeight: "600", color: "#d32f2f" }}>
                {ring.risk_score.toFixed(1)}
              </td>
              <td style={{ padding: "8px", fontSize: "11px", maxWidth: "200px", wordBreak: "break-word" }}>
                <details style={{ cursor: "pointer" }}>
                  <summary style={{ fontWeight: "500", userSelect: "none" }}>
                    {ring.member_accounts.length} accounts
                  </summary>
                  <div style={{ marginTop: "4px", padding: "4px 0", borderTop: "1px solid #e0e0e0" }}>
                    {ring.member_accounts.map((acc, i) => (
                      <div key={i} style={{ padding: "2px 0", color: "#666" }}>
                        • {acc}
                      </div>
                    ))}
                  </div>
                </details>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FraudRingTable;
