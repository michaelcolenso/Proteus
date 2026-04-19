// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry
#import "achievement_helpers.typ": get_achievement
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Professional Experience")

#columns(2, gutter: 1em)[
  #cvEntry(
    title: [Project Manager],
    society: [STS Construction],
    logo: none,
    date: [2022 – 2025],
    location: [Seattle, WA],
    description: list(
      [*Spearheaded \$12M, 57-unit multifamily delivery,* optimizing P&L management, 18 subcontractor teams, and client relations from groundbreak to occupancy],
      [*Secured zero recordable safety incidents* over 24 months, orchestrating a 35+ person workforce through rigorous field leadership],
    ),
    tags: ("Multifamily Construction", "Production Leadership", "Budget Management")
  )

  #cvEntry(
    title: [Project Manager],
    society: [Toth Construction],
    logo: none,
    date: [2020 – 2022],
    location: [Seattle, WA],
    description: list(
      [*Strategically directed \$8M+ in luxury residential projects,* uniting world-class architects and artisans to execute flawless, high-end environments],
      [*Cemented long-term client loyalty,* securing formal referrals and repeat commissions through exceptional advisor-level engagement],
    ),
    tags: ("Client Experience", "Luxury Residential", "Project Scheduling")
  )

  #cvEntry(
    title: [Project Manager],
    society: [Osborne Construction Company],
    logo: none,
    date: [2018 – 2019],
    location: [Redmond, WA],
    description: list(
      [*Drove data-backed owner decision-making* through high-precision cost reports and cash flow modeling for a \$35M facility expansion],
      [*Captured \$4M+ in scope variance,* neutralizing claims exposure through rigorous documentation and principled negotiation],
    ),
    tags: ("Risk Management", "Financial Reporting", "Stakeholder Communication", "Change Management")
  )

  #colbreak()

  #cvEntry(
    title: [Project Manager],
    society: [Discovery Land Company],
    logo: none,
    date: [2017 – 2018],
    location: [Abaco, Bahamas],
    description: list(
      [*Elevated luxury vacation home delivery* in exclusive development, surpassing exacting benchmarks for ultra-discerning clientele],
      [*Optimized supply chain resilience* by architecting strategic vendor partnerships, capturing 30% reduction in lead times],
    ),
    tags: ("International Projects", "Luxury Residential", "Procurement")
  )

  #cvEntry(
    title: [Project Manager],
    society: [SODO Builders],
    logo: none,
    date: [2016 – 2017],
    location: [Seattle, WA],
    description: list(
      [*Engineered complex building envelope delivery* for a \$200M twin-tower landmark, precisely integrating curtain wall and precast systems],
      [*Captured \$400K+ in value-engineered facade savings* by pioneering a proactive change management framework that mitigated exposure],
    ),
    tags: ("High-Rise Construction", "Value Engineering", "Claims Mitigation")
  )

  #cvEntry(
    title: [Project Engineer / Field Engineer],
    society: [Graham, Skender, West Builders],
    logo: none,
    date: [2004 – 2011],
    location: [Seattle, Chicago, Los Angeles],
    description: list(
      [*Accelerated professional progression* from Field Engineer to Project Engineer through hands-on leadership across high-stakes education and hospitality projects],
      [*Commanded \$50M+ in contracted scope,* establishing repeat-client satisfaction by delivering large-scale projects within compressed windows],
    ),
    tags: ("Preconstruction", "Project Management", "Multisector Experience")
  )
]
