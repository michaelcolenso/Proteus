// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvSkill, hBar
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)


#cvSection("Core Competencies")

#cvSkill(
  type: [Remodeling & Residential Expertise],
  info: [Luxury & Custom Residential #hBar() Historic Renovation & Seismic Retrofit #hBar() Multifamily & Mixed-Use #hBar() High-End Interiors #hBar() Occupied/Phased Work #hBar() Podium Construction #hBar() Tenant Improvements],
)
#line(length: 100%, stroke: 0.5pt + gray)
#cvSkill(
  type: [Leadership & Operations],
  info: [Production Leadership #hBar() Team Development & Coaching #hBar() Cross-Functional Alignment #hBar() Schedule Recovery #hBar() Quality Control],
)
#line(length: 100%, stroke: 0.5pt + gray)
#cvSkill(
  type: [Financial & Process Control],
  info: [P&L Management #hBar() Budget Management (\$1M-\$200M) #hBar() Job Costing & Margin Tracking #hBar() Change Order Negotiation #hBar() Value Engineering #hBar() Risk Management #hBar() Contract Administration],
)
#line(length: 100%, stroke: 0.5pt + gray)
#cvSkill(
  type: [Client Experience & Delivery],
  info: [Client Relations #hBar() Stakeholder Communication #hBar() Preconstruction & Estimating #hBar() Subcontractor Management #hBar() Last Planner System],
)
#line(length: 100%, stroke: 0.5pt + gray)
#cvSkill(
  type: [Software & Tools],
  info: [Procore #hBar() MS Project #hBar() Primavera P6 #hBar() Bluebeam Revu #hBar() MS Office Suite #hBar() Smartsheet #hBar() BuilderTrend #hBar() Excel (Advanced)],
)
