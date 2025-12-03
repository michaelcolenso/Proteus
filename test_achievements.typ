// Achievement Database Integration Test
// This file tests the achievement_helpers.typ functions

#import "modules_en/achievement_helpers.typ": *

#set page(width: 8.5in, height: 11in, margin: 1in)
#set text(size: 11pt)

= Achievement Database Integration Test

== Basic Value Retrieval

Testing `get_achievement()` function:

- Eastlake project value: #get_achievement("eastlake-value")
- Eastlake units: #get_achievement("eastlake-units")
- Eastlake square footage: #get_achievement("eastlake-sf")
- King Street project value: #get_achievement("king-street-value")

== Numeric Values

Testing `get_achievement_numeric()` function:

- Eastlake value (numeric): #get_achievement_numeric("eastlake-value")
- King Street value (numeric): #get_achievement_numeric("king-street-value")

== Project Achievements

Testing `get_project_achievements()` function:

Achievements for "2210 Eastlake":
#let eastlake_achievements = get_project_achievements("2210 Eastlake")
#for achievement in eastlake_achievements [
  - #achievement.metric: #achievement.value
]

== Filtering by Tags

Testing `get_achievements_by_tags()` function:

Achievements tagged with "multifamily":
#let multifamily = get_achievements_by_tags(("multifamily",))
Found #multifamily.len() multifamily achievements

== Total Project Value

Testing `get_total_project_value()` and `format_currency()` functions:

Total project value: #format_currency(get_total_project_value())

== Sample Usage in CV Context

Managed a #get_achievement("eastlake-value") multifamily project with #get_achievement("eastlake-units"), completing the #get_achievement("eastlake-stories") building ahead of schedule.

Successfully delivered over #format_currency(get_total_project_value()) in construction projects across multiple sectors, including the #get_achievement("king-street-value") King Street development.

== Metadata

Testing `get_metadata()` function:

Database metadata:
#let meta = get_metadata()
- Version: #meta.version
- Last updated: #meta.last_updated
- Total achievements: #meta.total_achievements
- Owner: #meta.owner

---

*Test completed successfully if all values appear above without errors*
