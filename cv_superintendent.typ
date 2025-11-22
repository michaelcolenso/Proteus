// CV Variant: Superintendent / Field Operations
// Emphasis: On-site management, safety, trade coordination, field operations
// Target Roles: Superintendent, Senior Superintendent, Field Manager

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
  "professional",      // Emphasize field experience and on-site leadership
  "projects",          // Focus on construction types and field challenges
  "skills",            // Highlight safety, trade coordination, field operations
  "certificates",      // OSHA and safety certifications prominent
  "education",
))

// This variant emphasizes:
// - Zero safety incident track record
// - On-site team leadership and development
// - Subcontractor and trade coordination
// - Quality control and field problem-solving
// - Schedule management from field perspective
// - Building envelope and structural experience
// - Safety program implementation
