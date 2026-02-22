import { useEffect, useRef } from "react";
import CytoscapeComponent from "react-cytoscapejs";

function GraphVisualization({ graph }) {
  if (!graph || !graph.nodes || graph.nodes.length === 0) {
    return (
      <div style={{ height: "500px", display: "flex", alignItems: "center", justifyContent: "center" }}>
        No graph data available
      </div>
    );
  }

  // Build Cytoscape elements
  const elements = [
    ...graph.nodes.map((n) => {
      const nodeColor = n.suspicious
        ? "#8B0000"   // Dark Red
        : "#87CEEB";  // Sky Blue

      return {
        data: {
          id: n.account_id,
          label: n.account_id,
          suspicion_score: n.suspicion_score,
          suspicious: n.suspicious,
          ring_id: n.ring_id,
        },
        classes: n.suspicious ? "suspicious" : "normal",
        style: {
          backgroundColor: nodeColor,
          borderColor: n.suspicious ? "#FFFFFF" : "#5DADE2",
          borderWidth: n.suspicious ? 4 : 2,
          width: n.suspicious ? 50 : 35,
          height: n.suspicious ? 50 : 35,
        }
      };
    }),
    ...graph.edges.map((e) => ({
      data: {
        source: e.from,
        target: e.to,
        id: `${e.from}-${e.to}`,
      },
      classes: "edge",
    })),
  ];

  const stylesheet = [
    {
      selector: "node",
      style: {
        label: "data(label)",
        backgroundColor: "#87CEEB",  // Sky Blue
        color: "#ffffff",
        fontSize: 9,
        fontWeight: "normal",
        width: 35,
        height: 35,
        borderWidth: 2,
        borderColor: "#5DADE2",
        textValign: "center",
        textHalign: "center",
      },
    },
    {
      selector: "node.suspicious",
      style: {
        backgroundColor: "#8B0000", // Dark Red
        borderWidth: 4,
        borderColor: "#FFFFFF",
        width: 50,
        height: 50,
        fontSize: 10,
        fontWeight: "bold",
      },
    },
    {
      selector: "edge",
      style: {
        width: 2,
        lineColor: "#006400",        // Dark Green
        targetArrowShape: "triangle",
        targetArrowColor: "#006400", // Dark Green
        curveStyle: "bezier",
        opacity: 0.9,
      },
    },
  ];

  const layout = {
    name: "cose",
    directed: true,
    animate: false,
    animationDuration: 500,
    avoidOverlap: true,
    nodeSpacing: 10,
  };

  return (
    <div style={{ height: "500px", border: "1px solid #ddd", position: "relative" }}>
      <CytoscapeComponent
        elements={elements}
        style={{ width: "100%", height: "100%" }}
        layout={layout}
        stylesheet={stylesheet}
        wheelSensitivity={0.1}
      />

      <div style={{
        position: "absolute",
        bottom: 10,
        right: 10,
        fontSize: "12px",
        color: "#666",
        backgroundColor: "rgba(255, 255, 255, 0.9)",
        padding: "8px 12px",
        borderRadius: "4px",
        maxWidth: "200px"
      }}>
        <div><strong>Legend:</strong></div>

        <div style={{ marginTop: "4px" }}>
          <span style={{
            display: "inline-block",
            width: "12px",
            height: "12px",
            backgroundColor: "#87CEEB",
            marginRight: "6px",
            borderRadius: "2px"
          }}></span>
          Normal Account
        </div>

        <div style={{ marginTop: "4px" }}>
          <span style={{
            display: "inline-block",
            width: "12px",
            height: "12px",
            backgroundColor: "#8B0000",
            marginRight: "6px",
            borderRadius: "2px",
            border: "1px solid white"
          }}></span>
          Suspicious Account
        </div>
      </div>
    </div>
  );
}

export default GraphVisualization;