// CV Variant: Estimator / Preconstruction Manager
// Emphasis: Estimating, value engineering, preconstruction, buyout
// Target Roles: Estimator, Senior Estimator, Preconstruction Manager

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
  "professional",      // Focus on preconstruction and estimating experience
  "projects",          // Emphasize project budgets and cost management
  "skills",            // Highlight estimating, value engineering, buyout
  "education",
  "certificates",
))

// This variant emphasizes:
// - Estimating and preconstruction experience
// - Value engineering and cost savings achievements (10% savings at Barton)
// - Bid evaluation and subcontractor buyout
// - Contract negotiation and scope development
// - Design-build and negotiated work experience
// - Budget management across $1M-$200M projects
// - Cost projection and forecasting
