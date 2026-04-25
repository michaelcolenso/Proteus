// BOLD EDUCATION MODULE
// Minimal, impactful presentation

#boldSection("Education")

#grid(
  columns: (1fr, auto),
  gutter: 24pt,
  
  align(left + top,
    block(
      {
        text(
          font: font-header,
          size: 10.5pt,
          weight: 700,
          fill: deep-steel,
          "Northern Michigan University"
        )
        v(2pt)
        text(
          font: font-body,
          size: 9.5pt,
          fill: charcoal,
          "Bachelor of Science, Construction Management"
        )
      }
    )
  ),
  
  align(right + top,
    block(
      {
        text(
          font: font-mono,
          size: 8pt,
          fill: warm-gray,
          "2004 | Marquette, MI"
        )
      }
    )
  )
)
