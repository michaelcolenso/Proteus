// CV Variant: Senior Project Manager
// Emphasis: Leadership, P&L management, client relations, large projects
// Target Roles: Senior PM, Project Executive, Construction Manager

// Imports
#import "@preview/brilliant-cv:2.0.3": cv
#let metadata = toml("./metadata.toml")
#let importModules(modules, lang: metadata.language) = {
  for module in modules {
    include {
      "modules_" + lang + "/" + module + ".typ"
    }
  }
}

#show: cv.with(
  metadata,
  profilePhoto: none,
)

#importModules((
  "professional",      // Full professional experience showing progression
  "projects",          // Highlight major projects with $ values
  "skills",            // Emphasize leadership and management skills
  "education",         // Educational background
  "certificates",      // Professional certifications
))

// This variant emphasizes:
// - Progressive career growth and increasing responsibility
// - Large project values ($12M - $200M range)
// - P&L management and budget accountability
// - Team leadership and development
// - Client relationship management
// - Multi-sector experience
