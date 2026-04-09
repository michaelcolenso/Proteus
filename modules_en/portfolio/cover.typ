// ============================================================================
// COVER PAGE — Luxury Residential Portfolio
// ============================================================================

#import "theme.typ": *
#import "components.typ": eyebrow

// Full-bleed navy cover with gold accents.
#page(
  margin: 0in,
  fill: navy,
)[
  #set text(fill: cream)

  // Top ornamental bar
  #place(top + left, dx: 0.9in, dy: 0.9in)[
    #line(length: 80pt, stroke: 1.5pt + gold)
  ]
  #place(top + right, dx: -0.9in, dy: 0.9in)[
    #text(
      font: heading-font,
      size: 8.5pt,
      tracking: 3pt,
      fill: gold,
      weight: "medium",
    )[#upper("Portfolio · MMXXV")]
  ]

  // Centered title block
  #v(1fr)
  #align(center)[
    #text(
      font: heading-font,
      size: 9pt,
      tracking: 4.5pt,
      fill: gold,
      weight: "medium",
    )[#upper("Luxury Residential")]

    #v(18pt)

    #text(
      font: display-font,
      size: 52pt,
      weight: "thin",
      fill: cream,
    )[Portfolio]

    #v(10pt)

    #line(length: 120pt, stroke: 0.8pt + gold)

    #v(18pt)

    #text(
      font: body-font,
      size: 12pt,
      style: "italic",
      fill: rgb("#E8DFCC"),
    )[
      Selected works in high-end residential, \
      historic renovation, and custom construction.
    ]
  ]
  #v(1fr)

  // Bottom identity block
  #align(center)[
    #line(length: 40pt, stroke: 0.5pt + gold)
    #v(12pt)
    #text(
      font: display-font,
      size: 18pt,
      weight: "light",
      fill: cream,
    )[Michael Colenso]
    #v(4pt)
    #text(
      font: heading-font,
      size: 8.5pt,
      tracking: 2.5pt,
      fill: gold,
      weight: "medium",
    )[#upper("Construction Project Manager  ·  Seattle, WA")]
    #v(0.9in)
  ]
]
