// ============================================================================
// CAPABILITIES — Service pillars for luxury residential engagements.
// ============================================================================

#import "theme.typ": *
#import "components.typ": eyebrow, section-title, capability

#eyebrow("Capabilities")
#section-title(
  [How I serve \
  discerning clients.],
  subtitle: [A focused set of capabilities refined across eighteen years of residential work.],
)

#v(4pt)

#grid(
  columns: (1fr, 1fr),
  column-gutter: 18pt,
  row-gutter: 12pt,

  capability(
    "Preconstruction & Planning",
    [Detailed constructability review, realistic cost modeling, and value engineering that respects design intent rather than erasing it.],
  ),
  capability(
    "Design-Team Collaboration",
    [Direct, respectful partnership with architects and interior designers — protecting the design vision through honest, early conversation.],
  ),
  capability(
    "Owner Representation",
    [Trusted-advisor reporting cadence, transparent budget tracking, and the discretion that private-client work demands.],
  ),
  capability(
    "Change Management",
    [A disciplined, documented approach to change — fair, fast, and built to preserve the owner relationship under pressure.],
  ),
  capability(
    "Specialty Trade Coordination",
    [Long-standing relationships with stone, millwork, metalwork, lighting, and integrated-systems specialists across the Pacific Northwest.],
  ),
  capability(
    "Historic & Adaptive Reuse",
    [SHPO-level fluency in preservation requirements, seismic retrofit, and the balance between heritage and modern comfort.],
  ),
  capability(
    "Schedule Discipline",
    [Last Planner System, pull planning, and the kind of week-by-week rigor that delivered a \$40M project two months early.],
  ),
  capability(
    "Quality & Punch",
    [Finish-level QC programs, mock-up driven approvals, and a zero-tolerance approach to the last 2% that defines a luxury home.],
  ),
)

#v(20pt)

// ---- Trade & specialty expertise block -------------------------------------
#block(
  width: 100%,
  inset: 16pt,
  fill: cream-deep,
  stroke: (left: 2pt + gold),
  radius: 2pt,
  breakable: false,
)[
  #text(
    font: heading-font,
    size: 9pt,
    tracking: 1.6pt,
    fill: gold-dark,
    weight: "medium",
  )[#upper("Specialty Trades & Systems")]
  #v(8pt)

  #grid(
    columns: (1fr, 1fr, 1fr),
    column-gutter: 16pt,
    row-gutter: 6pt,
    [*Envelope* \ Curtain wall · Stone veneer · IMPs],
    [*Interiors* \ Custom millwork · Natural stone · Plaster],
    [*Systems* \ Radiant heat · Smart home · AV integration],
    [*Structure* \ Seismic retrofit · Post-tension · Wood frame],
    [*Sitework* \ Shoring · Urban logistics · Landscape],
    [*Finishes* \ Mock-ups · Lighting · Specialty metals],
  )
]

#pagebreak()
