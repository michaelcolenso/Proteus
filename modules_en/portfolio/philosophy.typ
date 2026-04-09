// ============================================================================
// PHILOSOPHY — An editorial opener establishing voice and positioning.
// ============================================================================

#import "theme.typ": *
#import "components.typ": eyebrow, section-title, pull-quote, divider

#eyebrow("Approach")
#section-title(
  [Building for \
  the discerning few.],
  subtitle: [A practice grounded in craftsmanship, trust, and quiet precision.],
)

#grid(
  columns: (1.35fr, 1fr),
  column-gutter: 28pt,
  [
    #set par(justify: true, leading: 0.78em)
    #set text(size: 10.5pt, fill: charcoal)

    Luxury residential work is a relationship business first and a
    construction business second. Over eighteen years and more than
    \$300M in delivered projects, I have built my practice around one
    conviction: that discerning clients deserve a builder who
    communicates with clarity, protects the design intent, and treats
    every detail as if it were their own.

    #v(4pt)

    My portfolio spans ultra-high-net-worth residences in Seattle and
    the Bahamas, custom high-rise apartment buildouts, historic
    adaptive reuse, and boutique multifamily developments. Across each,
    the throughline is the same — rigorous preconstruction, a disciplined
    approach to change, and an unwavering advocacy for the owner's vision.

    #v(4pt)

    I work best where the stakes are personal: where the drawings are
    ambitious, the finishes are unforgiving, and the client expects a
    builder who can quietly absorb complexity so they don't have to.
  ],
  [
    #pull-quote(
      [
        "Fostering a culture of trust and collaboration through
        consistent advocacy, fairness, diligence, and transparency."
      ],
      attribution: "Guiding Principle",
    )

    #v(10pt)

    #block(
      width: 100%,
      inset: 14pt,
      fill: cream-deep,
      radius: 2pt,
    )[
      #text(
        font: heading-font,
        size: 8.5pt,
        tracking: 1.8pt,
        fill: gold-dark,
        weight: "medium",
      )[#upper("At a Glance")]
      #v(6pt)
      #line(length: 24pt, stroke: 1pt + gold)
      #v(6pt)

      #set text(size: 9.5pt, fill: charcoal)
      #set par(leading: 0.68em)

      *18+ years* — construction leadership \
      *\$300M+* — delivered project value \
      *Zero* — recordable safety incidents \
      *2 continents* — Seattle · Bahamas \
      *Trusted advisor* — to UHNW clientele
    ]
  ],
)

#pagebreak()
