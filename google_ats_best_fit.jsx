import { useState } from "react";

const CATEGORIES = ["All", "SRE", "EngProd / CI", "Cloud Infra", "Embedded / Firmware", "AI/ML Infra"];

const roles = [
{
id: 1,
title: "Senior SWE, Site Reliability Engineering",
team: "SRE — Core (Google Search, Ads, Gmail, YouTube)",
category: "SRE",
locations: ["Raleigh/Durham, NC"],
level: "L5",
salary: "$166K–$244K",
remote: false,
url: "https://careers.google.com/jobs/results/139247466443612870-senior-software-engineer/",
required: [
{ skill: "Software development in any language (5+ yrs)", weight: 22 },
{ skill: "Large-scale distributed systems — design, analysis, troubleshooting (3+ yrs)", weight: 25 },
{ skill: "Technical project leadership (2+ yrs)", weight: 18 },
],
preferred: [
{ skill: "M.S. or Ph.D in CS or Engineering", weight: 15 },
{ skill: "Observability, reliability, on-call automation", weight: 12 },
{ skill: "Cross-functional technical leadership", weight: 8 },
],
candidateScores: {
required: [
{ score: 99, note: "8+ years multi-language: Python, C++, Go, JS/TS, Rust — far exceeds threshold" },
{ score: 88, note: "k3s cluster infra, AV CI/CD at NVIDIA, ARM K8s cluster at LM — strong distributed systems footprint" },
{ score: 90, note: "Led 10-engineer team at LM, leads AV infra platform at NVIDIA, mentored 6 engineers" },
],
preferred: [
{ score: 100, note: "M.S. Computer Science, UCF 2021" },
{ score: 85, note: "On-call Slack agent, Jenkins pipeline health, DDU validation — directly relevant to SRE mission" },
{ score: 87, note: "Cross-functional at LM (embedded + software), AV infra spans GPU/build/test" },
],
},
whyFit: "SRE is effectively your current job at NVIDIA. Incident triage automation, pipeline reliability, and self-healing CI agents map 1:1 to Google SRE's mission. Strongest overall match on the board.",
},
{
id: 2,
title: "Senior SWE, SRE, Google Cloud",
team: "SRE — Google Cloud",
category: "SRE",
locations: ["Raleigh/Durham, NC", "Pittsburgh, PA", "New York, NY", "Seattle, WA"],
level: "L5",
salary: "$166K–$244K",
remote: false,
url: "https://www.google.com/about/careers/applications/jobs/results/126939198258062022-senior-software-engineer-site-reliability-engineering-google-cloud",
required: [
{ skill: "Software development in any language (5+ yrs)", weight: 20 },
{ skill: "Data structures / algorithms (5+ yrs)", weight: 15 },
{ skill: "Large-scale distributed systems — design, analysis, troubleshooting (3+ yrs)", weight: 25 },
{ skill: "Technical project leadership (2+ yrs)", weight: 15 },
],
preferred: [
{ skill: "M.S. in CS or Engineering", weight: 12 },
{ skill: "Cloud-native operations / SRE tooling", weight: 13 },
],
candidateScores: {
required: [
{ score: 99, note: "8+ years, Python/C++/Go/Rust — extremely strong" },
{ score: 82, note: "Implied by large-scale systems work; not explicitly highlighted on resume" },
{ score: 88, note: "Same as above SRE role — distributed infra strong" },
{ score: 90, note: "Demonstrated at LM and NVIDIA" },
],
preferred: [
{ score: 100, note: "M.S. CS" },
{ score: 80, note: "Kubernetes, Helm, Terraform, Jenkins, Bazel — strong cloud-native stack" },
],
},
whyFit: "Cloud SRE extends your existing NVIDIA and LM infra patterns directly into cloud operations. The Terraform/K8s/Helm toolchain you built at LM is exactly what Cloud SRE teams run.",
},
{
id: 3,
title: "Senior SWE, Workspace Cloud Infrastructure",
team: "Google Workspace",
category: "Cloud Infra",
locations: ["Raleigh/Durham, NC (Remote eligible)"],
level: "L5",
salary: "$174K–$255K",
remote: true,
url: "https://careers.google.com/jobs/results/109062984432526022-senior-software-engineer/",
required: [
{ skill: "Java and C++ software development (5+ yrs)", weight: 22 },
{ skill: "Testing, maintaining, or launching software products (3+ yrs)", weight: 18 },
{ skill: "Software design and architecture (1+ yr)", weight: 15 },
{ skill: "Technical leadership / mentoring", weight: 10 },
],
preferred: [
{ skill: "Large-scale distributed systems", weight: 15 },
{ skill: "Multi-quarter project ownership", weight: 10 },
{ skill: "Cross-functional influence", weight: 10 },
],
candidateScores: {
required: [
{ score: 72, note: "C++ strong; Java not on resume — notable gap for this JD" },
{ score: 95, note: "20+ CI/CD pipelines at LM, DDU end-to-end automation at NVIDIA — top-tier match" },
{ score: 90, note: "k3s multi-agent system, K8s cluster infra, multi-agent orchestration architecture" },
{ score: 88, note: "10-engineer team at LM, 6 junior mentored, AV infra platform lead" },
],
preferred: [
{ score: 92, note: "k3s, Jenkins, Bazel, GPU-accelerated infra — large-scale systems" },
{ score: 80, note: "DDU automation was multi-quarter; AI triage system was multi-quarter" },
{ score: 85, note: "Cross-org at LM; AV infra at NVIDIA spans multiple teams" },
],
},
whyFit: "Extremely strong on every axis except Java. Adding Java to your skills section (even as 'familiar with') would push this to a near-perfect match. Remote eligible is a major plus.",
},
{
id: 4,
title: "SWE, Engineering Productivity, Google Cloud",
team: "EngProd — Google Cloud Platforms",
category: "EngProd / CI",
locations: ["Kirkland, WA", "Sunnyvale, CA"],
level: "L4",
salary: "$141K–$202K",
remote: false,
url: "https://careers.google.com/jobs/results/75949428141105862-software-engineer-iii-engineering-productivity-google-cloud/",
required: [
{ skill: "C++ software development (2+ yrs)", weight: 20 },
{ skill: "Kubernetes / Google Cloud Platform experience", weight: 22 },
{ skill: "CI/CD tooling — build systems, test infra, automation", weight: 25 },
],
preferred: [
{ skill: "M.S./Ph.D in CS", weight: 10 },
{ skill: "Developer tooling / test frameworks", weight: 13 },
{ skill: "Large-scale build systems (Bazel)", weight: 10 },
],
candidateScores: {
required: [
{ score: 90, note: "C++ used across LM and NVIDIA work; solid foundation" },
{ score: 95, note: "k3s (K8s derivative), Helm, Docker — direct match; no GCP cert but tooling is identical" },
{ score: 97, note: "This is exactly your job. Jenkins pipelines, Bazel builds, AI-driven CI triage, self-healing agents — a nearly perfect description of your NVIDIA work" },
],
preferred: [
{ score: 100, note: "M.S. CS" },
{ score: 95, note: "Claude Code agents, LLM-powered failure analysis, Slack maintainer agent — cutting edge developer tooling" },
{ score: 88, note: "Bazel is explicitly on your resume and used daily at NVIDIA" },
],
},
whyFit: "EngProd is essentially a formalized version of your NVIDIA role. Google's EngProd mission — 'build tools that make engineering easier and better at scale' — is word-for-word what you've been doing. Strongest keyword-to-keyword match on the board.",
},
{
id: 5,
title: "Senior SWE, Embedded Systems & Firmware, Platforms & Devices",
team: "Platforms & Devices (Nest, Pixel, hardware products)",
category: "Embedded / Firmware",
locations: ["Mountain View, CA", "Sunnyvale, CA"],
level: "L5",
salary: "$174K–$255K",
remote: false,
url: "https://careers.google.com/jobs/results/82113414880469702-senior-software-engineer/",
required: [
{ skill: "Software development + data structures/algorithms (5+ yrs)", weight: 20 },
{ skill: "Testing, maintaining, or launching software products (3+ yrs)", weight: 15 },
{ skill: "Embedded OS experience (3+ yrs)", weight: 28 },
],
preferred: [
{ skill: "M.S./Ph.D in CS or related", weight: 10 },
{ skill: "Data structures/algorithms depth (5+ yrs)", weight: 10 },
{ skill: "ARM/ARM64, compilers, kernel, OS, firmware, Rust", weight: 17 },
],
candidateScores: {
required: [
{ score: 95, note: "8+ years, C/C++/Python primary — strong" },
{ score: 90, note: "Yocto OS builds, ARM boards, 20+ CI/CD pipelines at LM — directly relevant" },
{ score: 95, note: "Kernel-level ARM development, Yocto, QEMU, Hyper-V, embedded HIL at LM — exact match" },
],
preferred: [
{ score: 100, note: "M.S. CS + B.S. Aerospace Engineering — strong dual background" },
{ score: 80, note: "Implied via large systems; not explicitly emphasized" },
{ score: 93, note: "ARM/ARM64 explicitly listed, Yocto listed, QEMU/Hyper-V listed, Rust listed — excellent" },
],
},
whyFit: "Your 6-year ARM embedded OS track record at Lockheed is a rare skillset. Google's hardware teams (Pixel, Nest, TPU) need this exact profile. CA location is the only real downside.",
},
{
id: 6,
title: "SWE, AI/ML Networking",
team: "Network Infrastructure / Systems Infrastructure",
category: "AI/ML Infra",
locations: ["Durham/Raleigh, NC"],
level: "L4",
salary: "$147K–$211K",
remote: false,
url: "https://careers.google.com/jobs/results/126366348421800646-software-engineer-aiml-networking/",
required: [
{ skill: "C++ software development (2+ yrs)", weight: 20 },
{ skill: "ML infrastructure (model deployment, eval, optimization)", weight: 20 },
{ skill: "Embedded operating systems (1+ yr)", weight: 15 },
{ skill: "Network protocol / high-bandwidth low-latency env", weight: 12 },
],
preferred: [
{ skill: "M.S./Ph.D in CS", weight: 8 },
{ skill: "Data structures & algorithms", weight: 10 },
{ skill: "ML Infrastructure depth", weight: 15 },
],
candidateScores: {
required: [
{ score: 90, note: "C++ strong across LM and NVIDIA" },
{ score: 75, note: "LangChain/OpenAI/Anthropic/TF/PyTorch — ML tooling solid; not low-level serving infra" },
{ score: 95, note: "Kernel-level ARM embedded OS at LM — direct hit" },
{ score: 38, note: "No networking protocol work visible; infra is CI/CD not network-layer" },
],
preferred: [
{ score: 100, note: "M.S. CS" },
{ score: 80, note: "Complex systems, algorithms implied" },
{ score: 60, note: "Agent orchestration/LLM pipelines — app-layer ML, not kernel/GPU-level ML infra" },
],
},
whyFit: "Strong on C++ and embedded OS, but the networking protocol requirement is a meaningful gap. Good application if you can articulate any exposure to network-layer work.",
},
{
id: 7,
title: "Staff SWE, Google Cloud Storage",
team: "Google Cloud",
category: "Cloud Infra",
locations: ["Raleigh/Durham, NC", "Sunnyvale, CA"],
level: "L6",
salary: "$185K–$283K",
remote: false,
url: "https://careers.google.com/jobs/results/116772894345700038-staff-software-engineer-google-cloud-storage/",
required: [
{ skill: "Software development + algorithms (8+ yrs)", weight: 18 },
{ skill: "Testing & launching software products (5+ yrs)", weight: 15 },
{ skill: "Large-scale infra / distributed systems (5+ yrs)", weight: 20 },
{ skill: "Technical leadership of project teams (3+ yrs)", weight: 15 },
{ skill: "Complex matrixed org cross-functional leadership (3+ yrs)", weight: 12 },
],
preferred: [
{ skill: "M.S./Ph.D in Engineering or CS", weight: 8 },
{ skill: "Staff-level technical direction setting", weight: 12 },
],
candidateScores: {
required: [
{ score: 88, note: "8+ years total experience, multi-language" },
{ score: 88, note: "20+ pipelines, DDU automation — strong but mostly CI/CD flavored not storage infra" },
{ score: 83, note: "k3s, ARM K8s, AV CI/CD — solid but not storage/cloud-native specifically" },
{ score: 72, note: "10-engineer team at LM, NVIDIA platform lead — approaching but not quite Staff-level" },
{ score: 68, note: "Cross-functional at LM; NVIDIA tenure still early (5 months)" },
],
preferred: [
{ score: 100, note: "M.S. CS" },
{ score: 62, note: "Strong individual ownership; staff-level org-wide direction not yet fully demonstrated" },
],
},
whyFit: "A stretch at L6 right now — you're 1-2 years of demonstrated impact away from a clean Staff-level match. Apply now as a long-shot or revisit in 2027 after more NVIDIA tenure.",
},
];

function computeScore(role) {
const reqTotal = role.required.reduce((a, r) => a + r.weight, 0);
const prefTotal = role.preferred.reduce((a, p) => a + p.weight, 0);
let reqWeighted = 0;
role.required.forEach((r, i) => { reqWeighted += (role.candidateScores.required[i].score / 100) * r.weight; });
let prefWeighted = 0;
role.preferred.forEach((p, i) => { prefWeighted += (role.candidateScores.preferred[i].score / 100) * p.weight; });
const reqPct = (reqWeighted / reqTotal) * 100;
const prefPct = (prefWeighted / prefTotal) * 100;
const final = reqPct * 0.65 + prefPct * 0.35;
return { reqPct: Math.round(reqPct), prefPct: Math.round(prefPct), final: Math.round(final) };
}

function getVerdict(score) {
if (score >= 88) return { label: "Top Match", color: "#22d3a5", bg: "rgba(34,211,165,0.13)", rank: 1 };
if (score >= 80) return { label: "Strong Match", color: "#60a5fa", bg: "rgba(96,165,250,0.13)", rank: 2 };
if (score >= 70) return { label: "Good Match", color: "#fbbf24", bg: "rgba(251,191,36,0.13)", rank: 3 };
return { label: "Stretch", color: "#f87171", bg: "rgba(248,113,113,0.13)", rank: 4 };
}

function ScoreBar({ value, color, thin }) {
return (
<div style={{ background: "#1a1a2e", borderRadius: 4, height: thin ? 5 : 8, width: "100%", overflow: "hidden" }}>
<div style={{ height: "100%", width: `${value}%`, background: color, borderRadius: 4, transition: "width 0.9s cubic-bezier(.4,0,.2,1)" }} />
</div>
);
}

function CategoryPill({ cat, active, onClick }) {
return (
<button onClick={onClick} style={{
background: active ? "rgba(96,165,250,0.18)" : "rgba(255,255,255,0.04)",
border: active ? "1px solid rgba(96,165,250,0.5)" : "1px solid rgba(255,255,255,0.08)",
color: active ? "#93c5fd" : "#666",
borderRadius: 20,
padding: "5px 14px",
fontSize: 11,
fontFamily: "'DM Mono', monospace",
cursor: "pointer",
letterSpacing: 0.3,
transition: "all 0.15s",
whiteSpace: "nowrap",
}}>{cat}</button>
);
}

function RoleCard({ role, isSelected, onSelect }) {
const scores = computeScore(role);
const verdict = getVerdict(scores.final);
return (
<div onClick={onSelect} style={{
cursor: "pointer",
background: isSelected ? "rgba(255,255,255,0.07)" : "rgba(255,255,255,0.025)",
border: isSelected ? `1.5px solid ${verdict.color}55` : "1.5px solid rgba(255,255,255,0.06)",
borderLeft: `3px solid ${verdict.color}`,
borderRadius: 10,
padding: "14px 16px",
marginBottom: 8,
transition: "all 0.15s",
}}>
<div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
<div style={{ flex: 1, minWidth: 0 }}>
<div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 4 }}>
<span style={{ fontFamily: "'DM Mono', monospace", fontSize: 10, color: "#555", letterSpacing: 0.5 }}>{role.level}</span>
<span style={{ fontSize: 10, color: "#444" }}>·</span>
<span style={{ fontFamily: "'DM Mono', monospace", fontSize: 10, color: verdict.color, opacity: 0.8 }}>{role.category}</span>
{role.remote && <span style={{ fontSize: 9, background: "rgba(34,211,165,0.1)", color: "#22d3a5", border: "1px solid rgba(34,211,165,0.25)", borderRadius: 10, padding: "1px 7px", letterSpacing: 0.3 }}>REMOTE ELIGIBLE</span>}
</div>
<div style={{ fontFamily: "'Syne', sans-serif", fontWeight: 700, fontSize: 13, color: "#e0e0e0", lineHeight: 1.3, marginBottom: 2 }}>{role.title}</div>
<div style={{ fontSize: 11, color: "#555" }}>{role.locations[0]}{role.locations.length > 1 ? ` +${role.locations.length - 1}` : ""}</div>
</div>
<div style={{ textAlign: "right", flexShrink: 0 }}>
<div style={{ fontFamily: "'Syne', sans-serif", fontSize: 26, fontWeight: 800, color: verdict.color, lineHeight: 1 }}>{scores.final}</div>
<div style={{ fontSize: 9, color: "#444", fontFamily: "'DM Mono', monospace" }}>/100</div>
<div style={{ fontSize: 9, background: verdict.bg, color: verdict.color, border: `1px solid ${verdict.color}30`, borderRadius: 10, padding: "2px 7px", marginTop: 4, fontFamily: "'DM Mono', monospace", letterSpacing: 0.3 }}>{verdict.label}</div>
</div>
</div>
<div style={{ marginTop: 8 }}>
<ScoreBar value={scores.final} color={verdict.color} />
</div>
<div style={{ display: "flex", gap: 12, marginTop: 6 }}>
<span style={{ fontSize: 10, color: "#444", fontFamily: "'DM Mono', monospace" }}>REQ <span style={{ color: "#777" }}>{scores.reqPct}</span></span>
<span style={{ fontSize: 10, color: "#444", fontFamily: "'DM Mono', monospace" }}>PREF <span style={{ color: "#777" }}>{scores.prefPct}</span></span>
<span style={{ fontSize: 10, color: "#444", fontFamily: "'DM Mono', monospace" }}>{role.salary}</span>
</div>
</div>
);
}

function DetailPanel({ role }) {
const scores = computeScore(role);
const verdict = getVerdict(scores.final);
const allItems = [
...role.required.map((r, i) => ({ ...r, score: role.candidateScores.required[i].score, note: role.candidateScores.required[i].note, type: "REQ" })),
...role.preferred.map((p, i) => ({ ...p, score: role.candidateScores.preferred[i].score, note: role.candidateScores.preferred[i].note, type: "PREF" })),
];
const gaps = allItems.filter(x => x.score < 72).sort((a, b) => a.score - b.score);
const strengths = allItems.filter(x => x.score >= 88).sort((a, b) => b.score - a.score);

return (
<div style={{ fontFamily: "'DM Sans', sans-serif" }}>
{/* Header */}
<div style={{ marginBottom: 20 }}>
<div style={{ display: "flex", gap: 8, marginBottom: 6, flexWrap: "wrap" }}>
<span style={{ fontSize: 10, fontFamily: "'DM Mono', monospace", color: "#555" }}>{role.level}</span>
<span style={{ color: "#333" }}>·</span>
<span style={{ fontSize: 10, fontFamily: "'DM Mono', monospace", color: verdict.color }}>{role.category}</span>
{role.remote && <span style={{ fontSize: 9, background: "rgba(34,211,165,0.1)", color: "#22d3a5", border: "1px solid rgba(34,211,165,0.25)", borderRadius: 10, padding: "1px 7px" }}>REMOTE ELIGIBLE</span>}
</div>
<div style={{ fontFamily: "'Syne', sans-serif", fontWeight: 800, fontSize: 18, color: "#f0f0f0", lineHeight: 1.2, marginBottom: 4 }}>{role.title}</div>
<div style={{ fontSize: 12, color: "#555" }}>{role.team}</div>
<div style={{ fontSize: 11, color: "#444", marginTop: 2 }}>{role.locations.join(" · ")} · {role.salary}</div>
</div>

  {/* Score ring section */}
  <div style={{ display: "flex", gap: 10, marginBottom: 18 }}>
    <div style={{ flex: 1, background: verdict.bg, border: `1px solid ${verdict.color}30`, borderRadius: 12, padding: "14px 16px", textAlign: "center" }}>
      <div style={{ fontFamily: "'Syne', sans-serif", fontSize: 42, fontWeight: 800, color: verdict.color, lineHeight: 1 }}>{scores.final}</div>
      <div style={{ fontSize: 10, color: "#555", fontFamily: "'DM Mono', monospace", marginTop: 2 }}>ATS SCORE</div>
      <div style={{ fontSize: 11, color: verdict.color, marginTop: 4, fontWeight: 600 }}>{verdict.label}</div>
    </div>
    <div style={{ flex: 2, display: "flex", flexDirection: "column", gap: 8 }}>
      {[
        { label: "Required Criteria (65%)", value: scores.reqPct, color: "#60a5fa" },
        { label: "Preferred Criteria (35%)", value: scores.prefPct, color: "#a78bfa" },
      ].map(item => (
        <div key={item.label} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 8, padding: "10px 12px", border: "1px solid rgba(255,255,255,0.05)", flex: 1 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
            <span style={{ fontSize: 10, color: "#555", fontFamily: "'DM Mono', monospace" }}>{item.label}</span>
            <span style={{ fontFamily: "'Syne', sans-serif", fontWeight: 700, fontSize: 16, color: item.color }}>{item.value}</span>
          </div>
          <ScoreBar value={item.value} color={item.color} thin />
        </div>
      ))}
    </div>
  </div>

  {/* Why This Fits */}
  <div style={{ background: "rgba(96,165,250,0.06)", border: "1px solid rgba(96,165,250,0.2)", borderRadius: 10, padding: "12px 14px", marginBottom: 16 }}>
    <div style={{ fontSize: 10, color: "#60a5fa", fontFamily: "'DM Mono', monospace", letterSpacing: 0.5, marginBottom: 6, textTransform: "uppercase" }}>Why This Fits You</div>
    <div style={{ fontSize: 12, color: "#aaa", lineHeight: 1.6 }}>{role.whyFit}</div>
  </div>

  {/* Criteria detail */}
  <div style={{ marginBottom: 14 }}>
    <div style={{ fontSize: 10, color: "#555", fontFamily: "'DM Mono', monospace", letterSpacing: 1, textTransform: "uppercase", marginBottom: 10 }}>Required</div>
    {role.required.map((r, i) => {
      const s = role.candidateScores.required[i];
      const c = s.score >= 88 ? "#22d3a5" : s.score >= 70 ? "#fbbf24" : "#f87171";
      return (
        <div key={i} style={{ background: "rgba(255,255,255,0.03)", borderRadius: 8, padding: "10px 12px", marginBottom: 8, border: `1px solid ${c}18` }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
            <span style={{ fontSize: 12, color: "#ccc", flex: 1, paddingRight: 10 }}>{r.skill}</span>
            <span style={{ fontFamily: "'DM Mono', monospace", fontSize: 13, fontWeight: 700, color: c, flexShrink: 0 }}>{s.score}%</span>
          </div>
          <ScoreBar value={s.score} color={c} thin />
          <div style={{ fontSize: 10, color: "#555", marginTop: 5, lineHeight: 1.4 }}>{s.note}</div>
        </div>
      );
    })}
  </div>

  <div style={{ marginBottom: 16 }}>
    <div style={{ fontSize: 10, color: "#555", fontFamily: "'DM Mono', monospace", letterSpacing: 1, textTransform: "uppercase", marginBottom: 10 }}>Preferred</div>
    {role.preferred.map((p, i) => {
      const s = role.candidateScores.preferred[i];
      const c = s.score >= 88 ? "#22d3a5" : s.score >= 70 ? "#fbbf24" : "#f87171";
      return (
        <div key={i} style={{ background: "rgba(255,255,255,0.03)", borderRadius: 8, padding: "10px 12px", marginBottom: 8, border: `1px solid ${c}18` }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
            <span style={{ fontSize: 12, color: "#ccc", flex: 1, paddingRight: 10 }}>{p.skill}</span>
            <span style={{ fontFamily: "'DM Mono', monospace", fontSize: 13, fontWeight: 700, color: c, flexShrink: 0 }}>{s.score}%</span>
          </div>
          <ScoreBar value={s.score} color={c} thin />
          <div style={{ fontSize: 10, color: "#555", marginTop: 5, lineHeight: 1.4 }}>{s.note}</div>
        </div>
      );
    })}
  </div>

  {/* Gaps / Strengths */}
  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 14 }}>
    {gaps.length > 0 && (
      <div style={{ background: "rgba(248,113,113,0.06)", border: "1px solid rgba(248,113,113,0.18)", borderRadius: 8, padding: 12 }}>
        <div style={{ fontSize: 10, color: "#f87171", fontFamily: "'DM Mono', monospace", marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 }}>⚠ Gaps</div>
        {gaps.map((g, i) => (
          <div key={i} style={{ fontSize: 11, color: "#999", marginBottom: 6, paddingLeft: 8, borderLeft: "2px solid rgba(248,113,113,0.35)" }}>
            <div style={{ fontSize: 9, color: "#f87171", fontFamily: "'DM Mono', monospace" }}>{g.type} · {g.score}%</div>
            <div style={{ lineHeight: 1.3 }}>{g.skill}</div>
          </div>
        ))}
      </div>
    )}
    {strengths.length > 0 && (
      <div style={{ background: "rgba(34,211,165,0.06)", border: "1px solid rgba(34,211,165,0.18)", borderRadius: 8, padding: 12 }}>
        <div style={{ fontSize: 10, color: "#22d3a5", fontFamily: "'DM Mono', monospace", marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 }}>✓ Strengths</div>
        {strengths.slice(0, 4).map((s, i) => (
          <div key={i} style={{ fontSize: 11, color: "#999", marginBottom: 6, paddingLeft: 8, borderLeft: "2px solid rgba(34,211,165,0.35)" }}>
            <div style={{ fontSize: 9, color: "#22d3a5", fontFamily: "'DM Mono', monospace" }}>{s.type} · {s.score}%</div>
            <div style={{ lineHeight: 1.3 }}>{s.skill}</div>
          </div>
        ))}
      </div>
    )}
  </div>

  <a href={role.url} target="_blank" rel="noopener noreferrer" style={{
    display: "block", textAlign: "center", background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "#888", borderRadius: 8, padding: "9px", fontSize: 11, textDecoration: "none", fontFamily: "'DM Mono', monospace",
  }}>→ View on Google Careers</a>
</div>
);
}

export default function App() {
const [selected, setSelected] = useState(0);
const [activeCategory, setActiveCategory] = useState("All");

const sorted = [...roles]
.map((r, originalIdx) => ({ role: r, score: computeScore(r).final, originalIdx }))
.sort((a, b) => b.score - a.score);

const filtered = activeCategory === "All" ? sorted : sorted.filter(({ role }) => role.category === activeCategory);
const selectedRole = roles[selected];

return (
<div style={{ minHeight: "100vh", background: "#0c0c1a", color: "#f0f0f0", fontFamily: "'DM Sans', sans-serif" }}>
<style>{`@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@400;500;600&display=swap'); * { box-sizing: border-box; margin: 0; padding: 0; } ::-webkit-scrollbar { width: 4px; } ::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 4px; }`}</style>

  {/* Header */}
  <div style={{ padding: "22px 24px 16px", borderBottom: "1px solid rgba(255,255,255,0.05)", background: "linear-gradient(135deg,rgba(34,211,165,0.05),rgba(96,165,250,0.05))" }}>
    <div style={{ fontFamily: "'DM Mono', monospace", fontSize: 10, color: "#444", letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 4 }}>ATS Match Analysis · Google Careers · All US Locations</div>
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 8 }}>
      <div>
        <div style={{ fontFamily: "'Syne', sans-serif", fontWeight: 800, fontSize: 20, color: "#f0f0f0" }}>Andrew L. Stewart, Jr.</div>
        <div style={{ fontSize: 12, color: "#555" }}>Senior Systems Software Engineer · NVIDIA / TCWGlobal</div>
      </div>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {[{ v: "7 roles", s: "analyzed" }, { v: "L4–L6", s: "levels" }, { v: "Required 65%", s: "· Preferred 35%" }].map(tag => (
          <div key={tag.v} style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 6, padding: "4px 10px", fontSize: 10, color: "#666", fontFamily: "'DM Mono', monospace" }}>
            <span style={{ color: "#888" }}>{tag.v}</span> {tag.s}
          </div>
        ))}
      </div>
    </div>
    {/* Category filter */}
    <div style={{ display: "flex", gap: 6, marginTop: 14, flexWrap: "wrap" }}>
      {CATEGORIES.map(c => <CategoryPill key={c} cat={c} active={activeCategory === c} onClick={() => setActiveCategory(c)} />)}
    </div>
  </div>

  <div style={{ display: "grid", gridTemplateColumns: "1fr 1.1fr", height: "calc(100vh - 148px)", minHeight: 560 }}>
    {/* Left list */}
    <div style={{ overflowY: "auto", padding: "16px 16px 16px 20px", borderRight: "1px solid rgba(255,255,255,0.04)" }}>
      {filtered.length === 0 ? (
        <div style={{ color: "#444", fontSize: 13, marginTop: 40, textAlign: "center" }}>No roles in this category</div>
      ) : (
        filtered.map(({ role, originalIdx }, i) => (
          <RoleCard key={role.id} role={role} isSelected={selected === originalIdx} onSelect={() => setSelected(originalIdx)} />
        ))
      )}

      {/* Quick summary */}
      <div style={{ marginTop: 10, background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)", borderRadius: 10, padding: "12px 14px" }}>
        <div style={{ fontSize: 10, color: "#444", fontFamily: "'DM Mono', monospace", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8 }}>Resume Gap to Fix for Google</div>
        <div style={{ fontSize: 11, color: "#444", lineHeight: 1.6 }}>
          Adding <span style={{ color: "#fbbf24" }}>Java</span> to your skills (even as "familiar with") unlocks the Workspace Cloud Infra and other Workspace roles that weight Java heavily. Everything else on your resume is well-represented. Consider explicitly naming <span style={{ color: "#fbbf24" }}>Bazel</span> in the NVIDIA bullet points — it's mentioned in skills but not in bullets where ATS parsers scan for it.
        </div>
      </div>
    </div>

    {/* Right detail */}
    <div style={{ overflowY: "auto", padding: "16px 20px 16px 16px" }}>
      <DetailPanel role={selectedRole} />
    </div>
  </div>
</div>
);
}
