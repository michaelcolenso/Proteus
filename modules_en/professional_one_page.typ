// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Professional Experience")

#cvEntry(
    title: [Bartender],
    society: [Easy Street Records],
    logo: none,
    date: [2024 – Present],
    location: [Seattle, WA],
    description: list(
      [Craft beverages and maintain efficient operations in iconic Seattle music venue],
      [Foster welcoming atmosphere while engaging diverse clientele in fast-paced setting]
    ),
    tags: ("Customer Service", "Beverage Operations", "Music Venue")
)

#cvEntry(    
    title: [Project Manager],
    society: [STS Construction],
    logo: none,
    date: [2022 – 2024],
    location: [Seattle, WA],
    description: list(
      [Managed 58-unit podium-style multifamily project through successful completion],
      [Developed and enforced safety protocols resulting in zero incidents during construction],
      [Implemented solutions-oriented approach to reduce conflicts and maintain project momentum]
    ),
    tags: ("Multifamily Construction", "Team Leadership", "Safety Management")
)

#cvEntry(
    title: [Project Manager],
    society: [Toth Construction],
    logo: none,
    date: [2020 – 2022],
    location: [Seattle, WA],
    description: list(
      [Managed high-end residential projects, coordinating with elite design professionals and craftspeople],
      [Maintained client satisfaction through meticulous attention to detail and clear communication]
    ),
    tags: ("Luxury Residential", "Client Relations", "Project Delivery")
)

#cvEntry(
    title: [Project Manager],
    society: [Discovery Land Company],
    logo: none,
    date: [2017 – 2018],
    location: [Abaco, Bahamas],
    description: list(
      [Oversaw construction of luxury homes in remote island setting, resolving complex logistics challenges],
      [Managed international procurement and vendor relationships to maintain material availability]
    ),
    tags: ("International Construction", "Luxury Residential", "Supply Chain")
)

#cvEntry(
    title: [Software Developer],
    society: [Various Tech Companies],
    logo: none,
    date: [2012 – 2015],
    location: [California & Washington],
    description: list(
      [Built web applications using JavaScript, HTML5, CSS3, and MongoDB at Cloudmunch, Team Coco, and CP+B],
      [Contributed to development teams at startups and established companies, focusing on front-end and full-stack solutions]
    ),
    tags: ("Web Development", "JavaScript", "Full Stack", "Agile")
)]
