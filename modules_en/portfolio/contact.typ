// ============================================================================
// CONTACT — Closing page with contact details and a parting statement.
// ============================================================================

#import "theme.typ": *
#import "components.typ": eyebrow

// Full-bleed navy closing, mirroring the cover.
#page(
  margin: 0in,
  fill: navy,
)[
  #set text(fill: cream)

  // Top bar
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
    )[#upper("Let us build something enduring")]
  ]

  #v(1fr)

  #align(center)[
    #text(
      font: heading-font,
      size: 9pt,
      tracking: 4.5pt,
      fill: gold,
      weight: "medium",
    )[#upper("In Closing")]

    #v(16pt)

    #text(
      font: display-font,
      size: 34pt,
      weight: "thin",
      fill: cream,
    )[Thank you for \ your consideration.]

    #v(12pt)

    #line(length: 100pt, stroke: 0.8pt + gold)

    #v(16pt)

    #block(
      width: 70%,
      text(
        font: body-font,
        size: 11pt,
        style: "italic",
        fill: rgb("#E8DFCC"),
      )[
        I would welcome a conversation about your project — whether
        it is a custom residence, a historic restoration, or a
        boutique multifamily development. Every meaningful build
        begins with a candid, unhurried first conversation.
      ]
    )
  ]

  #v(1fr)

  // Contact block
  #align(center)[
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
    )[#upper("Construction Project Manager")]

    #v(14pt)

    #line(length: 60pt, stroke: 0.5pt + gold)

    #v(14pt)

    #set text(font: body-font, size: 10.5pt, fill: cream)
    #grid(
      columns: (auto, auto, auto),
      column-gutter: 22pt,
      [
        #text(
          font: heading-font,
          size: 7.5pt,
          tracking: 1.6pt,
          fill: gold,
        )[#upper("Phone")]
        #linebreak()
        206.607.7836
      ],
      [
        #text(
          font: heading-font,
          size: 7.5pt,
          tracking: 1.6pt,
          fill: gold,
        )[#upper("Email")]
        #linebreak()
        #link("mailto:michaelcolenso@gmail.com")[#text(fill: cream)[michaelcolenso\@gmail.com]]
      ],
      [
        #text(
          font: heading-font,
          size: 7.5pt,
          tracking: 1.6pt,
          fill: gold,
        )[#upper("Based in")]
        #linebreak()
        Seattle, WA
      ],
    )

    #v(0.9in)
  ]
]
