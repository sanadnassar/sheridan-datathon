"use client";
// app/page.tsx
import Link from "next/link";
import {SiPython, SiReact, SiFlask, SiNextdotjs, SiTailwindcss, SiJavascript,
SiTypescript, SiNodedotjs,SiHtml5, SiCss3, SiGithub} from "react-icons/si";
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
              HydraX is an AI-powered sustainability tool that helps the city of
              London, UK measure and visualize its rainwater harvesting
              potential. By combining open-source environmental data with
              geospatial analytics, HydraX calculates how much rainwater could
              be collected from rooftops, visualizing the potential savings in
              both liters of water and reduced stormwater runoff.
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
              Urban areas lose millions of litres of clean rainwater every year
              due to inefficient drainage and lack of collection systems. HydraX
              helps city planners and sustainability teams quantify what&apos;s
              possible, before expensive infrastructure decisions are made.
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
                <li>How much rainwater can be harvested city-wide or by district.</li>
                <li>Which rooftops offer the highest collection potential.</li>
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
                <li>More efficient water use and access to clean water for families.</li>
                <li>Reduced pressure on stormwater systems during heavy rainfall.</li>
                <li>Better planning of green roofs and blue-green infrastructure.</li>
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
                <SiReact title="React" size={30}/>
                <SiHtml5 title="Html" size={30}/>
                <SiCss3 title="Css" size={30}/>
                <SiJavascript title="Javascript" size={30}/>
                <SiFlask title="Flask" size={30}/>
                <SiNextdotjs title="Nextdotjs" size={30}/>
                <SiGithub title="Github" size={30}/>
              </p>
            </div>
            <div className="hx-team-card">
              <p className="hx-team-role">Full-stack Engineer</p>
              <p className="hx-team-name">Shaun Malhotra</p>
              <p className="hx-team-note">
                Backend APIs, integration with mapping libraries.
                Git version control and collaborative workflow management.
              </p>
            </div>
            <div className="hx-team-card">
              <p className="hx-team-role">AI Engineer</p>
              <p className="hx-team-name">Ethan Wang</p>
              <p className="hx-team-note">
                Model training, data preprocessing, and API deployment for rainfall
                and spatial prediction systems.
              </p>
            </div>
              <div className="hx-team-card">
              <p className="hx-team-role">Data Engineer</p>
              <p className="hx-team-name">ML Engineer</p>
              <p className="hx-team-note">
                Data collection, cleaning, and structuring.
                Development of data pipelines and preparation of datasets for AI analysis.
              </p>
            </div>
              <div className="hx-team-card">
              <p className="hx-team-role">UX &amp; Storytelling</p>
              <p className="hx-team-name">Teammate 3</p>
              <p className="hx-team-note">
                Narrative, SDG framing and interface polish for the demo.
              </p>
            </div>

          </div>
        </div>
      </section>

      <footer className="hx-footer">
        <div className="hx-footer-inner">
          <p>© {new Date().getFullYear()} HydraX. Built for the GDG Datathon.</p>
          <div className="hx-footer-links">
            {/* Put your real repo link here */}
            <a
              href="https://github.com/your-username/hydrax"
              target="_blank"
              rel="noreferrer"
            >
              GitHub Repo
            </a>
            <span>•</span>
            <span>SDG 6 · SDG 11 · SDG 13 (SDG 9 via innovation)</span>
          </div>
        </div>
      </footer>
    </main>
  );
}
