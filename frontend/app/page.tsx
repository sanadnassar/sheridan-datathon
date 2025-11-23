"use client";
// app/page.tsx
import Link from "next/link";
import {SiPython, SiReact, SiFlask, SiNextdotjs, SiFastapi, SiJavascript,
SiTypescript, SiNodedotjs,SiHtml5, SiCss3, SiGithub, SiSqlite} from "react-icons/si";
import { useEffect } from "react";

export default function HomePage() {
  // simple fade-in on scroll
  useEffect(() => {
    const elements = document.querySelectorAll(".hx-reveal");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("hx-visible");
          }
        });
      },
      { threshold: 0.1 }
    );

    elements.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  return (
    <main className="hx-page">
      {/* NAVBAR */}
      <header className="hx-navbar">
        <div className="hx-nav-inner">
          <div className="hx-logo">
            <div className="hx-logo-mark" />
            <span>HydraX</span>
          </div>
          <nav className="hx-nav-links">
            <a href="#about">About</a>
            <a href="#problem">Problem</a>
            <a href="#solution">Solution</a>
            <a href="#impact">Impact</a>
            <a href="#team">Team</a>
          </nav>
        </div>
      </header>

      {/* HERO */}
      <section id="hero" className="hx-section hx-hero">
        <div className="hx-container hx-hero-inner">
          <div className="hx-hero-text hx-reveal">
            <div className="hx-badge">
              <span className="hx-badge-dot" />
              <span>AI for Sustainable Cities</span>
            </div>
            <h1 className="hx-hero-title">
              HydraX
              <span className="hx-hero-gradient">
                {" "}
                Rainwater Intelligence for London
              </span>
            </h1>
            <p className="hx-hero-subtitle">
              HydraX is a sustainability intelligence platform focused on maximizing London’s rainwater potential. By combining rooftop geometry with predictive rainfall analytics, HydraX estimates how much rainwater can be captured by each household — helping residents, planners, and policymakers understand their water-saving potential. The tool supports long-term feasibility planning for installing rooftop water reclamation systems, turning rainfall into a practical, sustainable water source for the city.
            </p>
            <p className="hx-hero-meta">
              Aligned with SDG 6, 11 &amp; 13 • Designed for planners,
              sustainability teams &amp; citizens.
            </p>

            <div className="hx-hero-actions">
              <a href="#about" className="hx-btn hx-btn-primary">
                Learn More
              </a>
              <a href="#impact" className="hx-btn hx-btn-ghost">
                View Impact
              </a>
            </div>

            <p className="hx-hero-note">
              Powered by open environmental datasets, rooftop detection and
              geospatial analytics.
            </p>
          </div>

          <div className="hx-hero-visual hx-reveal">
            <Link href="/impact" className="hx-hero-card hx-card-link" target="_self">
              <p className="hx-hero-card-title">
                London Rainwater Harvesting Snapshot (Prototype)
              </p>
              <div className="hx-hero-grid">
                <div className="hx-metric">
                  <p className="hx-metric-label">Annual Harvest Potential</p>
                  <p className="hx-metric-value">≈ 120M L</p>
                  <p className="hx-metric-tag">Clean rainwater</p>
                </div>
                <div className="hx-metric">
                  <p className="hx-metric-label">Stormwater Reduction</p>
                  <p className="hx-metric-value">-18%</p>
                  <p className="hx-metric-tag">Runoff on peak days</p>
                </div>
                <div className="hx-metric">
                  <p className="hx-metric-label">High-yield rooftops</p>
                  <p className="hx-metric-value">3,250+</p>
                  <p className="hx-metric-tag">Priority buildings</p>
                </div>
                <div className="hx-metric">
                  <p className="hx-metric-label">District coverage</p>
                  <p className="hx-metric-value">32</p>
                  <p className="hx-metric-tag">Boroughs analysed</p>
                </div>
              </div>
            </Link>
          </div>
        </div>
      </section>

      {/* ABOUT */}
      <section id="about" className="hx-section hx-section-alt">
        <div className="hx-container hx-reveal">
          <div className="hx-section-header">
            <p className="hx-section-kicker">About HydraX</p>
            <h2 className="hx-section-title">
              Turning London&apos;s rooftops into a hidden water reservoir
            </h2>
            <p className="hx-section-subtitle">
            Urban areas lose millions of litres of clean rainwater
            every year due to inefficient drainage and the absence of
            localized collection systems. HydraX empowers city planners, sustainability teams,
            and homeowners to quantify rooftop rainwater potential using predictive rainfall analytics — providing clear
            insights before investing in large-scale infrastructure.
            </p>
          </div>

          <div className="hx-split">
            <div className="hx-card">
              <h3>Data-driven insight for real decisions</h3>
              <p className="hx-body-text">
                HydraX uses open-source rainfall data, building footprints and
                rooftop area estimates to model how much water can be captured
                across London. The result is a geospatial layer that highlights:
              </p>
              <ul className="hx-list">
                <li>How much rainwater can be harvested city-wide or by address.</li>
                <li>How much water collection potential your rooftop has.</li>
                <li>
                  How rainfall patterns and urban density affect sustainable
                  water planning.
                </li>
              </ul>
            </div>

            <div className="hx-card">
              <h3>Why it matters</h3>
              <p className="hx-body-text">
                By revealing untapped rainwater resources, HydraX supports:
              </p>
              <ul className="hx-list">
                <li>Communities gaining better access to clean water by reducing dependence on overburdened municipal water systems. (SDG 6)</li>
                <li>The Development of resilient, water-smart cities that can better handle flooding and drought conditions. (SDG 11)</li>
                <li>Cities adapting to the impacts of climate change through solutions that reduce urban flooding from poor drainage systems. (SDG 13)</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* PROBLEM */}
      <section id="problem" className="hx-section">
        <div className="hx-container hx-reveal">
          <div className="hx-section-header">
            <p className="hx-section-kicker">The Problem</p>
            <h2 className="hx-section-title">
              Millions of litres of rainwater wasted. Streets still flood.
            </h2>
            <p className="hx-section-subtitle">
              London receives significant annual rainfall, yet most of it rushes
              straight into drains. Families face water stress, cities face
              overwhelmed drainage systems, and planners lack a clear map of
              where water can be stored at the building scale.
            </p>
          </div>

          <div className="hx-card">
            <p className="hx-body-text">
              Without a clear view of rooftop potential, rainwater harvesting
              decisions are slow, fragmented and reactive. HydraX replaces
              guesswork with actionable geospatial intelligence that supports
              SDG 6 (Clean Water), SDG 11 (Sustainable Cities) and SDG 13
              (Climate Action).
            </p>
          </div>
        </div>
      </section>

      {/* SOLUTION / HOW IT WORKS */}
      <section id="solution" className="hx-section hx-section-alt">
        <div className="hx-container">
          <div className="hx-section-header hx-reveal">
            <p className="hx-section-kicker">Our Solution</p>
            <h2 className="hx-section-title">
              HydraX: AI + geospatial analytics for rooftop rainwater
            </h2>
            <p className="hx-section-subtitle">
              HydraX layers rainfall data, rooftop geometry and urban
              characteristics into a single interactive map, showing where the
              city can store water before it becomes stormwater.
            </p>
          </div>

          <div className="hx-steps hx-reveal">
            <div className="hx-step-card">
              <p className="hx-step-index">Step 1 · Ingest</p>
              <h3 className="hx-step-title">Open environmental &amp; urban data</h3>
              <p className="hx-step-body">
                HydraX pulls in rainfall history, rooftop polygons, elevation
                and land-use data from open-source and municipal datasets for
                the London area.
              </p>
            </div>
            <div className="hx-step-card">
              <p className="hx-step-index">Step 2 · Analyse</p>
              <h3 className="hx-step-title">AI-powered rooftop potential</h3>
              <p className="hx-step-body">
                We estimate rainwater capture per building using roof area,
                slope assumptions and rainfall intensity, then classify
                rooftops into low, medium and high-yield opportunities.
              </p>
            </div>
            <div className="hx-step-card">
              <p className="hx-step-index">Step 3 · Visualize</p>
              <h3 className="hx-step-title">Interactive city-scale dashboard</h3>
              <p className="hx-step-body">
                City planners explore districts, filter by yield class and
                simulate how installing harvesting systems impacts stormwater
                runoff and water availability.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* IMPACT */}
      <section id="impact" className="hx-section">
        <div className="hx-container hx-impact-grid hx-reveal">
          <div>
            <div className="hx-section-header">
              <p className="hx-section-kicker">Impact</p>
              <h2 className="hx-section-title">
                From wasted rainfall to resilient, water-smart neighbourhoods
              </h2>
              <p className="hx-section-subtitle">
                HydraX helps families gain more access to clean water, supports
                cities in reducing stormwater waste, and informs investments in
                green infrastructure.
              </p>
            </div>

            <div className="hx-impact-metrics">
              <div className="hx-impact-pill">
                <h4>Clean Water Access</h4>
                <p>
                  Estimate how many households could be supported with rooftop
                  rainwater storage during dry periods.
                </p>
              </div>
              <div className="hx-impact-pill">
                <h4>Stormwater Relief</h4>
                <p>
                  Visualize reductions in runoff volume for extreme rainfall
                  scenarios at borough or city scale.
                </p>
              </div>
              <div className="hx-impact-pill">
                <h4>Green Coverage</h4>
                <p>
                  Identify rooftops where green roofs + harvesting systems can
                  boost canopy and cooling.
                </p>
              </div>
              <div className="hx-impact-pill">
                <h4>Investment Planning</h4>
                <p>
                  Prioritize districts where every litre captured delivers the
                  greatest climate and social benefit.
                </p>
              </div>
            </div>
          </div>

          <div className="hx-mini-chart">
            <h3>Prototype Impact Scenario</h3>
            <p className="hx-body-text">
              Example scenario if high-potential rooftops installed harvesting
              systems:
            </p>
            <div className="hx-chart-bars">
              <div>
                <div className="hx-bar hx-bar-1" />
                <p className="hx-bar-label">Rainwater captured</p>
              </div>
              <div>
                <div className="hx-bar hx-bar-2" />
                <p className="hx-bar-label">Runoff reduction</p>
              </div>
              <div>
                <div className="hx-bar hx-bar-3" />
                <p className="hx-bar-label">Households supported</p>
              </div>
            </div>
            <p className="hx-chart-caption">
              These values are placeholders for the datathon prototype and can
              be updated with real model outputs.
            </p>
          </div>
        </div>
      </section>

      {/* TEAM & FOOTER */}
      <section id="team" className="hx-section hx-section-alt">
        <div className="hx-container hx-reveal">
          <div className="hx-section-header">
            <p className="hx-section-kicker">Meet The Team</p>
            <p className="hx-section-subtitle">
              We’re a team of computer and data scientists building AI tools
              that drive real-world impact — one breakthrough at a time.
            </p>
          </div>

          <div className="hx-team-grid">
            <div className="hx-team-card">
              <p className="hx-team-role">Frontend & Visualization Engineer</p>
              <p className="hx-team-name">Sanad Nassar</p>
              <p className="hx-team-note">
                Frontend development and UI integration for rainfall modeling,
                rooftop potential, and spatial analysis tools.
              </p>
              <p className="hx-team-hover-text">
              <SiReact title="React" size={30} color="#61DAFB" />
              <SiHtml5 title="HTML" size={30} color="#E34F26" />
              <SiCss3 title="CSS" size={30} color="#1572B6" />
              <SiJavascript title="JavaScript" size={30} color="#F7DF1E" />
              <SiNextdotjs title="Next.js" size={30} color="#433d3dff" />
              <SiGithub title="GitHub" size={30} color="#ffffffff" />
              </p>
            </div>
            <div className="hx-team-card">
              <p className="hx-team-role">Full-stack Engineer</p>
              <p className="hx-team-name">Shaun Malhotra</p>
              <p className="hx-team-note">
                Backend APIs, integration with mapping libraries.
                Git version control and collaborative workflow management.
              </p>
              <p className="hx-team-hover-text">
              <SiPython title="Python" size={30} color="#3776AB" />
              <SiFastapi title="FastAPI" size={30} color="#009688" />
              <SiFlask title="Flask" size={30} color="#ef0000ff" />
              <SiNextdotjs title="Next.js" size={30} color="#433d3dff" />
              <SiGithub title="GitHub" size={30} color="#ffffff" />
              </p>
            </div>
            <div className="hx-team-card">
              <p className="hx-team-role">AI Engineer</p>
              <p className="hx-team-name">Ethan Wang</p>
              <p className="hx-team-note">
                Model training, data preprocessing, and API deployment for rainfall
                and spatial prediction systems.
              </p>
              <p className="hx-team-hover-text">
              <SiPython title="Python" size={30} color="#3776AB" />
              <SiFastapi title="FastAPI" size={30} color="#009688" />
              <SiFlask title="Flask" size={30} color="#ef0000ff" />
              <SiNextdotjs title="Next.js" size={30} color="#433d3dff" />
              <SiGithub title="GitHub" size={30} color="#FFFFFF" />
              </p>
            </div>
              <div className="hx-team-card">
              <p className="hx-team-role">Data Engineer</p>
              <p className="hx-team-name">Lopey Soleye</p>
              <p className="hx-team-note">
                Data collection, cleaning, and structuring.
                Development of data pipelines and preparation of datasets for AI analysis.
              </p>
              <p className="hx-team-hover-text">
                <SiPython title="Python" size={30} color="#3776AB" />
                <SiSqlite title="SQLite" size={30} color="#adc166ff" />
                <SiFlask title="Flask" size={30} color="#ef0000ff" />
                <SiNextdotjs title="Next.js" size={30} color="#433d3dff" />
                <SiGithub title="GitHub" size={30} color="#ffffffff" />
              </p>
            </div>
              <div className="hx-team-card">
              <p className="hx-team-role">Database Architect</p>
              <p className="hx-team-name">Hana</p>
              <p className="hx-team-note">
                Implements spatial indexing and
                efficient data retrieval for large-scale building and
                rainfall datasets.
              </p>
              <p className="hx-team-hover-text">
              <SiPython title="Python" size={30} color="#3776AB" />
              <SiSqlite title="SQLite" size={30} color="#adc166ff" />
              <SiFlask title="Flask" size={30} color="#ef0000ff" />
              <SiNextdotjs title="Next.js" size={30} color="#433d3dff" />
              <SiGithub title="GitHub" size={30} color="#FFFFFF" />
              </p>
            </div>

          </div>
        </div>
      </section>

      <footer className="hx-footer">
        <div className="hx-footer-inner">
          <p>© {new Date().getFullYear()} HydraX. Built for Sheridan Datathon.</p>
          <div className="hx-footer-links" style={{ cursor: "pointer" }}>
            {/* Put your real repo link here */}
            <a
              href="https://github.com/sanadnassar/HydraX"
              target="_blank"
              rel="noreferrer"
              style={{ cursor: "pointer"}}
            >
              <SiGithub title="Github" size={15} className="hx-footer-links" style={{ cursor: "pointer" }}/>
              <span className="hx-footer-links" style={{ cursor: "pointer" }}> - Github Repository</span>
            </a>
          </div>
        </div>
      </footer>
    </main>
  );
}
