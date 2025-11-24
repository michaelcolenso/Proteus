# GitHub Actions Workflows

## compile-pdfs.yml

Automatically compiles all Typst CV variants and cover letter into PDFs when source files are modified.

### Triggers

The workflow runs when:
- `.typ` files are modified
- `metadata.toml` is modified
- Files in `modules_en/` are modified
- Files in `src/` (images, logos) are modified

### What it does

1. **Installs Typst**: Uses the official Typst installer
2. **Installs fonts**: Installs Roboto, Font Awesome, and Source Sans Pro
3. **Compiles all variants**:
   - `cv.typ` → `cv.pdf` (Standard CV)
   - `cv_senior_pm.typ` → `cv_senior_pm.pdf` (Senior PM)
   - `cv_superintendent.typ` → `cv_superintendent.pdf` (Superintendent)
   - `cv_estimator.typ` → `cv_estimator.pdf` (Estimator)
   - `cv_exec_summary.typ` → `cv_exec_summary.pdf` (Executive Summary)
   - `letter.typ` → `letter.pdf` (Cover Letter)
4. **Uploads PDFs as artifacts**: Available in the Actions tab for 90 days
5. **Commits PDFs to repository** (optional): Only on pushes to `main` branch

### Viewing Compiled PDFs

**From a Pull Request or Push:**
1. Go to the **Actions** tab in your GitHub repository
2. Click on the workflow run
3. Scroll to **Artifacts** section at the bottom
4. Download `cv-pdfs.zip`

**From the repository** (if auto-commit is enabled):
- PDFs are automatically committed to the main branch
- The commit message will be: `chore: auto-compile PDFs from Typst sources [skip ci]`
- The `[skip ci]` tag prevents infinite loops

### Configuration Options

#### Disable Auto-Commit

If you prefer to only use artifacts and **not** commit PDFs to the repository:

1. Open `.github/workflows/compile-pdfs.yml`
2. Remove or comment out the entire "Commit and push PDFs" step

#### Change Target Branch

To auto-commit to a different branch (e.g., `develop`):

```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/develop'
```

#### Add More Variants

To compile additional CV variants, add them in the "Compile all CV variants" step:

```bash
echo "Compiling custom_variant.typ..."
typst compile custom_variant.typ custom_variant.pdf
```

And add to the artifacts:

```yaml
- name: Upload PDFs as artifacts
  uses: actions/upload-artifact@v4
  with:
    path: |
      ...
      custom_variant.pdf
```

### Font Installation Notes

The workflow installs:
- **Roboto**: From Ubuntu packages
- **Font Awesome 6**: From Ubuntu packages
- **Source Sans Pro**: Downloaded from Adobe's official GitHub releases

If you need additional fonts, add them to the "Install required fonts" step.

### Troubleshooting

**Compilation fails:**
- Check the Actions log for specific Typst errors
- Ensure all modules referenced in your `.typ` files exist
- Verify image paths are correct

**Fonts not found:**
- The workflow installs standard fonts automatically
- If using custom fonts, add installation commands to the workflow

**PDFs not committed:**
- Check that auto-commit is enabled (step exists)
- Verify you're pushing to the branch specified in the condition (default: `main`)
- Ensure repository permissions allow Actions to commit (Settings → Actions → Workflow permissions → "Read and write permissions")

### Performance

Typical workflow run time: **1-2 minutes**
- Checkout: ~5 seconds
- Install Typst: ~10 seconds
- Install fonts: ~20 seconds
- Compile all PDFs: ~10-30 seconds
- Upload artifacts: ~5 seconds
- Commit (if enabled): ~5 seconds
