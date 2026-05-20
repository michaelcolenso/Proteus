// ============================================================================
// COVER LETTER — Mercer Builders
// Project Manager – High-End Custom Residential
// Bellevue / Medina / Clyde Hill / Kirkland, WA
// ----------------------------------------------------------------------------
// Compile with:   typst compile letters/mercer_builders.typ
//            or:  copy to letter.typ and run ./generate.sh letter
// ============================================================================

#import "../modules_en/portfolio/theme.typ": *

#let metadata = toml("../metadata.toml")

// ---- Recipient + subject (edit per application) -----------------------------
#let recipient-name    = "Mercer Builders"
#let recipient-address = "Bellevue, Washington"
#let letter-subject    = "Project Manager – High-End Custom Residential"
#let letter-date       = datetime.today().display("[month repr:long] [day], [year]")

// ---- Document metadata ------------------------------------------------------
#set document(
  title: "Michael Colenso — Cover Letter",
  author: "Michael Colenso",
)

// ---- Page setup -------------------------------------------------------------
#set page(
  paper: "us-letter",
  margin: (x: 1.0in, top: 0.85in, bottom: 0.95in),
  fill: cream,
  footer: [
    #set text(
      font: heading-font,
      size: 7.5pt,
      tracking: 2.2pt,
      weight: "medium",
      fill: slate,
    )
    #grid(
      columns: (1fr, auto, 1fr),
      column-gutter: 14pt,
      align: (left + horizon, center + horizon, right + horizon),
      upper("Michael Colenso"),
      line(length: 28pt, stroke: 0.5pt + gold),
      upper("Cover Letter · Seattle, WA"),
    )
  ],
  footer-descent: 26pt,
)

// ---- Type ------------------------------------------------------------------
#set text(
  font: body-font,
  size: 10.5pt,
  fill: charcoal,
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.72em,
  spacing: 1.05em,
  first-line-indent: 0pt,
)

#show link: set text(fill: gold-dark)

// ============================================================================
// 1. LETTERHEAD
// ============================================================================
#grid(
  columns: (1fr, auto),
  column-gutter: 18pt,
  align: (left + bottom, right + bottom),
  [
    #text(
      font: display-font,
      size: 28pt,
      weight: "light",
      fill: navy,
    )[Michael Colenso]
    #v(-2pt)
    #text(
      font: heading-font,
      size: 8.5pt,
      tracking: 2.8pt,
      weight: "medium",
      fill: gold-dark,
    )[#upper("Construction Project Manager")]
  ],
  [
    #set text(size: 8.8pt, fill: slate)
    #set par(leading: 0.85em, justify: false)
    #align(right)[
      #metadata.personal.info.phone \
      #link("mailto:" + metadata.personal.info.email)[#metadata.personal.info.email] \
      Seattle, Washington
    ]
  ],
)

#v(10pt)
#line(length: 100%, stroke: 0.6pt + gold)

// ============================================================================
// 2. DATE · RECIPIENT · SUBJECT
// ============================================================================
#v(30pt)

#text(
  font: heading-font,
  size: 8.5pt,
  tracking: 1.8pt,
  weight: "medium",
  fill: gold-dark,
)[#upper(letter-date)]

#v(18pt)

#block(spacing: 0pt)[
  #text(
    font: heading-font,
    size: 11pt,
    weight: "medium",
    fill: navy,
  )[#recipient-name] \
  #text(size: 10pt, fill: slate)[#recipient-address]
]

#v(18pt)

#block(spacing: 0pt)[
  #text(
    font: heading-font,
    size: 8pt,
    tracking: 1.6pt,
    weight: "medium",
    fill: gold-dark,
  )[#upper("Re")]
  #h(8pt)
  #text(
    font: heading-font,
    size: 10.5pt,
    weight: "medium",
    fill: navy,
  )[#letter-subject]
]

#v(22pt)
#line(length: 36pt, stroke: 1pt + gold)
#v(18pt)

// ============================================================================
// 3. BODY
// ============================================================================
Dear Hiring Manager,

Mercer Builders has a strong reputation for delivering homes on the Eastside that set the standard for craftsmanship and client experience. That reputation is exactly what drew me to this opportunity. I'm a Seattle-based Project Manager with 20+ years in construction and a track record built specifically around high-end, detail-intensive residential work — the kind where clients are engaged, architects have vision, and the margin for error is zero.

At Toth Construction, I managed \$8M+ in luxury residential projects, coordinating directly with world-class architects and specialty artisans to execute environments that met exacting design intent and ownership standards. My role extended well beyond scheduling — I owned preconstruction estimating, ROM development, and value engineering conversations with owners from the earliest planning stages. That work in Medina, Clyde Hill, and the broader Eastside gave me fluency with the permit offices, subcontractor expectations, and client dynamics specific to these markets.

Prior to Toth, I spent a year at Discovery Land Company delivering ultra-luxury residential homes in an exclusive international resort community, where the client relationships and quality benchmarks were among the most demanding I've encountered. Building trust with owners who have exceedingly high standards — and keeping projects moving efficiently beneath that — is a discipline I carry into every project.

My estimating background includes detailed takeoffs, ROM budgeting through schematic and design development phases, and value engineering that preserves design intent while protecting the owner's budget. At SODO Builders I captured over \$400K in facade savings through a proactive VE process without compromising the architect's vision. That same approach scales down naturally to the custom residential context, where every line item is visible to the owner.

What I'd bring to Mercer Builders:

- *Preconstruction leadership* — ROM estimates, detailed budgets, and VE facilitation from early design through construction document phases
- *Eastside market knowledge* — established relationships with specialty subcontractors, familiarity with Bellevue, Medina, Clyde Hill, and Kirkland permitting processes
- *Owner-facing communication* — consistent track record of earning trusted-advisor status with high-net-worth clients through transparency, responsiveness, and follow-through
- *Multi-project management* — experience carrying multiple projects simultaneously without losing focus on quality, schedule, or budget at any site

I'd welcome the opportunity to learn more about your current project pipeline and discuss how I can contribute. Thank you for your time and consideration.

// ============================================================================
// 4. SIGN-OFF
// ============================================================================
#v(14pt)

With regards,

#v(2pt)

#image("../src/signature.png", height: 46pt)

#v(-6pt)

#text(
  font: display-font,
  size: 13pt,
  weight: "medium",
  fill: navy,
)[Michael Colenso]

#v(1pt)

#text(
  font: heading-font,
  size: 8pt,
  tracking: 1.8pt,
  weight: "medium",
  fill: gold-dark,
)[#upper("Construction Project Manager")]
