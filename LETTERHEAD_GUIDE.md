# Professional Letterhead Design Guide

## Overview

The cover letter template (`letter.typ`) now includes a refined professional letterhead design with enhanced typography and visual hierarchy.

## New Features

### 1. Professional Letterhead

The letterhead includes:
- **Large, bold name** in accent color (from `metadata.toml`)
- **Professional title** in small caps with elegant letter-spacing
- **Elegant separator line** using the accent color (lightened 40%)
- **Contact information** in a single-line layout with dot separators
- **Responsive design** that adapts to color scheme changes

### 2. Enhanced Typography

- **Font size**: 11pt for improved readability
- **Line spacing**: 0.65em leading within paragraphs
- **Paragraph spacing**: 1.2em between paragraphs
- **Text alignment**: Justified for professional appearance
- **Modern style**: No first-line indentation

### 3. Dynamic Color Theming

The letterhead automatically extracts and uses the `awesome_color` from `metadata.toml`, supporting:
- Preset colors: `skyblue`, `red`, `nephritis`, `concrete`, `darknight`
- Custom hex colors (e.g., `#1E90FF`)

## Customization Options

### Toggle Letterhead

To disable the custom letterhead and use the default brilliant-cv styling:

```typst
// Change this line in letter.typ
#let use-custom-letterhead = false
```

### Adjust Letterhead Spacing

Modify the vertical spacing after the letterhead:

```typst
// Adjust this value (currently 85pt) in letter.typ
v(85pt)  // Increase or decrease as needed
```

### Change Color Scheme

Edit `metadata.toml`:

```toml
[layout]
    awesome_color = "skyblue"  # or "red", "nephritis", "concrete", "darknight"
    # Or use custom hex:
    awesome_color = "#1E90FF"
```

### Customize Contact Information

The letterhead pulls contact info from `metadata.toml`:

```toml
[personal.info]
    phone = "206.607.7836"
    email = "michaelcolenso@gmail.com"
```

## Typography Settings Explained

### Paragraph Leading (Line Spacing)

```typst
#set par(leading: 0.65em)
```

- Controls space between lines within a paragraph
- `0.65em` provides comfortable reading without excessive spacing
- Adjust to `0.7em` for more space, `0.6em` for tighter spacing

### Paragraph Spacing

```typst
#set par(spacing: 1.2em)
```

- Controls space between paragraphs
- `1.2em` creates clear visual separation
- Adjust to `1.5em` for more space, `1em` for tighter spacing

### Text Justification

```typst
#set par(justify: true)
```

- Creates clean, aligned left and right margins
- Professional appearance for formal letters
- Set to `false` for left-aligned, ragged-right text

## Design Philosophy

The letterhead design follows these principles:

1. **Visual Hierarchy**: Name is most prominent, followed by title, then contact details
2. **Elegant Simplicity**: Minimal decorative elements, focus on typography
3. **Professional Tone**: Balanced, not overly designed
4. **Consistency**: Uses the same color scheme as the CV
5. **Readability**: Ample spacing and appropriate font sizes

## Best Practices

### For Different Applications

**Corporate/Traditional Roles**:
- Use `darknight` or `concrete` color scheme
- Keep letterhead enabled
- Use justified text

**Creative/Modern Roles**:
- Consider `skyblue` or `nephritis` for more personality
- Experiment with custom hex colors
- Consider left-aligned text (`justify: false`)

**Startup/Tech Roles**:
- Use brighter colors like `skyblue`
- Keep modern typography settings
- Consider adding LinkedIn or portfolio URL to contact line

### Customizing for Specific Companies

When tailoring letters for specific applications:

1. **Update recipient details**:
   ```typst
   recipientName: "Company Name",
   recipientAddress: "City, State",
   subject: "Re: Position Title",
   ```

2. **Adjust tone** through font size if needed:
   ```typst
   #set text(size: 10.5pt)  // Slightly smaller for more formal
   #set text(size: 11.5pt)  // Slightly larger for emphasis
   ```

3. **Save company-specific versions**:
   ```bash
   cp letter.typ letters/2025-12-03_company-name.typ
   ```

## Technical Details

### Font Stack

The letterhead uses fonts from `metadata.toml`:
- **Header (Name)**: `Roboto` (bold, 24pt)
- **Body text**: `Source Sans Pro` or `Source Sans 3` (11pt)
- **Contact info**: `Source Sans Pro` (9pt)

### Color Conversion

The template automatically converts brilliant-cv color names to RGB values:
- `darknight` → `#1E2022`
- `skyblue` → `#0395DE`
- `red` → `#DC3522`
- `nephritis` → `#27AE60`
- `concrete` → `#95A5A6`

### Spacing Units

All spacing uses Typst units:
- `pt` - Points (1/72 inch)
- `em` - Relative to font size (1em = current font size)
- `%` - Percentage of container width

## Troubleshooting

### Letterhead overlaps with content

Increase the spacing value:
```typst
v(95pt)  // Increase from 85pt
```

### Contact information wraps to multiple lines

Reduce font size or shorten text:
```typst
text(size: 8pt, ...)  // Reduce from 9pt
```

### Colors don't match CV

Ensure `metadata.toml` has the same `awesome_color` setting for both documents.

### Signature appears too close to text

Add more vertical space before signature:
```typst
#v(2em)  // Add before signature image
```

## Compilation

To compile the letter with the new design:

```bash
# Using the generate script
./generate.sh letter

# Or directly with Typst
typst compile letter.typ

# Watch mode for live updates
typst watch letter.typ
```

## Examples

### Minimal Contact Line

For privacy or brevity:
```typst
text(size: 9pt, fill: rgb("#444444"), {
  metadata.personal.info.email
})
```

### Extended Contact Line

Adding website or LinkedIn:
```typst
text(size: 9pt, fill: rgb("#444444"), {
  metadata.personal.info.phone
  h(12pt) + sym.circle.filled.small + h(12pt)
  metadata.personal.info.email
  h(12pt) + sym.circle.filled.small + h(12pt)
  link("https://linkedin.com/in/yourprofile")[LinkedIn]
})
```

## Version History

- **v1.0** (2025-12-03): Initial professional letterhead design
  - Custom letterhead with name, title, separator, contact info
  - Enhanced typography settings
  - Dynamic color theming
  - Improved paragraph and line spacing

## Future Enhancements

Potential additions for future versions:
- Optional professional photo in letterhead
- QR code linking to portfolio/LinkedIn
- Multiple letterhead layout options (centered, right-aligned)
- Company logo placement option
- Watermark support for draft versions
- Multi-page header/footer system

---

**Questions or Issues?**
Refer to the main documentation in `CLAUDE.md` or the brilliant-cv package documentation at https://typst.app/universe/package/brilliant-cv
