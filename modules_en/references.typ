// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)

#cvSection("References")

#align(left)[
  _Professional references available upon request, including:_

  #v(5pt)

  • Former project owners and clients across multiple sectors \
  • Direct supervisors and senior leadership from recent positions \
  • Subcontractor partners and trade professionals \
  • Architecture and engineering team collaborators
]
