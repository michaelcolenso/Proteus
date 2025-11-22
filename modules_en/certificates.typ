// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvHonor
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvHonor = cvHonor.with(metadata: metadata)


#cvSection("Certifications & Training")

#cvHonor(
  date: [],
  title: [OSHA 30-Hour Construction Safety],
  issuer: [Occupational Safety and Health Administration],
)

#cvHonor(
  date: [],
  title: [Lean Construction Training],
  issuer: [Lean Construction Institute],
)

#cvHonor(
  date: [],
  title: [Last Planner System Implementation],
  issuer: [Lean Construction Institute],
)

// Uncomment and add date if you have these certifications:
// #cvHonor(
//   date: [2024],
//   title: [Project Management Professional (PMP)],
//   issuer: [Project Management Institute],
// )

// #cvHonor(
//   date: [2023],
//   title: [LEED Accredited Professional],
//   issuer: [U.S. Green Building Council],
// )

// #cvHonor(
//   date: [2022],
//   title: [Certified Construction Manager (CCM)],
//   issuer: [Construction Management Association of America],
// )
