// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Featured Project Portfolio")

// This module provides expanded project details suitable for:
// - LinkedIn Featured section
// - Portfolio websites
// - Detailed project discussions in interviews
// - Client presentations

#cvEntry(
  title: [2210 Eastlake Apartments],
  society: [8-story, 57-unit multifamily development],
  date: [\$12M • 2022-2024],
  location: [Seattle, WA],
  description: list(
    [*Project Scope*: 35,000 SF, 8-story, 57-unit apartment building using podium construction (6 over 2 Type III/V wood frame over concrete podium)],
    [*Challenge*: Tight urban site in Seattle's Eastlake neighborhood requiring careful coordination with neighboring properties and city agencies],
    [*Solution*: Implemented comprehensive safety program and maintained strong communication with all stakeholders throughout construction],
    [*Results*: Zero safety incidents, project completed meeting owner's budget and schedule expectations, strong subcontractor relationships maintained throughout],
    [*Key Responsibilities*: Full P&L accountability, team development, client relations, schedule management, subcontractor coordination, project controls, financial reporting and forecasting]
  ),
  tags: ("Multifamily", "Podium Construction", "Urban Development", "Team Leadership", "Seattle")
)

#cvEntry(
  title: [Hyatt Place Hotel & Apartments],
  society: [Mixed-use hotel and multifamily project],
  date: [\$40M • Completed 2 months early],
  location: [Seattle, WA],
  description: list(
    [*Project Scope*: Combined hotel and apartment development in Seattle's competitive hospitality market],
    [*Challenge*: Project falling behind schedule in early phases; needed to recover timeline and manage significant late-stage scope changes],
    [*Solution*: Mid-project implementation of Last Planner System, creating collaborative planning process with all trade partners. Established aggressive but achievable weekly work plans with stakeholder buy-in],
    [*Results*: Substantial completion achieved 2 months ahead of revised schedule. Successfully negotiated and implemented 25 Construction Change Directives valued at over \$4M in final four months while maintaining momentum],
    [*Client Impact*: Fostered culture of trust and collaboration through consistent advocacy, fairness, diligence, and transparency throughout challenging project conditions],
    [*Recognition*: Project served as case study for effective Last Planner System implementation on distressed projects]
  ),
  tags: ("Hospitality", "Multifamily", "Lean Construction", "Last Planner System", "Schedule Recovery", "Change Management")
)

#cvEntry(
  title: [255 S. King Street],
  society: [Twin tower development in Pioneer Square],
  date: [\$200M • 600,000 SF],
  location: [Seattle, WA],
  description: list(
    [*Project Scope*: Major mixed-use development in Seattle's historic Pioneer Square district consisting of 23-story Embassy Suites hotel tower, 18-story office/parking tower, connected by 10-story glass atrium],
    [*Challenge*: Complex high-rise construction in historic district with strict design review requirements; coordination of two simultaneous concrete towers with shared infrastructure],
    [*Solution*: Developed comprehensive logistics and sequencing plan for dual tower construction. Coordinated closely with historic preservation board and city agencies],
    [*Key Scope*: Managed building envelope construction including curtain wall system, precast elements, and insulated metal panels for both towers],
    [*Results*: Successfully delivered large-scale urban project meeting aggressive timeline and budget requirements in sensitive historic context],
    [*Technical Expertise*: High-rise concrete construction, complex building envelopes, urban logistics, historic preservation requirements]
  ),
  tags: ("High-Rise", "Hospitality", "Office", "Historic District", "Building Envelope", "Urban Construction")
)

#cvEntry(
  title: [The Alaska Building Renovation],
  society: [Award-winning historic restoration],
  date: [\$12M+ • Multiple national awards],
  location: [Seattle, WA],
  description: list(
    [*Project Scope*: Complete renovation and seismic retrofit of iconic 1904 historic office building in Seattle's downtown core],
    [*Challenge*: Preserve historic character while implementing modern seismic standards and building systems; navigate complex historic preservation requirements],
    [*Solution*: Collaborated closely with preservation architects, structural engineers, and SHPO to develop solutions honoring building's history while ensuring modern safety standards],
    [*Change Management*: Successfully negotiated and executed over \$6M in scope changes while maintaining positive, cooperative relationship with owner],
    [*Results*: Project recognized with prestigious national awards for excellence in historic restoration],
    [*Awards*: 2009 National Excellence in Construction Awards - Eagle Award Winner for Best Historic Restoration; 2009 Northwest Construction - Best Historic Renovation],
    [*Additional Contributions*: Developed marketing content including photography and copy that contributed to national award recognition]
  ),
  tags: ("Historic Restoration", "Seismic Retrofit", "Award-Winning", "Preservation", "Downtown Seattle")
)

#cvEntry(
  title: [Barton Senior Residences],
  society: [Lean construction case study],
  date: [\$12M • 15% faster delivery],
  location: [Chicago, IL],
  description: list(
    [*Project Scope*: Senior living facility requiring careful attention to occupied building considerations and resident comfort during construction],
    [*Innovation*: Led project-specific Lean Construction initiative, partnering with key trades to develop aggressive but achievable schedule using Last Planner System principles],
    [*Collaboration Approach*: Weekly pull planning sessions with all trades, commitment-based scheduling, proactive constraint removal],
    [*Schedule Performance*: Achieved 15% reduction in overall construction duration compared to baseline schedule],
    [*Cost Performance*: Nearly 10% budget savings through diligent and timely buyout negotiations and contract execution],
    [*Lessons Learned*: Project served as template for Lean implementation on future senior living projects; demonstrated value of collaborative planning and trade partner engagement]
  ),
  tags: ("Healthcare", "Senior Living", "Lean Construction", "Pull Planning", "Cost Savings", "Schedule Optimization")
)

#cvEntry(
  title: [Temple Lofts Historic Conversion],
  society: [Adaptive reuse of Masonic Temple],
  date: [\$25M • Historic adaptive reuse],
  location: [Long Beach, CA],
  description: list(
    [*Project Scope*: Seismic retrofit and complete renovation of historic Masonic Temple, converting ceremonial spaces into luxury loft apartments],
    [*Historic Significance*: Preserved character-defining features including ornate plasterwork, ceremonial spaces, and architectural details while adapting for residential use],
    [*Technical Challenges*: Complex seismic retrofit in historic unreinforced masonry building; integration of modern MEP systems without compromising historic character],
    [*Regulatory Navigation*: Secured historic tax credits, worked through state historic preservation office review, maintained Mills Act benefits],
    [*Market Success*: High tenant satisfaction and occupancy rates, successful lease-up demonstrating market appeal of historic properties],
    [*Results*: Delivered project on schedule with no delays despite complex regulatory environment and technical challenges]
  ),
  tags: ("Historic Conversion", "Adaptive Reuse", "Seismic Retrofit", "Luxury Residential", "Historic Tax Credits")
)

#cvEntry(
  title: [Quail Park of Lynnwood Expansion],
  society: [Occupied senior living expansion],
  date: [\$35M • 3-story addition + 14 cottages],
  location: [Lynnwood, WA],
  description: list(
    [*Project Scope*: Major expansion of fully operational assisted living and memory care facility, adding 3-story building wing plus 14 independent cottage-style duplex residences with extensive sitework],
    [*Critical Constraint*: Construction on occupied campus serving vulnerable senior population requiring continuous operations and resident safety],
    [*Safety Approach*: Implemented stringent construction barrier protocols, noise management strategies, and communication plans to protect residents while maintaining quality of life],
    [*Stakeholder Coordination*: Daily coordination with facility management, activities directors, and care staff to schedule work around resident routines and facility operations],
    [*Logistics*: Managed complex phasing to maintain emergency access, deliveries to operating facility, and separation of construction traffic from resident areas],
    [*Outcome*: Successfully delivered large addition with minimal disruption to residents; maintained positive relationships with facility staff throughout construction]
  ),
  tags: ("Senior Living", "Occupied Facility", "Healthcare", "Phased Construction", "Stakeholder Management")
)

#pagebreak()
