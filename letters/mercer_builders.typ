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
  fill: white,
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
      upper("Seattle, WA"),
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

I'm a Seattle-based Project Manager with 20+ years in construction and a track record built around high-end, detail-intensive residential work. At Toth Construction I managed \$8M+ in luxury residential projects on the Eastside — coordinating directly with world-class architects and artisans, owning preconstruction estimating and ROM development, and managing value engineering conversations with owners from early design through delivery. That work gave me fluency with the permit offices, subcontractor relationships, and client expectations specific to Medina, Clyde Hill, Bellevue, and Kirkland.

Prior to Toth I spent a year at Discovery Land Company delivering ultra-luxury resort homes for among the most demanding clientele I've worked with. Building owner trust and keeping projects moving beneath that level of scrutiny is a discipline I carry into every engagement.

My estimating background spans detailed takeoffs, ROM budgeting through schematic and design development phases, and VE that protects design intent while protecting the owner's budget — at SODO Builders I captured \$400K+ in facade savings without compromising the architect's vision. I'm also comfortable running multiple projects simultaneously without losing focus on quality, schedule, or cost at any site.

I'd welcome the opportunity to hear more about your pipeline and discuss how I can contribute. Thank you for your consideration.

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
