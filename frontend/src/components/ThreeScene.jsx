import React, { useRef, useEffect } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

function Network() {
  const groupRef = useRef();
  const mouse = useRef(new THREE.Vector2(0, 0));

  const nodeCount = 120;
  const nodes = [];
  const linePositions = [];

  // Generate nodes
  for (let i = 0; i < nodeCount; i++) {
    nodes.push(
      new THREE.Vector3(
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20
      )
    );
  }

  // Create connections (distance based)
  for (let i = 0; i < nodeCount; i++) {
    for (let j = i + 1; j < nodeCount; j++) {
      const dist = nodes[i].distanceTo(nodes[j]);
      if (dist < 4) {
        linePositions.push(
          nodes[i].x,
          nodes[i].y,
          nodes[i].z,
          nodes[j].x,
          nodes[j].y,
          nodes[j].z
        );
      }
    }
  }

  useEffect(() => {
    const handleMove = (e) => {
      mouse.current.x = (e.clientX / window.innerWidth) - 0.5;
      mouse.current.y = (e.clientY / window.innerHeight) - 0.5;
    };

    const handleTouch = (e) => {
      const touch = e.touches[0];
      mouse.current.x = (touch.clientX / window.innerWidth) - 0.5;
      mouse.current.y = (touch.clientY / window.innerHeight) - 0.5;
    };

    window.addEventListener("mousemove", handleMove);
    window.addEventListener("touchmove", handleTouch);

    return () => {
      window.removeEventListener("mousemove", handleMove);
      window.removeEventListener("touchmove", handleTouch);
    };
  }, []);

  useFrame(() => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.001;
      groupRef.current.rotation.x = mouse.current.y * 1.5;
      groupRef.current.rotation.y += mouse.current.x * 0.02;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Nodes */}
      {nodes.map((pos, i) => (
        <mesh key={i} position={pos}>
          <sphereGeometry args={[0.12, 8, 8]} />
          <meshBasicMaterial color="#2563eb" />
        </mesh>
      ))}

      {/* Lines */}
      <lineSegments>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            array={new Float32Array(linePositions)}
            count={linePositions.length / 3}
            itemSize={3}
          />
        </bufferGeometry>
        <lineBasicMaterial color="#60a5fa" transparent opacity={0.4} />
      </lineSegments>
    </group>
  );
}

export default function ThreeScene() {
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100vh",
        zIndex: -1,
        pointerEvents: "none",
        background: "#0f172a", // dark fintech background
      }}
    >
      <Canvas camera={{ position: [0, 0, 18] }}>
        <Network />
      </Canvas>
    </div>
  );
}