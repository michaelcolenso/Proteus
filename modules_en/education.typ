// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry, hBar
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)


#cvSection("Education")

#cvEntry(
  title: [Northern Michigan University],
  society: [Bachelor of Science, Construction Management],
  date: [2004],
  location: [Marquette, MI],
  logo: image("../src/logos/ucla.png"),
  description: none,
)
