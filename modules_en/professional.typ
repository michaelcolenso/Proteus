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
    date: [2022 – 2024],
    location: [Seattle, WA],
    description: list(
      [Led on-site construction team to successfully complete a #get_achievement("eastlake-units"), #get_achievement("eastlake-stories"), podium style multifamily project while maintaining disciplined cost controls and schedule performance],
      [Built and maintained detailed CPM schedules, weekly look-ahead plans, and client-ready progress reports to keep stakeholders aligned],
      [Developed and enforced safety protocols, achieving zero incidents throughout all project phases]
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
      [Managed high-end luxury residential construction from preconstruction through closeout, including ROM budgets, detailed estimates, and value engineering to optimize scope and finish selections.],
      [Built and maintained master schedules, procurement logs, and subcontractor coordination plans to deliver custom homes on time and within budget.],
      [Cultivated strong relationships with ultra-high-net-worth clients, architects, and design consultants, providing consistent updates and clear decision pathways.]
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
      [Provided stakeholders with detailed monthly cost reports, cash flow projections, and variance narratives to support budget decisions],
      [Managed multiple and ongoing scope changes and successfully prepared, negotiated, and executed owner change orders and subcontract modifications],
      [Created and managed a comprehensive CPM project schedule that was crucial to the successful delivery of the project]
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
      [Oversaw construction of multiple luxury homes in a private development for extremely discerning clients expecting the highest level of service and discretion],
      [Managed all project phases across international borders, including schedule development, procurement planning, and budget tracking for long-lead materials],
      [Established strong vendor partnerships, ensuring material availability despite supply chain constraints on a remote island location]
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
      [Implemented and tracked changes to the scope of work while mitigating claims risk; Provided
value-engineered solutions where applicable and negotiated subcontractor change orders when required.],
      [Coordinated high-rise building envelope construction including curtain wall system, precast elements, and insulated metal panels for both towers.]
    ),
    tags: ("High-Rise Construction", "Value Engineering", "Claims Mitigation")
  )

  #cvEntry(
    title: [Software Developer / Senior Software Engineer],
    society: [Adonit, Team Coco, Cloudmunch],
    logo: none,
    date: [2012 – 2015],
    location: [Los Angeles, CA & Seattle, WA],
    description: list(
      [Self-taught programming skills leading to significant contributions in professional software teams],
      [Advanced to Senior Software Engineer at a cloud services startup, driving product development and scaling solutions]
    ),
    tags: ("Software Development", "Cross-Functional Collaboration")
  )
//   #cvEntry(
//     title: [Senior Software Engineer],
//     society: [Cloudmunch],
//     logo: none,
//     date: [Apr 2015 – Nov 2015 · 8 mos],
//     location: [Bellevue, Washington],
//     description: list(
//         [Contributed to enterprise JavaScript applications development, implementing DevOps solutions for improved deployment processes.],
//         [Collaborated with team members to maintain and enhance application architecture and system stability.]
//     ),
//     tags: ("JavaScript", "DevOps", "Web Development", "Team Collaboration")
// )

// #cvEntry(
//     title: [Front End Web Developer],
//     society: [Adonit],
//     logo: none,
//     date: [Mar 2014 – Mar 2015 · 1 yr 1 mo],
//     location: [Austin, TX [Remote]],
//     description: list(
//         [Worked remotely within an agile team to build and maintain web applications using modern front-end practices.],
//         [Utilized Sass, CoffeeScript, and MongoDB to implement features and improvements as part of the development team.]
//     ),
//     tags: ("Front-end Development", "Sass", "MongoDB", "Agile", "Remote Work")
// )

// #cvEntry(
//     title: [Interactive Developer],
//     society: [Crispin Porter + Bogusky],
//     logo: none,
//     date: [2013 – 2014 · 1 yr],
//     location: [Santa Monica, California],
//     description: list(
//         [Built and maintained web applications for major brand clients as part of a collaborative development team.],
//         [Participated in implementing modern frameworks and technologies to enhance application performance.]
//     ),
//     tags: ("Full Stack Development", "Web Development", "Modern Frameworks")
// )

// #cvEntry(
//     title: [Web Developer],
//     society: [Team Coco Digital],
//     logo: none,
//     date: [2013 – Jul 2013 · 7 mos],
//     location: [Burbank, California],
//     description: list(
//         [Contributed to the development of interactive features for Conan O'Brien's digital platform.],
//         [Assisted in implementing responsive design solutions to improve mobile user experience.]
//     ),
//     tags: ("Web Development", "Interactive Features", "Responsive Design")
// )

// #cvEntry(
//     title: [Web Developer],
//     society: [Lunchbox],
//     logo: none,
//     date: [Oct 2012 – Feb 2013 · 5 mos],
//     location: [Culver City, California],
//     description: list(
//         [Developed and maintained web experiences for retail clients using HTML5, CSS3, and JavaScript.],
//         [Collaborated with creative and marketing teams to implement new features and content updates.],
//         [Worked with MongoDB and modern web technologies to improve existing platform functionality.]
//     ),
//     tags: ("Web Development", "HTML5", "CSS3", "JavaScript", "MongoDB")
// )

  #cvEntry(
    title: [Project Engineer],
    society: [Graham Construction],
    logo: none,
    date: [2007 – 2011],
    location: [Seattle, WA],
    description: list(
      [Managed over \$50 million in contracted scope, completing two projects in 18 months for a single owner],
      [Supported preconstruction efforts on negotiated and design-build projects, coordinating bids, ROM pricing, and detailed estimates for public and private clients],
      [Executed complex projects in education, retail, hospitality, and seismic retrofit sectors]
    ),
    tags: ("Preconstruction", "Project Management", "Multisector Experience")
  )

  #cvEntry(
    title: [Project Engineer],
    society: [Skender Construction],
    logo: none,
    date: [2006 – 2007],
    location: [Chicago, IL],
    description: list(
      [Evaluated and reviewed bids to ensure alignment with project requirements and budget goals],
      [Developed scopes of work and negotiated subcontracts for a senior care facility project],
      [Monitored project progress, ensuring adherence to key milestones and objectives]
    ),
    tags: ("Bid Evaluation", "Contract Negotiation", "Healthcare Facilities")
  )

  #cvEntry(
    title: [Field Engineer],
    society: [West Builders],
    logo: none,
    date: [2004 – 2006],
    location: [Los Angeles, CA],
    description: list(
      [Controlled project costs and monitored progress, ensuring adherence to schedules and budgets],
      [Managed procurement, change analysis, and document control on a complex, high-stakes project]
    ),
    tags: ("Cost Control", "Procurement", "Project Documentation", "Multifamily")
  )
]

#pagebreak()
