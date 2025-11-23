"use client";

import Link from "next/link";
import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { FiMapPin, FiCloudRain, FiDroplet, FiActivity } from "react-icons/fi";
import { FiArrowLeft } from "react-icons/fi";


type YearData = {
  predicted_rainfall_mm: number;
  predicted_collection_liters: number;
};

type ImpactResult = {
  building_area?: number;
  predicted_rainfall?: Record<string, YearData>;
};

export default function ImpactPage() {
  const [address, setAddress] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<ImpactResult | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/api/geocode", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address }),
      });

      if (!response.ok) {
        throw new Error("Failed to get prediction from HydraX engine.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Unknown error while contacting the backend.");
    } finally {
      setLoading(false);
    }
  };

  // Derived stats for dashboard cards
  const stats = useMemo(() => {
    if (!result?.predicted_rainfall) return null;

    const entries = Object.entries(result.predicted_rainfall);
    if (entries.length === 0) return null;

    let totalRain = 0;
    let totalLitres = 0;
    let maxRain = 0;

    for (const [, data] of entries) {
      totalRain += data.predicted_rainfall_mm;
      totalLitres += data.predicted_collection_liters;
      maxRain = Math.max(maxRain, data.predicted_rainfall_mm);
    }

    const avgRain = totalRain / entries.length;

    return {
      years: entries.length,
      avgRain,
      maxRain,
      totalLitres,
    };
  }, [result]);

  return (
    <main className="hx-page">
      <section className="hx-section">
        <div className="hx-container hx-reveal">
          {/* Header */}
          <motion.div
            className="hx-section-header"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
          >
            <p className="hx-section-kicker">Impact Dashboard</p>
            <h1 className="hx-section-title">
              HydraX rainwater intelligence at the building scale
            </h1>
            <p className="hx-section-subtitle">
              Enter a London address to estimate rooftop area, projected
              rainfall, and how much clean rainwater could be captured over
              time — for both the building and the wider city.
            </p>
          </motion.div>

          {/* Top layout: form + key metrics */}
          <div className="hx-split">
            {/* Left: Address form & status */}
            <motion.div
              className="hx-card"
              id="lastDiv"
              initial={{ opacity: 0, x: -25 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1, duration: 1 }}
            >
              <h2 className="hx-step-title" style={{ marginBottom: "0.75rem" }}>
                Address-level impact probe
              </h2>
              <p className="hx-body-text" style={{ marginBottom: "1rem" }}>
                HydraX uses the entered address as an anchor point for rooftop
                geometry and rainfall projections. This is a prototype view for
                the Sheridan Datathon.
              </p>

              <form
                onSubmit={handleSubmit}
                className="hx-form"
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "0.75rem",
                  marginTop: "0.5rem",
                }}
              >
                <label
                  htmlFor="address"
                  className="hx-body-text"
                  style={{ fontWeight: 500, display: "flex", gap: 8, alignItems: "center" }}
                >
                  <FiMapPin />
                  Enter a London address
                </label>
                <input
                  id="address"
                  type="text"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="e.g. 10 Downing Street, London"
                  required
                  className="hx-input"
                  style={{
                    padding: "12px 14px",
                    borderRadius: "12px",
                    border: "1px solid rgba(255,255,255,0.08)",
                    background:
                      "radial-gradient(circle at top left, rgba(88, 255, 244, 0.12), rgba(5, 10, 15, 0.95))",
                    color: "#f7fdfb",
                    outline: "none",
                    fontSize: "0.95rem",
                  }}
                />

                <motion.button
                  type="submit"
                  className="hx-btn hx-btn-primary"
                  whileHover={{ scale: loading ? 1 : 1.02 }}
                  whileTap={{ scale: loading ? 1 : 0.98 }}
                  disabled={loading}
                  style={{
                    marginTop: "0.25rem",
                    alignSelf: "flex-start",
                    minWidth: "220px",
                  }}
                >
                  {loading ? "Running HydraX model…" : "Get Impact Prediction"}
                </motion.button>
              </form>

              {/* Error / helper text */}
              <div style={{ marginTop: "2rem", minHeight: "1.5rem" }}>
                {error && (
                  <p style={{ color: "#ff6b81", fontSize: "0.9rem" }}>{error}</p>
                )}
                {!error && !result && !loading && (
                  <p
                    style={{
                      color: "rgba(200, 231, 222, 0.7)",
                      fontSize: "0.85rem",
                    }}
                  >
                    Tip: make sure the address is in London.
                  </p>
                )}
              </div>

              {/* Loading shimmer */}
              {loading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="hx-loading-bar"
                  style={{
                    marginTop: "1rem",
                    height: "4px",
                    borderRadius: "999px",
                    overflow: "hidden",
                    background: "rgba(255,255,255,0.06)",
                  }}
                >
                  <motion.div
                    style={{
                      height: "100%",
                      width: "40%",
                      background:
                        "linear-gradient(90deg, #57cc99, #80ed99, #c7f9cc)",
                    }}
                    animate={{
                      x: ["-40%", "120%"],
                    }}
                    transition={{
                      duration: 0.7,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  />
                </motion.div>
              )}
            </motion.div>

            {/* Right: Summary cards */}
            <motion.div
              className="hx-card"
              id="realLast"
              initial={{ opacity: 0, x: 25 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.15, duration: 0.7 }}
              style={{ width: "350px"}}
            >
              <h2 className="hx-step-title" style={{ marginBottom: "0.75rem" }}>
                Snapshot metrics
              </h2>
              <p className="hx-body-text" style={{ marginBottom: "1.25rem" }}>
                These prototype indicators show how much rainfall could be
                captured and how intense future rain years might be.
              </p>

              <div
                className="hx-impact-metrics"
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                  gap: "0.9rem",
                }}
              >
                <DashboardCard
                  icon={<FiCloudRain />}
                  label="Years projected"
                  value={stats ? stats.years.toString() : "—"}
                />
                <DashboardCard
                  icon={<FiDroplet />}
                  label="Avg. yearly rainfall"
                  value={
                    stats ? `${stats.avgRain.toFixed(1)} mm` : "Awaiting input"
                  }
                />
                <DashboardCard
                  icon={<FiActivity />}
                  label="Peak rainfall year"
                  value={stats ? `${stats.maxRain.toFixed(1)} mm` : "—"}
                />
                <DashboardCard
                  icon={<FiDroplet />}
                  label="Total captured water"
                  value={
                    stats
                      ? `${(stats.totalLitres / 1000).toFixed(1)} kL`
                      : "—"
                  }
                />
              </div>

              {result?.building_area && (
                <div
                  style={{
                    marginTop: "1.25rem",
                    padding: "0.85rem 1rem",
                    borderRadius: "12px",
                    background:
                      "linear-gradient(135deg, rgba(87,204,153,0.12), rgba(7,25,37,0.9))",
                    border: "1px solid rgba(87,204,153,0.3)",
                    fontSize: "0.9rem",
                  }}
                >
                  Rooftop coverage detected:{" "}
                  <strong>
                    {Number(result.building_area).toFixed(2)} m²
                  </strong>{" "}
                  of potential rainwater collection surface.
                </div>
              )}
            </motion.div>
          </div>

          {/* Detailed table */}
          {result?.predicted_rainfall && (
            <motion.section
              className="hx-card"
              style={{ marginTop: "2rem" }}
              initial={{ opacity: 0, y: 25 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
            >
              <div className="hx-section-header" style={{ marginBottom: "1rem" }}>
                <h2 className="hx-section-title" style={{ fontSize: "1.4rem" }}>
                  Year-by-year rainfall & captured water
                </h2>
                <p className="hx-section-subtitle">
                  Prototype 20-year projection for the selected address. Values
                  are estimates only and can be refined with more detailed
                  hydrological models.
                </p>
              </div>

              <div
                style={{
                  overflowX: "auto",
                  borderRadius: "12px",
                  border: "1px solid rgba(255,255,255,0.06)",
                }}
              >
                <table
                  style={{
                    width: "100%",
                    borderCollapse: "collapse",
                    minWidth: "420px",
                  }}
                >
                  <thead>
                    <tr
                      style={{
                        background: "rgba(15, 45, 64, 0.95)",
                      }}
                    >
                      <th className="hx-table-header">Year</th>
                      <th className="hx-table-header">Predicted Rainfall (mm)</th>
                      <th className="hx-table-header">Captured Water (L)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(result.predicted_rainfall).map(
                      ([year, data]) => (
                        <tr
                          key={year}
                          style={{
                            background: "rgba(5,10,15,0.98)",
                            borderBottom:
                              "1px solid rgba(255,255,255,0.04)",
                          }}
                        >
                          <td className="hx-table-cell">{year}</td>
                          <td className="hx-table-cell">
                            {Number(
                              data.predicted_rainfall_mm
                            ).toFixed(2)}
                          </td>
                          <td className="hx-table-cell">
                            {Number(
                              data.predicted_collection_liters
                            ).toFixed(2)}
                          </td>
                        </tr>
                      )
                    )}
                  </tbody>
                </table>
              </div>
            </motion.section>
          )}

      {/* Back Button */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        style={{
          position: "absolute",
          top: "80px",
          right: "12.59%",
          display: "flex",
          alignItems: "center",
          gap: "8px",
        }}
      >
        <Link href="/" className="hx-btn-back">
          <FiArrowLeft size={16} />
          <span>Back to Home</span>
        </Link>
      </motion.div>
        </div>
      </section>
    </main>
  );


type DashboardCardProps = {
  icon: React.ReactNode;
  label: string;
  value: string;
};

function DashboardCard({ icon, label, value }: DashboardCardProps) {
  return (
    <motion.div
      className="hx-mini-chart"
      whileHover={{ y: -3, scale: 1.01 }}
      transition={{ duration: 0.2 }}
      style={{
        padding: "0.85rem 0.9rem",
        borderRadius: "14px",
        background:
          "radial-gradient(circle at top, rgba(34,87,122,0.9), rgba(5,10,15,0.95))",
        border: "1px solid rgba(255,255,255,0.06)",
        boxShadow: "var(--hx-shadow-soft, 0 18px 40px rgba(0,0,0,0.45))",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          marginBottom: 4,
          fontSize: "0.8rem",
          textTransform: "uppercase",
          letterSpacing: "0.06em",
          opacity: 0.8,
        }}
      >
        <span>{icon}</span>
        <span>{label}</span>
      </div>
      <div style={{ fontSize: "1.1rem", fontWeight: 600 }}>{value}</div>
    </motion.div>
  );
}}
