// CV Variant: Executive Summary (One-Page)
// Emphasis: Quick overview for networking, recruiters, initial contact
// Use Cases: Networking events, recruiter emails, quick applications
// Format: Single page with highlights

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
  "exec_summary",      // Professional summary, competencies, key projects
  "education",         // Educational credentials
))

// This one-page variant provides:
// - Executive summary paragraph (3-4 sentences)
// - Core competencies in two-column format
// - 4-5 key project highlights with $ values
// - Education
// - Contact information in header
//
// Perfect for situations where a full CV is too much:
// - Initial networking conversations
// - Email introductions through recruiters
// - Quick job board applications
// - Career fair handouts
