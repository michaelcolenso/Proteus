// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry
#import "achievement_helpers.typ": get_achievement
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Professional Experience")

#columns[  
  // #cvEntry(
  //   title: [Bartender],
  //   society: [Easy Street Records],
  //   logo: none,
  //   date: [2024 – Present],
  //   location: [Seattle, WA],
  //   description: list(
  //     [Craft exceptional beverages while fostering a welcoming atmosphere in an iconic Seattle music venue],
  //     [Maintain efficient bar operations while engaging with a diverse clientele in a fast-paced environment]
  //   ),
  //   tags: ("Customer Service", "Beverage Operations", "Music Venue")
  // )

  #cvEntry(
    title: [Project Manager],
    society: [STS Construction],
    logo: none,
    date: [2022 – 2025],
    location: [Seattle, WA],
    description: list(
      [*Delivered \$12M, 57-unit podium-style multifamily building* (35,000 SF, 8 stories) in Seattle's Eastlake neighborhood—managing full P&L, 18 subcontractors, and direct owner relationship from groundbreak through certificate of occupancy],
      [*Maintained zero recordable safety incidents* across 24-month project with average daily workforce of 35+ across all trades],
      [*Resolved 40+ RFIs and field coordination conflicts* with average 48-hour turnaround, preventing schedule impacts on critical-path framing and MEP rough-in activities]
    ),
    tags: ("Multifamily Construction", "Team Leadership", "Budget Management")
  )

  #cvEntry(
    title: [Project Manager],
    society: [Toth Construction],
    logo: none,
    date: [2020 – 2022],
    location: [Seattle, WA],
    description: list(
      [*Managed portfolio of \$8M+ in luxury residential projects* for ultra-high-net-worth clients, coordinating with world-class architects and specialty craftspeople to deliver exceptional built environments],
      [*Cultivated trusted advisor relationships with discerning clients,* resulting in 3 referrals and 2 repeat engagements during tenure],
      [*Coordinated 57th-floor custom apartment buildout* in active high-rise, integrating luxury finishes with base building systems while maintaining strict schedule and access constraints]
    ),
    tags: ("Client Relations", "Luxury Residential", "Project Scheduling")
  )

  #cvEntry(
    title: [Project Manager],
    society: [Osborne Construction Company],
    logo: none,
    date: [2018 – 2019],
    location: [Redmond, WA],
    description: list(
      [*Delivered detailed monthly cost reports and cash flow projections* to ownership group, supporting informed decision-making on \$35M senior living facility expansion],
      [*Managed \$4M+ in scope changes* through proactive documentation and fair negotiation, maintaining positive owner relationship throughout],
      [*Created and maintained comprehensive CPM schedule* that drove successful on-time delivery despite 14 owner-directed changes to program]
    ),
    tags: ("Risk Management", "Financial Reporting", "Stakeholder Communication", "Change Management")
  )

  #cvEntry(
    title: [Project Manager],
    society: [Discovery Land Company],
    logo: none,
    date: [2017 – 2018],
    location: [Abaco, Bahamas],
    description: list(
      [*Oversaw construction of multiple luxury vacation homes* in exclusive private development, meeting exacting quality standards for clientele expecting world-class service],
      [*Established strategic vendor partnerships* that ensured material availability despite supply chain constraints inherent to remote island location, reducing procurement delays by 30%],
      [*Managed all project phases across international borders,* efficiently navigating customs, logistics, and workforce challenges unique to Caribbean construction]
    ),
    tags: ("International Projects", "Luxury Residential", "Procurement")
  )

  #colbreak()

  #cvEntry(
    title: [Project Manager],
    society: [SODO Builders],
    logo: none,
    date: [2016 – 2017],
    location: [Seattle, WA],
    description: list(
      [*Coordinated building envelope construction on \$200M twin-tower development* (23-story hotel + 18-story office/parking), including curtain wall, precast, and insulated metal panel systems],
      [*Implemented rigorous change management process* that mitigated claims exposure while delivering value-engineered solutions saving \$400K+ on facade scope]
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
      [*Progressed from Field Engineer to Project Engineer* across education, retail, hospitality, healthcare, and seismic retrofit sectors],
      [*Managed \$50M+ in contracted scope at Graham,* delivering two projects in 18 months for repeat client],
      [*Developed core competencies* in preconstruction, bid evaluation, and contract negotiation]
    ),
    tags: ("Preconstruction", "Project Management", "Multisector Experience")
  )

  #cvEntry(
    title: [Career Note],
    society: [Technology Sector],
    logo: none,
    date: [2012 – 2015],
    location: [San Francisco Bay Area],
    description: list(
      [_Pursued software development, advancing to Senior Engineer at venture-backed startup. Returned to construction with enhanced technical problem-solving and data analysis capabilities._]
    ),
    tags: ("Software Development", "Cross-Functional Collaboration")
  )
]

#pagebreak()
