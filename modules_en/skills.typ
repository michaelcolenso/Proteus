// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvSkill, hBar
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)


#cvSection("Skills & Core Competencies")

#cvSkill(
  type: [Project Management],
  info: [CPM Scheduling #hBar() Budget Management (\$1M-\$200M) #hBar() ROM & Detailed Estimating #hBar() Risk Mitigation #hBar() Contract Administration #hBar() Subcontractor Management #hBar() Owner Relations #hBar() Team Leadership #hBar() Safety Management #hBar() Quality Control #hBar() Progress Reporting],
)

#cvSkill(
  type: [Construction Specializations],
  info: [High-Rise #hBar() Multifamily #hBar() Historic Renovation #hBar() Luxury Residential #hBar() Healthcare/Senior Living #hBar() Hospitality #hBar() Podium Construction #hBar() Seismic Retrofit #hBar() Occupied Facilities],
)

#cvSkill(
  type: [Methodologies & Processes],
  info: [Last Planner System #hBar() Lean Construction #hBar() Design-Build #hBar() Negotiated Work #hBar() Value Engineering #hBar() Pull Planning #hBar() Preconstruction Services #hBar() Estimating #hBar() Buyout Management #hBar() Change Order Management #hBar() Client Updates],
)

#cvSkill(
  type: [Software & Technology],
  info: [MS Project #hBar() Primavera P6 #hBar() Procore #hBar() Bluebeam Revu #hBar() MS Office Suite #hBar() Smartsheet #hBar() BuilderTrend #hBar() AutoCAD (reading/markup) #hBar() Excel (Advanced) #hBar() Python #hBar() JavaScript],
)

