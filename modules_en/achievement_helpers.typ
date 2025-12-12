// Achievement Database Helper Functions
// Use these functions to access achievement data consistently across all CV variants
// This ensures all numbers are accurate and consistent across CV, cover letters, and interviews

#let achievements_data = yaml("../data/achievements.yaml")

// Get a specific achievement value by ID
// Example: #get_achievement("eastlake-value") returns "$12M"
#let get_achievement(id) = {
  let achievements = achievements_data.achievements
  for achievement in achievements {
    if achievement.id == id {
      return achievement.value
    }
  }
  return "[Achievement not found: " + id + "]"
}

// Get numeric value for calculations
// Example: #get_achievement_numeric("eastlake-value") returns 12000000
#let get_achievement_numeric(id) = {
  let achievements = achievements_data.achievements
  for achievement in achievements {
    if achievement.id == id {
      return achievement.value_numeric
    }
  }
  return 0
}

// Get all achievements for a specific project
// Returns array of achievement objects
#let get_project_achievements(project_name) = {
  let achievements = achievements_data.achievements
  let results = ()
  for achievement in achievements {
    if "project" in achievement and achievement.project == project_name {
      results.push(achievement)
    }
  }
  return results
}

// Get all achievements filtered by tags
// Example: #get_achievements_by_tags(("senior-pm", "multifamily"))
#let get_achievements_by_tags(tags) = {
  let achievements = achievements_data.achievements
  let results = ()
  for achievement in achievements {
    if "tags" in achievement {
      for tag in tags {
        if tag in achievement.tags {
          results.push(achievement)
          break
        }
      }
    }
  }
  return results
}

// Get all achievements for a specific company
#let get_company_achievements(company_name) = {
  let achievements = achievements_data.achievements
  let results = ()
  for achievement in achievements {
    if "company" in achievement and achievement.company == company_name {
      results.push(achievement)
    }
  }
  return results
}

// Get total project value across all projects
#let get_total_project_value() = {
  let achievements = achievements_data.achievements
  let total = 0
  for achievement in achievements {
    if achievement.metric == "project_value" {
      total = total + achievement.value_numeric
    }
  }
  return total
}

// Format a number as currency
#let format_currency(amount) = {
  if amount >= 1000000000 {
    return "$" + str(calc.round(amount / 1000000000, digits: 1)) + "B"
  } else if amount >= 1000000 {
    return "$" + str(calc.round(amount / 1000000, digits: 0)) + "M"
  } else if amount >= 1000 {
    return "$" + str(calc.round(amount / 1000, digits: 0)) + "K"
  } else {
    return "$" + str(amount)
  }
}

// Get achievement metadata
#let get_metadata() = {
  return achievements_data.metadata
}

// Example usage patterns (commented out):
//
// Simple value retrieval:
// [Managed a #get_achievement("eastlake-value") project with #get_achievement("eastlake-units")]
//
// List all achievements for a project:
// #let eastlake = get_project_achievements("2210 Eastlake")
// #for achievement in eastlake [
//   - #achievement.value
// ]
//
// Filter by tags for CV variants:
// #let senior_pm_achievements = get_achievements_by_tags(("senior-pm", "budget"))
// #for achievement in senior_pm_achievements [
//   - #achievement.value (#achievement.project)
// ]
//
// Calculate totals:
// [Managed over #format_currency(get_total_project_value()) in construction projects]
