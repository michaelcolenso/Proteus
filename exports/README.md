# CV Export Formats

This directory contains CV exports in multiple formats for different use cases.

## Overview

The Multi-Format Export Pipeline converts your Typst-compiled CV into various formats optimized for different submission methods and platforms.

## Available Formats

| Format | File Extension | Use Case | Tools Required |
|--------|----------------|----------|----------------|
| **PDF** | `.pdf` | Standard applications, printing | typst |
| **Plain Text** | `.txt` | Online application forms, paste-in fields | typst, pdftotext |
| **Markdown** | `.md` | GitHub, LinkedIn, easy editing | typst, pandoc (or pdftotext) |
| **HTML** | `.html` | Portfolio websites, online hosting | typst, pandoc (or pdftotext) |

## Quick Start

### Export Single Variant

```bash
# Export to all formats
./generate.sh export senior-pm all

# Export to specific formats
./generate.sh export senior-pm txt html md

# Export superintendent CV as markdown
./generate.sh export superintendent md
```

### Export All Variants

```bash
# Export all CV variants to all formats
./generate.sh export-all all

# Export all variants to text only
./generate.sh export-all txt
```

### Using Python Script Directly

```bash
# Export with more control
python3 scripts/export_cv.py cv_senior_pm --formats all --output-dir exports/

# Export to custom directory
python3 scripts/export_cv.py cv --formats txt md --output-dir build/

# Include ATS-optimized PDF
python3 scripts/export_cv.py cv_senior_pm --formats pdf --ats
```

## Format Details

### PDF (Standard)

**Purpose**: Standard high-quality CV for most applications

**Features**:
- Full Typst styling and formatting
- Multi-column layouts preserved
- Custom fonts and colors
- Optimized for printing

**Best For**:
- Email attachments
- Print submissions
- Professional presentations

**Command**:
```bash
./generate.sh export senior-pm pdf
```

### Plain Text (.txt)

**Purpose**: Paste into online application forms

**Features**:
- No formatting (plain text only)
- Layout preserved where possible
- Cleaned spacing
- Maximum ATS compatibility

**Best For**:
- Online job application forms
- Applicant Tracking Systems
- Plain text requirements
- Email body (when PDF rejected)

**Command**:
```bash
./generate.sh export senior-pm txt
```

**Example Use Case**: Indeed, LinkedIn, or company career portals that have text-only fields.

### Markdown (.md)

**Purpose**: GitHub, LinkedIn, easy sharing and editing

**Features**:
- Structured headings
- Bullet points preserved
- Plain text format
- Version control friendly

**Best For**:
- GitHub profile
- LinkedIn About section
- Quick updates and editing
- Version tracking

**Command**:
```bash
./generate.sh export senior-pm md
```

**Example Use Case**: Copy content to LinkedIn profile, GitHub README, or personal website CMS.

### HTML (.html)

**Purpose**: Portfolio websites and online hosting

**Features**:
- Styled with embedded CSS
- Responsive design
- Print-friendly
- Self-contained (no external dependencies)

**Best For**:
- Personal portfolio websites
- Online CV hosting
- Sharing via web link
- Blog posts

**Command**:
```bash
./generate.sh export senior-pm html
```

**Example Use Case**: Upload to personal website, host on GitHub Pages, or share via web link.

## Installation Requirements

### Required

- **Python 3.x**: For export script
- **Typst**: For PDF compilation

### Optional (for full functionality)

```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils pandoc

# macOS
brew install poppler pandoc

# Check installation
pdftotext -v
pandoc --version
```

**Without optional tools**:
- PDF export: ✓ Works (Typst only)
- TXT export: ✗ Requires pdftotext
- MD export: ⚠ Limited (uses text-based fallback)
- HTML export: ⚠ Limited (uses markdown-based fallback)

## Workflow Examples

### Job Application Workflow

**Scenario**: Applying for a Senior PM position

1. **Generate PDF for attachment**:
   ```bash
   ./generate.sh senior-pm
   ```

2. **Export text for online form**:
   ```bash
   ./generate.sh export senior-pm txt
   ```

3. **Copy text content**:
   ```bash
   cat exports/cv_senior_pm.txt | pbcopy  # macOS
   # or
   xclip -sel clip < exports/cv_senior_pm.txt  # Linux
   ```

4. **Submit**: Attach PDF and paste text into form fields

### Portfolio Update Workflow

**Scenario**: Updating personal website

1. **Export to HTML**:
   ```bash
   ./generate.sh export senior-pm html
   ```

2. **Upload to website**:
   ```bash
   cp exports/cv_senior_pm.html ~/website/cv.html
   ```

3. **Commit changes**:
   ```bash
   cd ~/website
   git add cv.html
   git commit -m "Update CV"
   git push
   ```

### LinkedIn Profile Update

**Scenario**: Keeping LinkedIn in sync with CV

1. **Export to Markdown**:
   ```bash
   ./generate.sh export exec-summary md
   ```

2. **Review and adapt**:
   ```bash
   cat exports/cv_exec_summary.md
   ```

3. **Copy sections** to LinkedIn:
   - Summary → About section
   - Professional Experience → Experience section
   - Key achievements → Featured section

## File Naming Convention

Exported files follow this pattern:

```
[base_name].[extension]
[base_name]_ats.[extension]  # ATS-optimized variant
```

**Examples**:
- `cv_senior_pm.pdf` - Standard Senior PM CV
- `cv_senior_pm.txt` - Plain text version
- `cv_senior_pm.md` - Markdown version
- `cv_senior_pm.html` - HTML version
- `cv_senior_pm_ats.pdf` - ATS-optimized PDF

## Cleaning Up

```bash
# Remove all exports
rm -rf exports/*

# Keep directory structure
rm -f exports/*.{pdf,txt,md,html}
```

## Best Practices

### Plain Text Exports

When using `.txt` files:
1. **Review before pasting**: Check formatting is acceptable
2. **Remove extra spacing**: Some online forms don't handle multiple spaces well
3. **Test in form**: Paste into form and verify readability

### HTML Exports

When using `.html` files:
1. **Test in browsers**: Check Safari, Chrome, Firefox
2. **Check mobile view**: Ensure responsive on phones/tablets
3. **Test printing**: Verify print layout if PDF fallback needed

### Markdown Exports

When using `.md` files:
1. **Review headings**: Adjust heading levels if needed (#, ##, ###)
2. **Check links**: Ensure email/phone links work correctly
3. **Preview rendered**: Use GitHub preview or markdown viewer

## Troubleshooting

### "typst: command not found"

**Problem**: Typst not installed

**Solution**:
```bash
# macOS
brew install typst

# Linux
cargo install --git https://github.com/typst/typst

# Or download from https://github.com/typst/typst/releases
```

### "pdftotext: command not found"

**Problem**: poppler-utils not installed

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

**Workaround**: Text export will be limited but still functional

### "pandoc: command not found"

**Problem**: Pandoc not installed

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install pandoc

# macOS
brew install pandoc
```

**Workaround**: Script will use text-based conversion (basic formatting)

### Exports Look Wrong

**Problem**: Format-specific issues

**Solutions**:
1. **Check source PDF**: Compile with `./generate.sh senior-pm` first
2. **Update tools**: Ensure latest versions of pdftotext/pandoc
3. **Manual cleanup**: Edit exported files to fix formatting
4. **Report issue**: File issue on GitHub repository

## Advanced Usage

### Custom Output Directory

```bash
python3 scripts/export_cv.py cv_senior_pm \
  --formats all \
  --output-dir custom_exports/
```

### Batch Export for All Variants

```bash
for variant in cv cv_senior_pm cv_superintendent cv_estimator cv_exec_summary; do
  python3 scripts/export_cv.py $variant --formats txt md
done
```

### Integration with CI/CD

```yaml
# .github/workflows/export-cv.yml
name: Export CVs
on: [push]
jobs:
  export:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: |
          sudo apt-get install -y poppler-utils pandoc
          cargo install --git https://github.com/typst/typst
      - name: Export all formats
        run: ./generate.sh export-all all
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: cv-exports
          path: exports/
```

## Future Enhancements

Planned features:
- **DOCX export**: Microsoft Word format
- **LaTeX export**: For academic CVs
- **JSON export**: Structured data for APIs
- **ATS-optimized templates**: Variant .typ files for max ATS compatibility
- **Batch processing**: Export all variants automatically on commit

## Support

For questions or issues:
1. Check this README
2. Review script help: `python3 scripts/export_cv.py --help`
3. Consult main documentation (README.md, CLAUDE.md)
4. File issue on GitHub repository

---

**Version**: 1.0
**Last Updated**: 2025-12-03
**Part of**: brilliantmikecv Multi-Format Export Pipeline
