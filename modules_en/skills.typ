// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvSkill, hBar
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)


#cvSection("Skills and Proficiencies")

#cvSkill(
  type: [General],
  info: [Leadership #hBar() Client Relations #hBar() CPM Scheduling #hBar() Estimating #hBar() Preconstruction #hBar() Value Engineering #hBar() Forecasting/Cost Projections #hBar() Claims Analysis #hBar() Change Management #hBar() Lean Construction #hBar() Contract Negotiation #hBar() Scope Development #hBar() Business Development #hBar() Construction Operations #hBar() Verbal and Written Communication],
)

#cvSkill(
  type: [Software],
  info: [MS Project #hBar() Primavera P6 #hBar() Procore #hBar() Bluebeam #hBar() MS Excel/Word/Outlook #hBar() Smartsheet #hBar() BuilderTrend #hBar() Python #hBar() JavaScript #hBar() HTML #hBar() CSS]
)


