// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Selected Projects")

    #columns[

    #cvEntry(
      title: [Hotel Delivered 2 Months Early — Hyatt Place Hotel & Apartments],
      society: [157-room hotel + 102 residential units],
      date: [\$40M],
      location: [Seattle, WA],
      description: list(
        [*Spearheaded mid-project implementation of Last Planner System,* creating aggressive pull schedules that recovered 10 weeks and achieved substantial completion 2 months ahead of contract date],
        [*Negotiated \$4M+ in late-stage scope changes* (25 CCDs in final 4 months) while maintaining project momentum and collaborative owner relationship],
        [Dual-use project: 157-room Hyatt Place hotel with 102 residential apartment units]
      ),
      tags: ("Hospitality", "Multi-Family", "Last Planner System", "Change Management")
    )

    #cvEntry(
      title: [\$200M Twin Towers — 255 S. King St],
      society: [23-story hotel + 18-story office/parking],
      date: [\$200M],
      location: [Seattle, WA],
      description: list(
        [*Managed 600,000 SF dual-tower development* in Seattle's Pioneer Square: 23-story Embassy Suites hotel and 18-story office tower/parking garage connected by 10-story glass atrium],
        [*Coordinated complex logistics and sequencing* for high-rise construction, ensuring adherence to aggressive timelines and budget constraints]
      ),
      tags: ("High-Rise Construction", "Hospitality")
    )

    #cvEntry(
      title: [Award-Winning Historic Renovation — The Alaska Building],
      society: [2009 National Excellence Eagle Award],
      date: [\$12M+],
      location: [Seattle, WA],
      description: list(
        [*Executed over \$6M in negotiated changes* while maintaining positive and cooperative relationship with owner],
        [*2009 National Excellence in Construction Awards* — Eagle Award Winner for Best Historic Restoration],
        [*2009 Northwest Construction* — Best Historic Renovation]
      ),
      tags: ("Historic Restoration", "Seismic Retrofit", "Award-Winning Projects")
    )

    #cvEntry(
      title: [2210 Eastlake],
      society: [8-story, 57-unit podium multifamily],
      date: [\$12M],
      location: [Seattle, WA],
      description: list(
        [*35,000 SF, 8-story, 57-unit multifamily apartment building* in Seattle's Eastlake neighborhood (podium construction: 6 over 2)],
        [*Held full responsibility for project P&L,* team development, client relations, subcontractor coordination, scheduling and controls, and financial reporting/forecasting]
      ),
      tags: ("Multifamily", "Project Management", "Team Leadership")
    )

    #colbreak()

    #cvEntry(
      title: [Quail Park of Lynnwood Expansion],
      society: [Senior living facility expansion],
      date: [\$35M],
      location: [Seattle, WA],
      description: list(
        [*Managed large 3-story addition* to existing and fully operational assisted living/memory care facility, ensuring minimal disruption to residents],
        [*Added 14 independent cottage-style duplex residences,* along with associated sitework and utility scope],
        [Coordinated closely with facility management to maintain safety and operational efficiency throughout construction]
      ),
      tags: ("Senior Living", "Facility Expansion", "Project Coordination")
    )

    #cvEntry(
      title: [Barton Senior Residences — 15% Faster, 10% Under Budget],
      society: [Senior care facility],
      date: [\$12M],
      location: [Chicago, IL],
      description: list(
        [*Led project-specific Lean Construction initiative,* collaborating closely with key trades to develop aggressive and achievable project schedule using Last Planner System],
        [*Achieved nearly 10% budget savings* through diligent and timely buyout negotiations and contract execution]
      ),
      tags: ("Healthcare Facilities", "Lean Construction", "Scheduling")
    )

    #cvEntry(
      title: [Temple Lofts — Historic Seismic Retrofit],
      society: [Masonic Temple conversion to luxury lofts],
      date: [\$25M],
      location: [Los Angeles, CA],
      description: list(
        [*Managed seismic retrofit and complete renovation* of historic Masonic Temple in downtown Long Beach, converting it into luxury loft apartments],
        [*Preserved historical elements* while integrating modern amenities, resulting in high tenant satisfaction and occupancy rates],
        [Navigated complex regulatory requirements for historic buildings, securing necessary approvals without project delays]
      ),
      tags: ("Historic Renovation", "Seismic Retrofit", "Multi-Family Housing")
    )

    #cvEntry(
      title: [Luxury Residential Portfolio],
      society: [International + custom homes],
      date: [\$15M],
      location: [Seattle & Bahamas],
      description: list(
        [*Managed major remodels of historic homes in Seattle,* aligning design intent with constructability, budget targets, and phasing plans],
        [*Coordinated 57th-floor custom apartment buildout* in new Seattle high-rise, integrating luxury finishes with building mechanical and structural constraints],
        [*Built several high-end beach vacation homes* at Bakers Bay, addressing procurement, workforce availability, and schedule management challenges for remote, international site]
      ),
      tags: ("Luxury Residential", "International", "Project Management")
    )
    ]
