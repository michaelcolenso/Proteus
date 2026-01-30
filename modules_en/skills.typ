// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvSkill, hBar
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)


#cvSection("Core Competencies")

#cvSkill(
  type: [Remodeling & Residential Expertise],
  info: [Luxury & Custom Residential #hBar() Historic Renovation & Seismic Retrofit #hBar() Multifamily & Mixed-Use #hBar() High-End Interiors #hBar() Occupied/Phased Work #hBar() Podium Construction],
)

#cvSkill(
  type: [Leadership & Operations],
  info: [Production Leadership #hBar() Team Development & Coaching #hBar() Cross-Functional Alignment #hBar() Accountability Systems #hBar() Schedule Recovery #hBar() Safety Management (Zero Incidents) #hBar() Quality Control],
)

#cvSkill(
  type: [Financial & Process Control],
  info: [P&L Management #hBar() Budget Management (\$1M-\$200M) #hBar() Job Costing & Margin Tracking #hBar() Change Order Negotiation #hBar() Value Engineering #hBar() Risk Management #hBar() Contract Administration],
)

#cvSkill(
  type: [Client Experience & Delivery],
  info: [Client Relations #hBar() Stakeholder Communication #hBar() Preconstruction & Estimating #hBar() Subcontractor Management #hBar() Last Planner System #hBar() Lean Construction #hBar() Pull Planning],
)

#cvSkill(
  type: [Software & Tools],
  info: [Procore #hBar() MS Project #hBar() Primavera P6 #hBar() Bluebeam Revu #hBar() MS Office Suite #hBar() Smartsheet #hBar() BuilderTrend #hBar() Excel (Advanced) #hBar() AutoCAD],
)
