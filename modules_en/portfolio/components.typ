// ============================================================================
// COMPONENTS — Reusable visual building blocks for the luxury portfolio.
// ============================================================================

#import "theme.typ": *

// ---- Small caps label -------------------------------------------------------
// Used above section titles for an editorial feel.
#let eyebrow(text-content) = {
  set text(
    font: heading-font,
    size: 8.5pt,
    tracking: 2.8pt,
    weight: "medium",
    fill: gold-dark,
  )
  upper(text-content)
}

// ---- Section title ----------------------------------------------------------
#let section-title(title, subtitle: none) = {
  v(6pt)
  text(
    font: display-font,
    size: 26pt,
    weight: "light",
    fill: navy,
  )[#title]
  if subtitle != none {
    v(2pt)
    text(
      font: body-font,
      size: 11pt,
      fill: slate,
      style: "italic",
    )[#subtitle]
  }
  v(4pt)
  line(length: 60pt, stroke: rule-thick + gold)
  v(10pt)
}

// ---- Horizontal rule --------------------------------------------------------
#let divider(color: hairline, weight: rule-thin) = {
  v(6pt)
  line(length: 100%, stroke: weight + color)
  v(6pt)
}

// ---- Metric card (for by-the-numbers grid) ----------------------------------
#let metric-card(value, label, caption: none) = {
  block(
    width: 100%,
    inset: 14pt,
    radius: 2pt,
    fill: cream-deep,
    stroke: (bottom: 1.5pt + gold),
  )[
    #set align(left)
    #text(
      font: display-font,
      size: 24pt,
      weight: "light",
      fill: navy,
    )[#value]
    #v(-4pt)
    #text(
      font: heading-font,
      size: 8.5pt,
      tracking: 1.8pt,
      fill: gold-dark,
      weight: "medium",
    )[#upper(label)]
    #if caption != none {
      v(2pt)
      text(size: 9pt, fill: slate)[#caption]
    }
  ]
}

// ---- Project case-study block ----------------------------------------------
#let project-case(
  title: "",
  location: "",
  value: "",
  year: "",
  role: "",
  scope: none,
  challenge: none,
  approach: none,
  outcome: none,
  tags: (),
  photo: none,
  photo-height: 150pt,
) = {
  block(
    width: 100%,
    inset: 0pt,
    radius: 2pt,
    fill: white,
    stroke: (
      left: 2pt + gold,
      rest: 0.4pt + hairline,
    ),
    clip: true,
    breakable: true,
  )[
    // Optional photo strip — full-width, cropped to fixed height
    #if photo != none {
      image(photo, width: 100%, height: photo-height, fit: "cover")
    }

    #pad(x: 18pt, top: 16pt, bottom: 16pt)[
      // Header row: title + metadata
      #grid(
        columns: (1fr, auto),
        column-gutter: 12pt,
        align: (left, right),
        [
          #text(
            font: display-font,
            size: 15pt,
            weight: "medium",
            fill: navy,
          )[#title]
          #linebreak()
          #text(size: 9.5pt, fill: slate, style: "italic")[#location · #year]
        ],
        [
          #text(
            font: display-font,
            size: 16pt,
            weight: "light",
            fill: gold-dark,
          )[#value]
          #linebreak()
          #text(size: 8pt, fill: slate, tracking: 1.2pt)[#upper(role)]
        ],
      )

      #v(8pt)
      #line(length: 100%, stroke: 0.3pt + hairline)
      #v(6pt)

      // Scope line
      #if scope != none [
        #text(font: heading-font, size: 8pt, tracking: 1.4pt, fill: gold-dark, weight: "medium")[#upper("Scope")] #h(4pt)
        #text(size: 10pt, fill: charcoal)[#scope]
        #v(5pt)
      ]

      // Case-study three-beat narrative
      #if challenge != none [
        #text(font: heading-font, size: 8pt, tracking: 1.4pt, fill: gold-dark, weight: "medium")[#upper("Challenge")] #h(4pt)
        #text(size: 10pt, fill: charcoal)[#challenge]
        #v(5pt)
      ]
      #if approach != none [
        #text(font: heading-font, size: 8pt, tracking: 1.4pt, fill: gold-dark, weight: "medium")[#upper("Approach")] #h(4pt)
        #text(size: 10pt, fill: charcoal)[#approach]
        #v(5pt)
      ]
      #if outcome != none [
        #text(font: heading-font, size: 8pt, tracking: 1.4pt, fill: gold-dark, weight: "medium")[#upper("Outcome")] #h(4pt)
        #text(size: 10pt, fill: charcoal)[#outcome]
      ]

      // Tag row
      #if tags.len() > 0 {
        v(8pt)
        line(length: 100%, stroke: 0.3pt + hairline)
        v(5pt)
        set text(size: 8pt, fill: slate, font: heading-font, tracking: 0.8pt)
        tags.map(upper).join("  ·  ")
      }
    ]
  ]
  v(10pt)
}

// ---- Pull quote -------------------------------------------------------------
#let pull-quote(body, attribution: none) = {
  block(
    width: 100%,
    inset: (x: 22pt, y: 14pt),
    stroke: (left: 2pt + gold),
  )[
    #set text(
      font: display-font,
      size: 13pt,
      style: "italic",
      fill: navy-soft,
      weight: "light",
    )
    #body
    #if attribution != none {
      v(4pt)
      text(
        font: heading-font,
        size: 8.5pt,
        tracking: 1.4pt,
        style: "normal",
        fill: gold-dark,
      )[— #upper(attribution)]
    }
  ]
}

// ---- Capability pillar ------------------------------------------------------
#let capability(title, description) = {
  block(
    width: 100%,
    inset: (x: 12pt, y: 10pt),
    spacing: 6pt,
  )[
    #text(
      font: heading-font,
      size: 10pt,
      weight: "semibold",
      fill: navy,
      tracking: 0.8pt,
    )[#upper(title)]
    #v(3pt)
    #line(length: 24pt, stroke: 1pt + gold)
    #v(4pt)
    #text(size: 9.5pt, fill: charcoal)[#description]
  ]
}
