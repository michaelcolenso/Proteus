// ============================================================================
// BY THE NUMBERS — Metrics dashboard sourced from the achievement database.
// ============================================================================

#import "theme.typ": *
#import "components.typ": eyebrow, section-title, metric-card

#eyebrow("By the numbers")
#section-title(
  [A practice measured \
  in outcomes.],
  subtitle: [Figures drawn from the projects featured in this portfolio.],
)

#v(6pt)

// ---- First row: headline figures -------------------------------------------
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 14pt,
  row-gutter: 14pt,

  metric-card(
    "$300M+",
    "Delivered project value",
    caption: [Across residential, mixed-use, and historic renovation.],
  ),
  metric-card(
    "18 yrs",
    "Construction leadership",
    caption: [From field engineer to senior project manager.],
  ),
  metric-card(
    "Zero",
    "Recordable incidents",
    caption: [Across 24-month \$12M podium build at 2210 Eastlake.],
  ),
)

#v(14pt)

// ---- Second row: luxury-specific wins --------------------------------------
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 14pt,
  row-gutter: 14pt,

  metric-card(
    "$15M+",
    "Luxury residential",
    caption: [UHNW projects in Seattle and the Bahamas, 2017–2022.],
  ),
  metric-card(
    "2 mo",
    "Early delivery",
    caption: [\$40M Hyatt Place turnaround via Last Planner System.],
  ),
  metric-card(
    "15%",
    "Faster schedule",
    caption: [Barton Senior Residences — lean pull-planning.],
  ),
)

#v(14pt)

// ---- Third row: trust & change-management signals --------------------------
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 14pt,
  row-gutter: 14pt,

  metric-card(
    "$6M+",
    "Negotiated changes",
    caption: [The Alaska Building — relationship preserved throughout.],
  ),
  metric-card(
    "3 + 2",
    "Referrals & repeats",
    caption: [From ultra-high-net-worth clients at Toth Construction.],
  ),
  metric-card(
    "2",
    "National awards",
    caption: [Eagle Award and Northwest Construction — historic.],
  ),
)

#pagebreak()
