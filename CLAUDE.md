# CLAUDE.md - AI Assistant Guide

## Repository Overview

This is a **professional CV and cover letter system** built with [Typst](https://typst.app/), a modern typesetting system. The repository uses the [brilliant-cv](https://typst.app/universe/package/brilliant-cv) template (v2.0.3) to generate polished PDF documents for a Construction Project Manager.

**Purpose**: Generate professional, ATS-optimized CV and cover letter documents from modular Typst source files with centralized configuration.

**Owner**: Michael Colenso, Construction Project Manager

## Technology Stack

- **Typst**: Modern typesetting system (alternative to LaTeX)
- **brilliant-cv v2.0.3**: CV template package from Typst Universe
- **TOML**: Configuration file format for metadata
- **Font Awesome 6**: Icon fonts for visual elements
- **Custom Fonts**: Source Sans Pro, Source Sans 3, Roboto

## Project Structure

```
brilliantmikecv/
├── cv.typ                      # Main CV entry point - imports modules
├── cv_senior_pm.typ            # Senior PM variant (leadership focus)
├── cv_superintendent.typ       # Superintendent variant (field focus)
├── cv_estimator.typ            # Estimator variant (preconstruction focus)
├── cv_exec_summary.typ         # One-page executive summary
├── letter.typ                  # Main cover letter template
├── metadata.toml               # Central configuration (personal info, layout, colors, keywords)
├── generate.sh                 # Quick build script for all variants
│
├── modules_en/                 # English CV content modules
│   ├── education.typ           # Education history
│   ├── professional.typ        # Full professional experience
│   ├── professional_one_page.typ # Condensed one-page version
│   ├── projects.typ            # Selected projects showcase
│   ├── portfolio_projects.typ  # Detailed project descriptions (LinkedIn/portfolio)
│   ├── skills.typ              # Technical/professional skills (ATS-optimized)
│   ├── certificates.typ        # Certifications and training
│   ├── references.typ          # References available statement
│   ├── exec_summary.typ        # Executive summary for one-page CV
│   ├── publications.typ        # Publications/bibliography
│   └── temp.typ                # Temporary/scratch file (empty)
│
├── letters/                    # Cover letter templates
│   ├── README.md               # Letter templates documentation
│   ├── senior_pm.typ           # Senior PM cover letter template
│   ├── multifamily.typ         # Multifamily construction template
│   └── lean_construction.typ   # Lean construction specialist template
│
├── applications/               # Job application tracking
│   ├── README.md               # Application tracking guide
│   ├── tracker.md              # Main application tracking table
│   └── responses/              # Interview prep and follow-up notes
│
├── src/                        # Asset directory
│   ├── avatar.png              # Profile photo (693KB)
│   ├── signature.png           # Signature for cover letter (145KB)
│   ├── publications.bib        # BibTeX bibliography file
│   └── logos/                  # Organization logos
│       ├── abc_company.png
│       ├── pqr_corp.png
│       ├── ucla.png
│       └── xyz_corp.png
│
├── otfs/                       # Font Awesome font files (gitignored)
│   ├── Font Awesome 6 Brands-Regular-400.otf
│   ├── Font Awesome 6 Free-Regular-400.otf
│   └── Font Awesome 6 Free-Solid-900.otf
│
├── cv.pdf                      # Compiled CV output (330KB)
├── letter.pdf                  # Compiled cover letter output (162KB)
├── README.md                   # User documentation
├── CLAUDE.md                   # AI assistant guide (this file)
└── .gitignore                  # Git exclusions
```

## Key Files and Their Roles

### Critical Configuration Files

**metadata.toml** - Central configuration hub
- Personal information (name, contact details)
- Layout settings (colors, spacing, fonts)
- ATS optimization (keyword injection, AI prompts)
- Multi-language support (en, fr, zh)
- Header quotes and footer text

**cv.typ** - Main CV orchestrator
- Imports brilliant-cv package
- Loads metadata.toml
- Defines module import function
- Lists active modules to include
- Controls profile photo display

**letter.typ** - Cover letter generator
- Imports brilliant-cv letter template
- Configures recipient and sender addresses
- Includes signature image
- Contains letter body text

### Content Modules (modules_en/)

All modules follow this pattern:
```typst
// Standard module structure
#import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Section Title")

#cvEntry(
  title: [Position/Title],
  society: [Organization Name],
  logo: image("../src/logos/company.png"),  // Optional
  date: [Date Range],
  location: [City, State],
  description: list(
    [Achievement or responsibility 1],
    [Achievement or responsibility 2]
  ),
  tags: ("Tag1", "Tag2", "Tag3")
)
```

## Development Workflows

### Building Documents

#### Quick Build with generate.sh Script

The repository includes a convenient build script for all CV variants:

```bash
# Generate specific CV variant
./generate.sh senior-pm          # Senior PM focused CV
./generate.sh superintendent     # Superintendent focused CV
./generate.sh estimator          # Estimator/Preconstruction CV
./generate.sh exec-summary       # One-page executive summary
./generate.sh standard           # Standard full CV
./generate.sh letter             # Cover letter

# Generate all variants at once
./generate.sh all

# Watch mode (auto-recompile on file changes)
./generate.sh watch senior-pm

# Clean all compiled PDFs
./generate.sh clean

# Show help
./generate.sh help
```

#### Manual Compilation

```bash
# Compile specific CV variant
typst compile cv_senior_pm.typ
typst compile cv_superintendent.typ
typst compile cv_estimator.typ
typst compile cv_exec_summary.typ

# Compile standard CV
typst compile cv.typ

# Compile cover letter
typst compile letter.typ

# Watch mode (auto-recompile on changes)
typst watch cv_senior_pm.typ
```

### CV Variants System

This repository includes multiple CV variants tailored for different job applications:

#### Available Variants

**cv_senior_pm.typ** - Senior Project Manager
- **Emphasis**: Leadership, P&L management, large projects ($12M-$200M)
- **Target Roles**: Senior PM, Project Executive, Construction Manager
- **Modules**: professional, projects, skills, education, certificates
- **Best For**: Leadership positions with budget accountability

**cv_superintendent.typ** - Superintendent / Field Operations
- **Emphasis**: On-site management, safety, trade coordination
- **Target Roles**: Superintendent, Senior Superintendent, Field Manager
- **Modules**: professional, projects, skills, certificates, education
- **Best For**: Field-focused positions emphasizing safety and operations

**cv_estimator.typ** - Estimator / Preconstruction Manager
- **Emphasis**: Estimating, value engineering, preconstruction, buyout
- **Target Roles**: Estimator, Senior Estimator, Preconstruction Manager
- **Modules**: professional, projects, skills, education, certificates
- **Best For**: Preconstruction and estimating positions

**cv_exec_summary.typ** - One-Page Executive Summary
- **Emphasis**: Quick overview with key highlights
- **Target Roles**: Any (for initial contact/networking)
- **Modules**: exec_summary, education
- **Best For**: Networking events, recruiter emails, quick applications

**cv.typ** - Standard Full CV
- **Emphasis**: Comprehensive professional history
- **Target Roles**: General applications
- **Modules**: education, professional, projects (skills commented out)
- **Best For**: When comprehensive detail is needed

#### Using CV Variants

**Workflow for job applications**:

1. **Identify target role type** (Senior PM, Superintendent, Estimator, etc.)
2. **Select appropriate CV variant** from list above
3. **Customize keywords** in metadata.toml if needed (see Keyword Optimization below)
4. **Select matching cover letter template** from letters/ directory
5. **Generate documents**:
   ```bash
   ./generate.sh senior-pm    # Compiles cv_senior_pm.pdf
   cp letters/senior_pm.typ letter.typ
   # Edit letter.typ with company-specific details
   ./generate.sh letter
   ```
6. **Track application** in applications/tracker.md

### Cover Letter Template System

The `letters/` directory contains targeted cover letter templates for different construction roles:

#### Available Templates

- **senior_pm.typ** - Senior PM roles emphasizing leadership and P&L management
- **multifamily.typ** - Multifamily/apartment construction focused positions
- **lean_construction.typ** - Roles focused on Lean Construction implementation

#### Using Cover Letter Templates

```bash
# 1. Copy appropriate template to root directory
cp letters/senior_pm.typ letter.typ

# 2. Customize placeholders in letter.typ
# - [Company Name]
# - [Position Title]
# - [Hiring Manager Name]
# - [Company Address]
# - [specific reason for interest]

# 3. Compile
./generate.sh letter
# or
typst compile letter.typ
```

#### Creating Custom Letters

For specific applications, create dated versions:

```bash
# Copy base template
cp letters/multifamily.typ letters/2025-01-15_turner-construction.typ

# Customize for specific company
# Save in letters/ directory for version control
```

### Application Tracking System

The `applications/` directory provides a structured system for tracking all job applications:

#### tracker.md
Markdown table tracking all applications with:
- Date applied
- Company name
- Position title
- CV variant used
- Cover letter template used
- Current status
- Next action/follow-up date

#### Individual Application Files
Create `applications/YYYY-MM-DD_company-name.md` for each application with:
- Job posting details and URL
- Company research notes
- Why you're interested
- Key talking points for interviews
- Customizations made to CV/cover letter

#### responses/ Directory
Store interview prep notes, thank you emails, and follow-up communications

#### Example Workflow

```bash
# 1. Create application file
echo "# ABC Construction - Senior PM" > applications/2025-01-15_abc-construction.md

# 2. Add company research and job requirements to file

# 3. Generate appropriate CV
./generate.sh senior-pm

# 4. Customize cover letter
cp letters/senior_pm.typ letter.typ
# Edit with company specifics
./generate.sh letter

# 5. Update applications/tracker.md with new row

# 6. Submit application

# 7. Create interview prep notes if contacted
# applications/responses/abc-construction-interview-prep.md
```

### Keyword Optimization

The metadata.toml file includes keyword optimization profiles for different role types. These help with ATS (Applicant Tracking System) parsing.

#### Available Keyword Profiles

Located in metadata.toml:
- `[keywords.senior_pm]` - Senior PM keywords
- `[keywords.superintendent]` - Superintendent keywords
- `[keywords.estimator]` - Estimator keywords
- `[keywords.lean_specialist]` - Lean Construction keywords
- `[keywords.multifamily]` - Multifamily construction keywords
- `[keywords.luxury_residential]` - Luxury residential keywords

#### Using Keyword Profiles

1. **Identify target role type**
2. **Find matching profile** in metadata.toml
3. **Copy keywords** from the profile
4. **Update `[inject] injected_keywords_list`** section with selected keywords
5. **Recompile** CV

**Example**:
```toml
[inject]
    inject_keywords = true
    # Copy from [keywords.senior_pm] profile
    injected_keywords_list = [
        "Senior Project Manager",
        "P&L Management",
        "Team Leadership",
        "Multifamily",
        "Seattle"
    ]
```

### Common Modifications

#### 1. Adding a New Job Entry

**File**: `modules_en/professional.typ`

1. Locate the appropriate position in the chronological list
2. Add new `#cvEntry()` block following the existing pattern
3. Include all required fields: title, society, date, location, description, tags
4. Recompile: `typst compile cv.typ`

#### 2. Updating Personal Information

**File**: `metadata.toml`

Edit the `[personal]` section:
```toml
[personal]
    first_name = "Michael"
    last_name = "Colenso"

    [personal.info]
        phone = "my_phone"
        email = "my_email"
```

#### 3. Changing Color Scheme

**File**: `metadata.toml`

```toml
[layout]
    # Preset options: skyblue, red, nephritis, concrete, darknight
    awesome_color = "darknight"

    # Or custom hex:
    awesome_color = "#1E90FF"
```

#### 4. Adding/Removing Modules

**File**: `cv.typ`

Modify the `#importModules()` call:
```typst
#importModules((
    "education",
    "professional",
    "projects",
    // "skills"  // Commented out = not included
))
```

#### 5. Creating Multi-Version CVs

**Strategy**: Create separate entry point files:
- `cv_full.typ` - Complete version with all modules
- `cv_onepage.typ` - Condensed version with `professional_one_page`
- `cv_technical.typ` - Emphasizing technical skills

Each can import different module combinations.

### Testing Changes

1. **Compile and verify**: `typst compile cv.typ`
2. **Check output**: Open `cv.pdf` in a PDF viewer
3. **Verify formatting**: Ensure spacing, alignment, and page breaks are correct
4. **Test ATS compatibility**: Use an ATS testing tool if making structural changes

## AI Assistant Guidelines

### When Modifying Content

1. **ALWAYS read files before editing** - Use the Read tool first
2. **Preserve exact formatting** - Maintain indentation, brackets, and Typst syntax
3. **Follow existing patterns** - Match the structure of existing entries
4. **Test compilation** - Run `typst compile cv.typ` after changes
5. **Respect chronological order** - Keep entries in reverse chronological order (newest first)

### Content Entry Best Practices

**Description bullets should**:
- Start with action verbs (Led, Managed, Developed, Implemented)
- Be concise (1-2 lines each)
- Quantify achievements where possible ($12M project, 57 units, 8 stories)
- Focus on outcomes and impact

**Tags should**:
- Be relevant keywords for ATS optimization
- Match industry terminology
- Include technical skills and project types
- Be enclosed in parentheses as a tuple: `("Tag1", "Tag2", "Tag3")`

### File Organization Rules

**DO**:
- Keep all English content in `modules_en/`
- Place images in `src/` directory
- Place logos in `src/logos/`
- Use relative paths from the file location (`../src/logos/company.png`)
- Comment out entries rather than deleting (for version control)

**DON'T**:
- Modify the brilliant-cv package import version without testing
- Change the module import function in `cv.typ`
- Edit compiled PDFs directly
- Hardcode personal information in module files (use metadata.toml)

### Common Typst Syntax

```typst
// Comments
// Single line comment

// Text formatting
[Regular text]
*Bold text*
_Italic text_
`Code text`

// Lists
list(
  [Item 1],
  [Item 2],
  [Item 3]
)

// Line breaks and spacing
#pagebreak()     // Force new page
#colbreak()      // Break to next column
#columns[...]    // Multi-column layout

// Conditionals
#if condition [
  // Content
]

// Images
image("path/to/image.png")

// Variables
#let variableName = value
```

### Handling Sensitive Information

The current repository uses placeholders:
- `my_phone` - Phone number placeholder
- `my_email` - Email placeholder
- `my_location` - Location placeholder

**When assisting with real deployments**:
- Advise using environment variables or separate config files
- Never commit real contact information to public repositories
- Consider using `.env` files (already in `.gitignore`)

## ATS Optimization Features

### Keyword Injection

**Location**: `metadata.toml`

```toml
[inject]
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

**Purpose**: Helps ATS systems identify relevant keywords. The brilliant-cv template can inject these invisibly into the PDF for parsing.

### AI Prompt Injection

```toml
[inject]
    inject_ai_prompt = true
```

**Purpose**: Embeds hidden prompts for AI-based ATS systems to better understand the CV context.

## Multi-Language Support

The system supports multiple languages through:

1. **Language-specific module folders**: `modules_en/`, `modules_fr/`, `modules_zh/`
2. **Language setting**: `language = "en"` in `metadata.toml`
3. **Localized strings**: `[lang.en]`, `[lang.fr]`, `[lang.zh]` sections

**To add a new language**:
1. Create folder: `modules_XX/` (where XX is language code)
2. Translate all module files
3. Add `[lang.XX]` section to `metadata.toml`
4. Set `language = "XX"` to activate

## Layout Customization

### Spacing Controls

**File**: `metadata.toml`

```toml
[layout]
    before_section_skip = "5pt"           # Space above section headers
    before_entry_skip = "1pt"             # Space above each entry
    before_entry_description_skip = "1pt" # Space above descriptions
```

**Units**: Typst uses points (pt), similar to CSS

### Font Configuration

```toml
[layout.fonts]
    regular_fonts = ["Source Sans Pro", "Source Sans 3"]
    header_font = "Roboto"
```

**Font loading order**:
1. System fonts (if installed)
2. Fonts in `otfs/` directory
3. Fallback to default if not found

### Header Customization

```toml
[layout.header]
    header_align = "left"  # Options: left, center, right
    display_profile_photo = false
```

### Entry Display Options

```toml
[layout.entry]
    display_entry_society_first = false  # false = job title bolded, true = company bolded
    display_logo = false                 # Show/hide organization logos
```

## Version Control Practices

### Current Git Branch

The repository uses feature branches for development:
- Branch pattern: `claude/claude-md-*` (session-specific)
- Main branch: (default)

### Commit Message Style

Based on recent commits:
```
Merge pull request #1 from michaelcolenso/...
Add comprehensive documentation for Typst CV
add gitignore
initial commit
```

**Recommended style**:
- Use descriptive present tense ("Add", "Update", "Fix")
- Reference specific changes
- Keep under 72 characters for first line

### Files in .gitignore

```
node_modules/     # Not used in this project (legacy)
otfs/             # Font files (too large, should be installed separately)
*.log
.env              # Environment variables
dist/
build/
.DS_Store         # macOS
Thumbs.db         # Windows
.vscode/          # IDE settings
.idea/
```

**Note**: Compiled PDFs (cv.pdf, letter.pdf) are currently committed. Consider adding to .gitignore for cleaner version control.

## Troubleshooting Guide

### Compilation Errors

**Symptom**: `typst compile cv.typ` fails

**Common causes**:
1. **Missing fonts** - Install Source Sans Pro and Roboto, or update `metadata.toml`
2. **Syntax errors** - Check for unmatched brackets `[ ]` or parentheses `( )`
3. **Missing files** - Verify all modules in `#importModules()` exist
4. **Wrong working directory** - Must run from repository root

**Debug command**:
```bash
typst compile cv.typ --verbose
```

### Module Not Loading

**Symptom**: Module content doesn't appear in PDF

**Checklist**:
- Module filename matches the name in `#importModules()`
- File exists in correct language folder (e.g., `modules_en/`)
- `language` setting in `metadata.toml` matches folder suffix
- Module file has correct imports and structure

### Image Not Displaying

**Symptom**: Logo or photo missing from PDF

**Checklist**:
- Image file exists at specified path
- Path is relative to the module file location (`../src/logos/company.png`)
- Image format is supported (PNG, JPEG, SVG)
- `display_logo = true` or `display_profile_photo = true` if applicable

### Spacing Issues

**Symptom**: Content too cramped or too spread out

**Solutions**:
1. Adjust spacing in `metadata.toml` (before_section_skip, etc.)
2. Use `#pagebreak()` to force new pages
3. Use `#columns[...]` for multi-column layouts
4. Check for extra blank lines in module files

## Advanced Features

### Two-Column Layouts

Used in `professional.typ` and `projects.typ`:

```typst
#columns[
  #cvEntry(...)
  #cvEntry(...)

  #colbreak()  // Force column break

  #cvEntry(...)
  #cvEntry(...)
]
```

**Benefits**: Fits more content, better space utilization

### Conditional Content Display

**Pattern**: Comment out entries to exclude without deleting

```typst
// #cvEntry(
//   title: [Outdated Position],
//   ...
// )
```

**Use cases**:
- Tailoring CV for specific job applications
- Maintaining history without displaying
- A/B testing different content versions

### Custom Icons

The template uses Font Awesome 6:

```toml
[personal.info.custom-1]
    awesomeIcon = "home"  # See https://fontawesome.com/icons
    text = "my_location"
    link = "https://www.nmu.edu"
```

**Icon examples**: "phone", "envelope", "linkedin", "github", "globe"

## Performance Considerations

### Compilation Speed

**Current state**: Compiles in ~1-2 seconds on modern hardware

**Optimization tips**:
- Use `typst watch` for incremental compilation during development
- Avoid excessive image sizes (current images are reasonably sized)
- Comment out unused modules during development

### PDF Size

**Current outputs**:
- `cv.pdf`: 330KB
- `letter.pdf`: 162KB

**To reduce size**:
- Compress images before adding to `src/`
- Avoid embedding large logos
- Set `display_logo = false` if not needed

## Security and Privacy

### Sensitive Data Handling

**Current placeholders in metadata.toml**:
- Phone: `my_phone`
- Email: `my_email`
- Location: `my_location`

**Recommendations for AI assistants**:
1. Never expose real contact information in logs or outputs
2. Suggest using environment variables for production
3. Advise keeping real data in local-only config files
4. Recommend separate branches for public vs. private versions

### Image Privacy

**Avatar and signature**: Currently committed to repository
- `src/avatar.png` (693KB)
- `src/signature.png` (145KB)

**Recommendation**: For public repositories, use placeholder images or add to .gitignore

## Extension Points

### Adding New Section Types

**Example**: Adding a "Volunteer Experience" section

1. Create `modules_en/volunteer.typ`:
```typst
#import "@preview/brilliant-cv:2.0.3": cvSection, cvEntry
#let metadata = toml("../metadata.toml")
#let cvSection = cvSection.with(metadata: metadata)
#let cvEntry = cvEntry.with(metadata: metadata)

#cvSection("Volunteer Experience")

#cvEntry(
  title: [Role],
  society: [Organization],
  date: [2020 - 2022],
  location: [City, State],
  description: list(
    [Contribution 1],
    [Contribution 2]
  ),
  tags: ("Volunteering", "Community")
)
```

2. Add to `cv.typ`:
```typst
#importModules((
  "education",
  "professional",
  "volunteer"  // New module
))
```

### Custom Components

The brilliant-cv package provides:
- `cvSection()` - Section headers
- `cvEntry()` - Main entry type
- `hBar()` - Horizontal separator

**See**: [brilliant-cv documentation](https://typst.app/universe/package/brilliant-cv) for more components

### Bibliography Integration

**File**: `src/publications.bib`

Used in `publications.typ` module for academic citations. The brilliant-cv template can format bibliography entries automatically.

## AI Assistant Workflow Checklist

When asked to modify this CV:

- [ ] Read relevant files before making changes
- [ ] Understand the user's goal (new job? different industry? length requirements?)
- [ ] Identify which modules need modification
- [ ] Preserve existing formatting and structure
- [ ] Follow the established content patterns (action verbs, quantification)
- [ ] Update ATS keywords if role/industry changed
- [ ] Test compilation: `typst compile cv.typ`
- [ ] Verify output PDF looks correct
- [ ] Commit changes with descriptive message
- [ ] Push to correct branch (claude/* pattern)

## Resources and References

### Documentation
- [Typst Official Docs](https://typst.app/docs)
- [brilliant-cv Package](https://typst.app/universe/package/brilliant-cv)
- [Typst Universe](https://typst.app/universe) - Package repository
- [Font Awesome Icons](https://fontawesome.com/icons)

### Related Files
- `README.md` - User-facing documentation (comprehensive)
- `metadata.toml` - Central configuration
- `.gitignore` - Version control exclusions

### Support
- Typst Community: https://discord.gg/typst
- brilliant-cv GitHub: https://github.com/mintyfrankie/brilliant-CV

---

**Document Version**: 1.0
**Last Updated**: 2025-11-18
**Maintained For**: AI assistants working with the brilliantmikecv repository
**Repository Owner**: Michael Colenso (michaelcolenso/brilliantmikecv)
