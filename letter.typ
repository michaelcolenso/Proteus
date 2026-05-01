// ============================================================================
// COVER LETTER — Editorial stationery matched to the luxury residential
// portfolio. Shares the navy / gold / cream palette and typography stack so
// the letter, CV, and portfolio read as one piece of correspondence.
// ----------------------------------------------------------------------------
// Compile with:   typst compile letter.typ
//            or:  ./generate.sh letter
// ============================================================================

#import "modules_en/portfolio/theme.typ": *

#let metadata = toml("./metadata.toml")

// ---- Recipient + subject (edit per application) -----------------------------
#let recipient-name    = "Landsea Homes"
#let recipient-address = "Issaquah, Washington"
#let letter-subject    = "Senior Project Manager Position"
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

I'm a Seattle-based Construction Manager with 20+ years delivering multifamily, high-rise, senior living, and luxury residential projects. My background includes high-end custom homes with Toth Construction and ultra-luxury resort residential work with Discovery Land Company, along with large technical builds across Seattle, LA, and Chicago.

I lead with strong field presence, clear communication, and disciplined scheduling. I'm fluent in the Seattle subcontractor network, permitting processes, and managing multiple jobsites while maintaining quality, safety, and cost control. My teams rely on predictable planning, early problem-solving, and coordination that keeps owners confident and projects on track.

Your focus on autonomy, accountability, and high standards aligns with how I run work. I'd bring deep regional experience, luxury-level quality expectations, and steady leadership to support your projects in Issaquah and the surrounding area.

I'd welcome a conversation about how I can contribute.

// ============================================================================
// 4. SIGN-OFF
// ============================================================================
#v(14pt)

With regards,

#v(2pt)

#image("src/signature.png", height: 46pt)

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
