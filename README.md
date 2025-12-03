# Michael Colenso CV - Typst Documentation

A professional CV and cover letter built with [Typst](https://typst.app/) using the [brilliant-cv](https://typst.app/universe/package/brilliant-cv) template (v2.0.3).

## Overview

This repository contains a modular CV system that generates professional PDF documents for a Construction Project Manager. The CV is designed to be easily customizable, maintainable, and supports multiple languages.

## Project Structure

```
.
├── cv.typ                    # Main CV entry point
├── letter.typ                # Cover letter template
├── metadata.toml             # Central configuration file
├── generate.sh               # Build script for all CV variants
├── modules_en/               # English CV sections
│   ├── education.typ
│   ├── professional.typ
│   ├── projects.typ
│   ├── skills.typ
│   ├── certificates.typ
│   ├── publications.typ
│   └── achievement_helpers.typ  # Achievement database integration
├── data/                     # Achievement database
│   └── achievements.yaml     # Centralized metrics and accomplishments
├── scripts/                  # Utility scripts
│   └── achievements.py       # Achievement database CLI tool
├── src/                      # Assets directory
│   ├── avatar.png           # Profile photo
│   ├── signature.png        # Signature for cover letter
│   ├── logos/               # Company/organization logos
│   └── publications.bib     # Bibliography file
├── letters/                  # Cover letter templates
│   ├── senior_pm.typ
│   ├── multifamily.typ
│   └── lean_construction.typ
├── applications/             # Job application tracking
│   ├── tracker.md
│   └── responses/
└── otfs/                     # Custom font files

Generated outputs:
├── cv.pdf                    # Compiled CV
├── cv_senior_pm.pdf         # Senior PM variant
├── cv_superintendent.pdf    # Superintendent variant
├── cv_estimator.pdf         # Estimator variant
├── cv_exec_summary.pdf      # One-page executive summary
└── letter.pdf               # Compiled cover letter
```

## Quick Start

### Prerequisites

1. Install [Typst](https://github.com/typst/typst):
   ```bash
   # macOS
   brew install typst

   # Linux
   cargo install --git https://github.com/typst/typst

   # Or download from https://github.com/typst/typst/releases
   ```

### Building the CV

```bash
# Compile CV
typst compile cv.typ

# Compile cover letter
typst compile letter.typ

# Watch mode (auto-recompile on changes)
typst watch cv.typ
```

## Configuration

### metadata.toml

The `metadata.toml` file is the central configuration hub. Key sections:

#### Personal Information
```toml
[personal]
    first_name = "Michael"
    last_name = "Colenso"

    [personal.info]
        phone = "my_phone"
        email = "my_email"
```

#### Layout Customization
```toml
[layout]
    # Color scheme options: skyblue, red, nephritis, concrete, darknight
    # Or use custom hex color: "#1E90FF"
    awesome_color = "darknight"

    # Spacing controls
    before_section_skip = "5pt"
    before_entry_skip = "1pt"
    before_entry_description_skip = "1pt"

    [layout.fonts]
        regular_fonts = ["Source Sans Pro", "Source Sans 3"]
        header_font = "Roboto"

    [layout.header]
        header_align = "left"  # Options: left, center, right
        display_profile_photo = false

    [layout.entry]
        # Bold company name vs position title
        display_entry_society_first = false
        display_logo = false
```

#### ATS Optimization
```toml
[inject]
    # Inject hidden AI prompts for ATS systems
    inject_ai_prompt = true

    # Inject keywords for ATS parsing
    inject_keywords = true
    injected_keywords_list = [
        "Construction Project Manager",
        "Lean Construction",
        "Multifamily",
        "High-Rise",
        "Historic Renovation",
        "Seattle"
    ]
```

#### Multi-language Support
```toml
language = "en"  # Must match folder suffix (modules_en, modules_zh, etc.)

[lang.en]
    header_quote = "Dynamic Construction Project Manager..."
    cv_footer = "Construction Project Manager"
    letter_footer = "Construction Project Manager"

[lang.fr]
    header_quote = "Chef de projet..."
    cv_footer = "Résumé"
    letter_footer = "Lettre de motivation"
```

## Module System

### Creating a New Section

1. Create a new `.typ` file in `modules_en/` (e.g., `certifications.typ`)
2. Use the standard module structure:

```typst
// Imports
#import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Certifications")

#cvEntry(
  title: [Certification Name],
  society: [Issuing Organization],
  logo: image("../src/logos/org.png"),  // Optional
  date: [2024],
  location: [Location],
  description: list(
    [Description point 1],
    [Description point 2]
  ),
  tags: ("Tag1", "Tag2", "Tag3")
)
```

3. Add the module to `cv.typ`:

```typst
#importModules((
  "education",
  "professional",
  "projects",
  "certifications"  // Add your new module
))
```

### Module Components

#### cvEntry Parameters
- `title`: Position/role/item name
- `society`: Company/organization name
- `logo`: Optional logo image
- `date`: Time period (e.g., "2020 - 2024")
- `location`: Geographic location
- `description`: List of bullet points describing responsibilities/achievements
- `tags`: Tuple of skill tags for the entry

#### Formatting Tips
- Use `list()` for bullet points
- Wrap text in brackets `[text]` for Typst markup
- Use `none` to omit optional fields
- Add `#pagebreak()` for pagination control
- Use `#columns[]` for multi-column layouts
- Use `#colbreak()` to break between columns

## Achievement Database

### Overview

The Achievement Database is a centralized YAML data store for all quantifiable achievements, metrics, and accomplishments across your career. This ensures consistency across your CV, cover letters, and interview preparation materials.

**Benefits**:
- **Consistency**: Same numbers everywhere (CV, cover letter, LinkedIn, interviews)
- **Easy Updates**: Change a value once, updates everywhere it's used
- **Variant Generation**: Filter achievements by tags for role-specific CVs
- **Analytics**: Track which achievements appear in successful applications
- **Interview Prep**: Quick reference for your key metrics

### Structure

The database is located in `data/achievements.yaml` and contains structured achievement entries:

```yaml
achievements:
  - id: eastlake-value
    metric: project_value
    value: "$12M"
    value_numeric: 12000000
    project: "2210 Eastlake"
    company: "STS Construction"
    year: 2023
    location: "Seattle, WA"
    category: multifamily
    tags: [budget, senior-pm, multifamily, superintendent]
```

### Using the Achievement Script

The `scripts/achievements.py` tool provides powerful querying and reporting:

```bash
# List all achievements
python3 scripts/achievements.py list

# Filter by tags (for CV variants)
python3 scripts/achievements.py list --tags senior-pm multifamily

# Show database statistics
python3 scripts/achievements.py stats

# Get specific achievement by ID
python3 scripts/achievements.py get eastlake-value

# Generate detailed report
python3 scripts/achievements.py report --tags senior-pm --sort value

# Export to JSON
python3 scripts/achievements.py export --format json --output achievements.json
```

### Integrating Achievements in Typst

Use the helper functions in `modules_en/achievement_helpers.typ`:

```typst
// Import the helpers
#import "achievement_helpers.typ": get_achievement, get_achievement_numeric

// Simple value retrieval
[Managed a #get_achievement("eastlake-value") project with #get_achievement("eastlake-units")]
// Output: "Managed a $12M project with 57 units"

// Get all achievements for a project
#let eastlake = get_project_achievements("2210 Eastlake")

// Filter by tags for CV variants
#let senior_pm_achievements = get_achievements_by_tags(("senior-pm", "budget"))

// Calculate totals
[Managed over #format_currency(get_total_project_value()) in projects]
// Output: "Managed over $351M in projects"
```

### Available Helper Functions

- `get_achievement(id)` - Get value string by ID
- `get_achievement_numeric(id)` - Get numeric value for calculations
- `get_project_achievements(project_name)` - All achievements for a project
- `get_company_achievements(company_name)` - All achievements for a company
- `get_achievements_by_tags(tags)` - Filter by tags
- `get_total_project_value()` - Sum all project values
- `format_currency(amount)` - Format numbers as currency ($12M, $351M, etc.)

### Achievement Metrics

Common metric types in the database:
- `project_value` - Total project budget/value
- `unit_count` - Number of units (multifamily)
- `square_footage` - Building size
- `building_height` - Number of stories
- `schedule_performance` - Time saved/gained
- `budget_savings` - Percentage or dollar savings
- `change_order_value` - Change order amounts
- `safety_incidents` - Safety record
- `team_size` - Team members managed
- `award` - Recognition and awards

### Filtering by Tags

Achievements are tagged for easy filtering:

**Role-based tags**: `senior-pm`, `superintendent`, `estimator`, `lean`

**Skill-based tags**: `budget`, `scheduling`, `safety`, `leadership`, `negotiation`

**Project-type tags**: `multifamily`, `high-rise`, `historic`, `luxury`, `hospitality`

Example workflow for creating a Superintendent-focused CV:
```bash
# See all superintendent achievements
python3 scripts/achievements.py report --tags superintendent

# Export for reference
python3 scripts/achievements.py export --tags superintendent --output superintendent_achievements.json
```

### Adding New Achievements

1. Open `data/achievements.yaml`
2. Add a new achievement following the existing pattern:
```yaml
  - id: new-project-value
    metric: project_value
    value: "$25M"
    value_numeric: 25000000
    project: "New Project Name"
    company: "Company Name"
    year: 2024
    location: "City, State"
    category: multifamily
    tags: [budget, senior-pm, multifamily]
```
3. Reference it in your Typst modules using `get_achievement("new-project-value")`

### Best Practices

1. **Use unique, descriptive IDs**: `eastlake-value` not `project1`
2. **Always include both value and value_numeric**: Allows display and calculations
3. **Tag appropriately**: Makes filtering for CV variants easy
4. **Be specific with projects/companies**: Helps with filtering and reporting
5. **Update centrally**: Never hardcode numbers in CV modules—always use the database

## Customization Guide

### Changing Colors

Edit `metadata.toml`:
```toml
[layout]
    awesome_color = "#1E90FF"  # Custom hex color
    # or
    awesome_color = "skyblue"   # Preset color
```

Available presets: `skyblue`, `red`, `nephritis`, `concrete`, `darknight`

### Adding a Profile Photo

1. Place your photo in `src/` directory
2. Update `metadata.toml`:
```toml
[layout.header]
    display_profile_photo = true
```
3. Update `cv.typ`:
```typst
#show: cv.with(
  metadata,
  profilePhoto: image("src/avatar.png"),
)
```

### Modifying the Header Quote

Edit `metadata.toml`:
```toml
[lang.en]
    header_quote = "Your professional summary here..."
```

### Adjusting Spacing

Fine-tune spacing in `metadata.toml`:
```toml
[layout]
    before_section_skip = "5pt"      # Space before section headers
    before_entry_skip = "1pt"         # Space before each entry
    before_entry_description_skip = "1pt"  # Space before descriptions
```

## Cover Letter

The `letter.typ` file generates a professional cover letter using the same styling as the CV.

### Customizing the Letter

Edit `letter.typ`:
```typst
#show: letter.with(
  metadata,
  myAddress: "Your Address Here",
  recipientName: "Company Name Here",
  recipientAddress: "Company Address Here",
  date: datetime.today().display(),
  subject: "Subject: Application for [Position]",
  signature: image("src/signature.png"),
)

// Add your letter content here
Dear Hiring Manager,

[Your letter content]

Sincerely,
```

## Best Practices

### ATS Optimization
- Use the `inject_keywords` feature in `metadata.toml`
- Include relevant industry keywords in your `injected_keywords_list`
- Keep formatting clean and simple
- Use standard section headers

### Content Organization
- Keep descriptions concise (2-4 bullet points per entry)
- Use action verbs at the start of bullet points
- Quantify achievements where possible
- Prioritize recent and relevant experience

### Version Control
- Commit `metadata.toml` changes with clear messages
- Use branches for different job applications
- Keep compiled PDFs in `.gitignore` if desired

### Multi-version CVs
Create different versions for different purposes:
```typst
// cv_full.typ - Full detailed version
#importModules((
  "education",
  "professional",
  "projects",
  "skills",
  "publications",
  "certificates"
))

// cv_onepage.typ - Condensed version
#importModules((
  "education",
  "professional_one_page"
))
```

## Troubleshooting

### Fonts Not Found
If you get font errors:
1. Check that fonts are installed on your system
2. Or place font files in the `otfs/` directory
3. Update font references in `metadata.toml`

### Compilation Errors
```bash
# Verbose output for debugging
typst compile cv.typ --verbose

# Check Typst version
typst --version
```

### Module Not Loading
- Verify file exists in `modules_en/` (or your language folder)
- Check module name in `#importModules()` matches filename
- Ensure language setting in `metadata.toml` matches folder suffix

## Advanced Features

### Multi-column Layouts
Use in module files for space efficiency:
```typst
#columns[
  #cvEntry(...)
  #colbreak()
  #cvEntry(...)
]
```

### Conditional Content
Show/hide content based on context:
```typst
// Comment out entries to exclude them
// #cvEntry(
//   title: [Hidden Entry],
//   ...
// )
```

### Custom Sections
The brilliant-cv template supports various section types:
- `cvSection()` - Standard section header
- `cvEntry()` - Job/education entries with full details
- `hBar()` - Horizontal separator bar

## Resources

- [Typst Documentation](https://typst.app/docs)
- [Brilliant CV Template](https://typst.app/universe/package/brilliant-cv)
- [Typst Universe](https://typst.app/universe) - More templates and packages
- [FontAwesome Icons](https://fontawesome.com/icons) - For custom icons

## License

This CV template uses the brilliant-cv package. Check the [brilliant-cv repository](https://github.com/mintyfrankie/brilliant-CV) for license information.

## Author

**Michael Colenso**
Construction Project Manager

---

*Built with Typst - A modern alternative to LaTeX*
