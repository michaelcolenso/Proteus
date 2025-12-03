# Achievement Database

## Overview

The Achievement Database is a centralized YAML data store for all quantifiable achievements, metrics, and accomplishments across Michael Colenso's professional career. This system ensures consistency across CV, cover letters, and interview preparation materials.

## Purpose

**Problem Solved**: Maintaining consistent numbers across multiple documents (CV, cover letter, LinkedIn, interview prep notes) is error-prone and time-consuming when updating values manually.

**Solution**: Single source of truth for all quantifiable achievements. Update once, use everywhere.

## Structure

### achievements.yaml

The database contains 27+ achievements organized by:

- **Projects**: Major construction projects with values, sizes, timelines
- **Performance**: Schedule improvements, budget savings, efficiency gains
- **Recognition**: Awards and industry recognition
- **Safety**: Safety records and incident metrics
- **Leadership**: Team sizes and management scope

### Achievement Entry Format

```yaml
achievements:
  - id: unique-identifier        # Unique ID (kebab-case)
    metric: metric_type           # Type of measurement
    value: "$12M"                 # Display value (string)
    value_numeric: 12000000       # Numeric value (for calculations)
    project: "Project Name"       # Associated project (optional)
    company: "Company Name"       # Company (optional)
    year: 2023                    # Year (optional)
    location: "City, State"       # Location (optional)
    category: category_name       # Project category
    tags: [tag1, tag2, tag3]     # Filter tags (array)
```

## Metric Types

| Metric Type | Description | Example Value |
|-------------|-------------|---------------|
| `project_value` | Total project budget/value | "$12M" |
| `unit_count` | Number of residential units | "57 units" |
| `square_footage` | Building size | "35,000 SF" |
| `building_height` | Number of stories | "8 stories" |
| `schedule_performance` | Time saved/gained | "2 months early" |
| `budget_savings` | Cost savings (% or $) | "10%" |
| `change_order_value` | Change order amounts | "$4M+" |
| `safety_incidents` | Safety record | "Zero incidents" |
| `team_size` | Team members managed | "15 direct reports" |
| `award` | Recognition received | "Eagle Award" |
| `process_improvement` | Methodology implementation | "Last Planner System" |

## Tag System

Tags enable filtering achievements for role-specific CVs and reports.

### Role-Based Tags
- `senior-pm` - Senior Project Manager focus
- `superintendent` - Superintendent/field operations
- `estimator` - Estimating/preconstruction
- `lean` - Lean Construction expertise

### Skill-Based Tags
- `budget` - Budget management
- `scheduling` - Schedule management
- `safety` - Safety management
- `leadership` - Team leadership
- `negotiation` - Negotiation skills
- `change-management` - Change order management
- `process-improvement` - Process improvements

### Project-Type Tags
- `multifamily` - Multifamily construction
- `high-rise` - High-rise buildings
- `historic` - Historic renovation
- `luxury` - Luxury residential
- `hospitality` - Hotels/hospitality
- `healthcare` - Healthcare facilities
- `international` - International projects

## Usage

### Command Line Tool

Query and analyze achievements using `scripts/achievements.py`:

```bash
# List all achievements
python3 scripts/achievements.py list

# Filter by tags
python3 scripts/achievements.py list --tags senior-pm multifamily

# Show statistics
python3 scripts/achievements.py stats

# Get specific achievement
python3 scripts/achievements.py get eastlake-value

# Generate report
python3 scripts/achievements.py report --tags superintendent --sort value

# Export to JSON
python3 scripts/achievements.py export --format json --output output.json
```

### Typst Integration

Use helper functions in CV modules (`modules_en/achievement_helpers.typ`):

```typst
// Import helpers
#import "achievement_helpers.typ": get_achievement, format_currency

// Use in CV text
[Managed a #get_achievement("eastlake-value") project]

// Calculate totals
[Over #format_currency(get_total_project_value()) in projects]

// Filter by tags
#let pm_achievements = get_achievements_by_tags(("senior-pm",))
```

## Workflows

### Creating Role-Specific CVs

**Example: Superintendent CV**

1. **Review relevant achievements**:
   ```bash
   python3 scripts/achievements.py report --tags superintendent
   ```

2. **Note key metrics**:
   - Safety records (zero incidents)
   - Project sizes and types
   - Field management experience

3. **Reference in CV module**:
   ```typst
   [Achieved #get_achievement("sts-safety-record") on the #get_achievement("eastlake-value") project]
   ```

4. **Compile variant**:
   ```bash
   ./generate.sh superintendent
   ```

### Adding New Achievements

1. **Determine metric type**: Is it a project value? Team size? Award?

2. **Create unique ID**: Use kebab-case, descriptive (e.g., `new-project-value`)

3. **Add to achievements.yaml**:
   ```yaml
   - id: new-project-value
     metric: project_value
     value: "$25M"
     value_numeric: 25000000
     project: "New Project"
     company: "Company Name"
     year: 2024
     category: multifamily
     tags: [budget, senior-pm, multifamily]
   ```

4. **Verify syntax**:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('data/achievements.yaml'))"
   ```

5. **Reference in CV**: Use `get_achievement("new-project-value")` in Typst files

### Interview Preparation

Generate achievement cheat sheets:

```bash
# All senior PM achievements sorted by value
python3 scripts/achievements.py report --tags senior-pm --sort value > interview_prep.txt

# Export to JSON for custom analysis
python3 scripts/achievements.py export --tags senior-pm --format json > achievements.json
```

## Statistics

Current database statistics (as of 2025-12-03):

- **Total Achievements**: 27
- **Unique Projects**: 10
- **Unique Companies**: 6
- **Year Range**: 2006 - 2023
- **Total Project Value**: $351M

**Top Categories**:
- Mixed-use: 6
- Multifamily: 4
- Senior living: 4
- Historic renovation: 3

**Most Common Tags**:
- senior-pm (27)
- budget (9)
- lean (7)
- multifamily (6)
- superintendent (6)

## Best Practices

### IDs
- Use descriptive, kebab-case IDs: `eastlake-value` not `proj1`
- Include project name or company: `hyatt-lean-implementation`
- Be specific: `alaska-building-eagle-award` not `award1`

### Values
- Always include both `value` (display) and `value_numeric` (calculations)
- Use consistent formatting: "$12M" not "$12,000,000"
- Include units when relevant: "57 units", "8 stories"

### Tags
- Tag comprehensively (all relevant tags)
- Use existing tags when possible
- Add new tags to metadata section if creating categories

### Maintenance
- Update achievements.yaml when numbers change
- Never hardcode metrics in CV files
- Verify YAML syntax after edits
- Recompile all affected CV variants after changes

## Integration with CV Variants

Each CV variant can emphasize different achievements:

- **cv_senior_pm.typ**: Leadership, budget, large projects
- **cv_superintendent.typ**: Safety, field ops, on-site management
- **cv_estimator.typ**: Preconstruction, estimating, buyout
- **cv_exec_summary.typ**: Top 3-5 achievements only

Filter achievements by tags to automatically generate variant-appropriate content.

## Testing

Test Typst integration:

```bash
# Compile test file
typst compile test_achievements.typ

# Should display all achievement values without errors
```

Test Python script:

```bash
# Run all commands
python3 scripts/achievements.py stats
python3 scripts/achievements.py list --tags senior-pm
python3 scripts/achievements.py get eastlake-value
```

## Future Enhancements

Potential additions:
- Achievement templates for common metric types
- Auto-sync with LinkedIn profile
- Integration with job application tracker
- Achievement timeline visualization
- Comparative analysis across companies/years

## Support

For questions or issues:
1. Check YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('data/achievements.yaml'))"`
2. Review this README
3. Consult main repository documentation (README.md, CLAUDE.md)

---

**Version**: 1.0
**Last Updated**: 2025-12-03
**Maintained By**: Achievement Database System
