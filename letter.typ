// Imports
#import "@preview/brilliant-cv:2.0.3": letter
#let metadata = toml("./metadata.toml")

// Extract color from metadata
#let accent-color = if metadata.layout.awesome_color == "darknight" {
  rgb("#1E2022")
} else if metadata.layout.awesome_color == "skyblue" {
  rgb("#0395DE")
} else if metadata.layout.awesome_color == "red" {
  rgb("#DC3522")
} else if metadata.layout.awesome_color == "nephritis" {
  rgb("#27AE60")
} else if metadata.layout.awesome_color == "concrete" {
  rgb("#95A5A6")
} else {
  // Assume hex color
  rgb(metadata.layout.awesome_color)
}

// Custom letterhead configuration
#let use-custom-letterhead = true

// Configure letter with custom styling
#show: letter.with(
  metadata,
  myAddress: "Seattle, Washington",
  recipientName: "Landsea Homes",
  recipientAddress: "Issaquah, Washington",
  date: datetime.today().display("[month repr:long] [day], [year]"),
  subject: "Re: Senior Project Manager Position",
  signature: image("src/signature.png"),
)

// Custom letterhead overlay (if enabled)
#if use-custom-letterhead {
  place(
    top + left,
    dx: 0pt,
    dy: -20pt,
    block(
      width: 100%,
      {
        // Name in large, elegant typography
        text(
          size: 24pt,
          weight: "bold",
          fill: accent-color,
          font: metadata.layout.fonts.header_font,
          [Michael Colenso]
        )
        v(-8pt)
        // Title/profession line
        text(
          size: 10pt,
          fill: rgb("#555555"),
          font: metadata.layout.fonts.regular_fonts.at(0),
          tracking: 0.5pt,
          smallcaps[Construction Project Manager]
        )
        v(4pt)
        // Elegant separator line
        line(length: 100%, stroke: 0.5pt + accent-color.lighten(40%))
        v(2pt)
        // Contact information in refined layout
        text(
          size: 9pt,
          fill: rgb("#444444"),
          {
            metadata.personal.info.phone
            h(12pt)
            sym.circle.filled.small
            h(12pt)
            metadata.personal.info.email
            h(12pt)
            sym.circle.filled.small
            h(12pt)
            [Seattle, WA]
          }
        )
        v(16pt)
      }
    )
  )
  // Add spacing to account for letterhead
  v(85pt)
}

// Enhanced typography and spacing for body text
#set par(
  leading: 0.65em,        // Line spacing within paragraphs
  spacing: 1.2em,         // Space between paragraphs
  justify: true,          // Justified text for professional appearance
  first-line-indent: 0pt  // No first-line indent (modern style)
)

#set text(
  size: 11pt,             // Slightly larger for better readability
  font: metadata.layout.fonts.regular_fonts.at(0)
)

Dear Hiring Manager,

I'm a Seattle-based Construction Manager with 20+ years delivering multifamily, high-rise, senior living, and luxury residential projects. My background includes high-end custom homes with Toth Construction and ultra-luxury resort residential work with Discovery Land Company, along with large technical builds across Seattle, LA, and Chicago.

I lead with strong field presence, clear communication, and disciplined scheduling. I'm fluent in the Seattle subcontractor network, permitting processes, and managing multiple jobsites while maintaining quality, safety, and cost control. My teams rely on predictable planning, early problem-solving, and coordination that keeps owners confident and projects on track.

Landsea's focus on autonomy, accountability, and high standards aligns with how I run work. I'd bring deep regional experience, luxury-level quality expectations, and steady leadership to support your projects in Issaquah and the surrounding area.

I'd welcome a conversation about how I can contribute.

#v(1.2em)

Best regards,

#v(2pt)

