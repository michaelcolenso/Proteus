// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvSkill, hBar
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)


#cvSection("Core Competencies")

#cvSkill(
  type: [Project Expertise],
  info: [Multifamily & High-Rise Construction #hBar() Luxury & Custom Residential #hBar() Historic Renovation & Seismic Retrofit #hBar() Healthcare/Senior Living #hBar() Hospitality #hBar() Podium Construction],
)

#cvSkill(
  type: [Project Management],
  info: [CPM Scheduling #hBar() Preconstruction & Estimating #hBar() Value Engineering #hBar() GMP & Design-Build Delivery #hBar() P&L Management #hBar() Budget Management (\$1M-\$200M) #hBar() Team Leadership #hBar() Safety Management (Zero Incidents) #hBar() Quality Control],
)

#cvSkill(
  type: [Core Competencies],
  info: [Change Order Negotiation #hBar() Claims Mitigation #hBar() Client Relations #hBar() Last Planner System #hBar() Lean Construction #hBar() Subcontractor Management #hBar() Contract Administration #hBar() Pull Planning #hBar() Risk Management],
)

#cvSkill(
  type: [Software & Tools],
  info: [Procore #hBar() MS Project #hBar() Primavera P6 #hBar() Bluebeam Revu #hBar() MS Office Suite #hBar() Smartsheet #hBar() BuilderTrend #hBar() Excel (Advanced) #hBar() AutoCAD],
)

