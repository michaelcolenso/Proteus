    // Imports
    #import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry
    #let metadata = toml("../metadata.toml")
    #let cvSection = cvSection.with(metadata: metadata)
    #let cvEntry = cvEntry.with(metadata: metadata)
    
    #cvSection("Selected Projects")
    
    #columns[        
    
    #cvEntry(      title: [2210 Eastlake],
      society: [8-story, 57-unit apartment building],
      date: [\$12M],
      location: [Seattle, WA],
      description: list(
        [35,000 SF, 8-story, 57-unit multifamily apartment building in Seattle’s Eastlake neighborhood (podium construction: 6 over 2).],
        [Held full responsibility for project team development and direction, client relations, subcontractor coordination, project scheduling and controls, and project financials—including reporting and forecasting.]
      ),
      tags: ("Multifamily", "Project Management", "Team Leadership")
    )
    
    #cvEntry(
      title: [255 S. King St],
      society: [Twin towers development in Pioneer Square],
      date: [\$200M],
      location: [Seattle, WA],
      description: list(
        [Managed the construction of a 600,000 SF development in Seattle's Pioneer Square, including two concrete towers: a 23-story Embassy Suites hotel and an 18-story office tower/parking garage connected by a 10-story glass atrium.],
        [Coordinated complex logistics and sequencing for high-rise construction, ensuring adherence to aggressive timelines and budget constraints.]
      ),
      tags: ("High-Rise Construction", "Hospitality")
    )
    
    #cvEntry(
      title: [Hyatt Place Hotel & Apartments],
      society: [Hotel and apartments completed two months early],
      date: [\$40M],
      location: [Seattle, WA],
      description: list(
        [Spearheaded mid-project implementation of the Last Planner System, creating aggressive and efficient construction schedules; achieved substantial completion two months early.],
        [Implemented 25 Construction Change Directives in the final four months, successfully negotiating over \$4M in late changes to project scope while maintaining project momentum.],
        [Fostered a culture of trust and collaboration with the owner/client by consistently demonstrating advocacy, fairness, diligence, and transparency throughout a challenging project.]
      ),
      tags: ("Hospitality", "Multi-Family", "Last Planner System", "Change Management")
    )
    
    #cvEntry(
      title: [The Alaska Building Renovation],
      society: [Award-winning historic renovation],
      date: [\$12M+],
      location: [Seattle, WA],
      description: list(
        [Executed over \$6M in negotiated changes while maintaining a positive and cooperative relationship with the owner.],
        [Developed marketing content, including copy and photography, contributing to the project's recognition with prestigious national awards.],
        [- 2009 National Excellence in Construction Awards - Eagle Award Winner for Best Historic Restoration],
        [- 2009 Northwest Construction - Best Historic Renovation]
      ),
      tags: ("Historic Restoration", "Seismic Retrofit", "Award-Winning Projects")
    )
    #colbreak()
    #cvEntry(
      title: [Barton Senior Residences],
      society: [Senior residence project completed 15% faster],
      date: [\$12M],
      location: [Chicago, IL],
      description: list(
        [Led a project-specific Lean Construction initiative, collaborating closely with key trades to develop an aggressive and achievable project schedule using the Last Planner System.],
        [Achieved nearly 10% budget savings through diligent and timely buyout negotiations and contract execution.]
      ),
      tags: ("Healthcare Facilities", "Lean Construction", "Scheduling")
    )
    
    #cvEntry(
      title: [Temple Lofts],
      society: [Historic temple converted into luxury lofts],
      date: [\$25M],
      location: [Los Angeles, CA],
      description: list(
        [Managed the seismic retrofit and complete renovation of a historic Masonic Temple in downtown Long Beach, converting it into luxury loft apartments.],
        [Preserved historical elements while integrating modern amenities, resulting in high tenant satisfaction and occupancy rates.],
        [Navigated complex regulatory requirements for historic buildings, securing necessary approvals without project delays.]
      ),
      tags: ("Historic Renovation", "Seismic Retrofit", "Multi-Family Housing")
    )
    
    #cvEntry(
      title: [Quail Park of Lynnwood Expansion],
      society: [Expansion of senior living facility],
      date: [\$35M],
      location: [Seattle, WA],
      description: list(
        [Managed a large 3-story addition to an existing and fully operational assisted living/memory care facility, ensuring minimal disruption to residents.],
        [Added 14 independent cottage-style duplex residences, along with associated sitework and utility scope.],
        [Coordinated closely with facility management to maintain safety and operational efficiency throughout construction.]
      ),
      tags: ("Senior Living", "Facility Expansion", "Project Coordination")
    )

    #cvEntry(
      title: [Luxury Residential Projects],
      society: [multiple projects],
      date: [\$15M],
      location: [Seattle & Bahamas],
      description: list(
        [Managed major remodels of historic homes in Seattle, aligning design intent with constructability, budget targets, and phasing plans.],
        [Coordinated construction of a custom apartment home on the 57th floor of a new Seattle high-rise, integrating luxury finishes with building mechanical and structural constraints while maintaining schedule and cost controls.],
        [Built several high-end beach vacation homes at Bakers Bay, addressing procurement, workforce availability, and schedule management challenges for a remote, international site.]

      ),
      tags: ("Luxury Residential", "International", "Project Management")
    )
    ]
