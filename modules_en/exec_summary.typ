// Executive Summary Module - Ultra-condensed for one-page CV
#import "@preview/brilliant-cv:2.0.3": cvSection
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("Professional Summary")

#align(left)[
  Construction Project Manager with 20+ years of progressive experience delivering complex projects from \$1M to \$200M across multifamily, high-rise, hospitality, healthcare, and historic renovation sectors. Proven track record of on-time, under-budget delivery through implementation of Lean Construction principles, collaborative stakeholder management, and solutions-oriented leadership. Notable achievements include completing \$40M hotel project 2 months early while managing \$4M+ in late-stage changes, achieving zero safety incidents on multiple projects, and earning national awards for historic restoration excellence.
]

#v(5pt)

#cvSection("Core Competencies")

#grid(
  columns: (1fr, 1fr),
  gutter: 10pt,
  [
    • Project Management (\$1M-\$200M) \
    • Team Leadership & Development \
    • Client Relations & Communication \
    • CPM Scheduling (MS Project, P6) \
    • Budget & Cost Control \
    • Contract Negotiation \
  ],
  [
    • Lean Construction & Last Planner \
    • Value Engineering \
    • Safety Management (Zero incidents) \
    • Subcontractor Coordination \
    • Change Order Management \
    • Preconstruction Services \
  ]
)

#cvSection("Recent Key Projects")

*2210 Eastlake* (\$12M) – 8-story, 57-unit multifamily, Seattle | *STS Construction* (2022-2024) \
Led complete project delivery with full P&L responsibility, zero safety incidents

*Hyatt Place Hotel & Apartments* (\$40M) – Mixed-use hospitality/multifamily, Seattle | *Osborne Construction* (2018-2019) \
Completed 2 months early through Last Planner System; managed \$4M+ late changes

*255 S. King Street* (\$200M) – Twin 23-story & 18-story towers, Seattle | *SODO Builders* (2016-2017) \
High-rise building envelope including curtain wall, precast, insulated metal panels

*Alaska Building* (\$12M+) – Historic renovation, Seattle | *Graham Construction* (2007-2011) \
National award winner for historic restoration excellence; \$6M+ negotiated changes
