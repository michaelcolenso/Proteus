// ============================================================================
// LUXURY RESIDENTIAL PORTFOLIO
// Michael Colenso | Construction Project Manager
// ----------------------------------------------------------------------------
// A standalone Typst presentation deck highlighting luxury residential work.
// Compile with:   typst compile portfolio.typ
//            or:  ./generate.sh portfolio
// ============================================================================

#import "modules_en/portfolio/theme.typ": *
#import "modules_en/portfolio/components.typ": *

// ---- Document metadata ------------------------------------------------------
#set document(
  title: "Michael Colenso — Luxury Residential Portfolio",
  author: "Michael Colenso",
  keywords: (
    "Luxury Residential",
    "Construction Management",
    "Ultra High Net Worth",
    "Custom Homes",
    "High-Rise",
    "Historic Renovation",
  ),
)

// ---- Global page setup ------------------------------------------------------
#set page(
  paper: "us-letter",
  margin: (x: 0.9in, y: 0.85in),
  fill: cream,
)

#set text(
  font: body-font,
  size: 10.5pt,
  fill: charcoal,
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.72em,
  first-line-indent: 0pt,
)

#show heading: set text(font: heading-font, fill: navy)
#show link: set text(fill: gold-dark)

// ============================================================================
// 1. COVER PAGE
// ============================================================================
#include "modules_en/portfolio/cover.typ"

// ============================================================================
// 2. PHILOSOPHY / APPROACH
// ============================================================================
#include "modules_en/portfolio/philosophy.typ"

// ============================================================================
// 3. BY THE NUMBERS
// ============================================================================
#include "modules_en/portfolio/metrics.typ"

// ============================================================================
// 4. FEATURED PROJECTS
// ============================================================================
#include "modules_en/portfolio/projects.typ"

// ============================================================================
// 5. SERVICE CAPABILITIES
// ============================================================================
#include "modules_en/portfolio/capabilities.typ"

// ============================================================================
// 6. CONTACT / CLOSING
// ============================================================================
#include "modules_en/portfolio/contact.typ"
