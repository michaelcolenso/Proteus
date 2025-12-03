#!/usr/bin/env python3
"""
Multi-Format CV Export Pipeline
Converts CV from Typst to multiple formats for different use cases

Formats:
- PDF (standard): Typst compiled output (default)
- TXT (plain text): For online application forms
- HTML (styled): For personal website/portfolio
- Markdown: For GitHub/LinkedIn
- PDF (ATS-optimized): Simplified layout for ATS systems

Usage:
    ./scripts/export_cv.py cv_senior_pm --formats all
    ./scripts/export_cv.py cv_senior_pm --formats txt html
    ./scripts/export_cv.py cv_senior_pm --output-dir exports/
"""

import argparse
import subprocess
import sys
import shutil
from pathlib import Path
from typing import List, Optional
import re


class CVExporter:
    """Export CV to multiple formats"""

    def __init__(self, source_file: str, output_dir: str = "exports"):
        self.source_file = Path(source_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        if not self.source_file.exists():
            raise FileNotFoundError(f"Source file not found: {source_file}")

        self.base_name = self.source_file.stem
        self.pdf_file = self.source_file.with_suffix('.pdf')

    def check_dependencies(self, format_type: str) -> bool:
        """Check if required tools are installed for format"""
        deps = {
            'pdf': ['typst'],
            'txt': ['pdftotext', 'typst'],
            'html': ['pandoc', 'typst'],
            'md': ['pandoc', 'typst'],
        }

        if format_type not in deps:
            return True

        for tool in deps[format_type]:
            if not shutil.which(tool):
                print(f"Warning: {tool} not found. Cannot export to {format_type}", file=sys.stderr)
                return False
        return True

    def export_pdf(self, ats_optimized: bool = False) -> Path:
        """Export to PDF using Typst"""
        print(f"Exporting to PDF...")

        if ats_optimized:
            # Use simplified template for ATS
            output_file = self.output_dir / f"{self.base_name}_ats.pdf"
            # Note: Would need to create ATS-optimized .typ variants
            print("  Note: ATS-optimized PDF requires ATS-specific .typ template")
            print("  Using standard PDF for now")
        else:
            output_file = self.output_dir / f"{self.base_name}.pdf"

        # Compile with Typst
        result = subprocess.run(
            ['typst', 'compile', str(self.source_file), str(output_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error compiling PDF: {result.stderr}", file=sys.stderr)
            return None

        print(f"  ✓ Created: {output_file}")
        return output_file

    def export_txt(self) -> Path:
        """Export to plain text"""
        print(f"Exporting to plain text...")

        # First ensure PDF exists
        if not self.pdf_file.exists():
            pdf = self.export_pdf()
            if not pdf:
                return None
            pdf_source = pdf
        else:
            pdf_source = self.pdf_file

        output_file = self.output_dir / f"{self.base_name}.txt"

        # Convert PDF to text using pdftotext
        result = subprocess.run(
            ['pdftotext', '-layout', str(pdf_source), str(output_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error converting to text: {result.stderr}", file=sys.stderr)
            return None

        # Clean up the text file
        self._clean_text_file(output_file)

        print(f"  ✓ Created: {output_file}")
        return output_file

    def _clean_text_file(self, file_path: Path):
        """Clean up plain text output"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove excessive blank lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        # Remove page form feeds
        content = content.replace('\f', '\n\n')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip() + '\n')

    def export_markdown(self) -> Path:
        """Export to Markdown using pandoc"""
        print(f"Exporting to Markdown...")

        # First ensure PDF exists
        if not self.pdf_file.exists():
            pdf = self.export_pdf()
            if not pdf:
                return None
            pdf_source = pdf
        else:
            pdf_source = self.pdf_file

        output_file = self.output_dir / f"{self.base_name}.md"

        # Convert PDF to markdown via pandoc
        result = subprocess.run(
            ['pandoc', str(pdf_source), '-f', 'pdf', '-t', 'markdown', '-o', str(output_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error converting to Markdown: {result.stderr}", file=sys.stderr)
            # Try alternative approach: txt -> md
            txt_file = self.export_txt()
            if txt_file:
                print("  Trying text-based conversion...")
                return self._txt_to_markdown(txt_file, output_file)
            return None

        print(f"  ✓ Created: {output_file}")
        return output_file

    def _txt_to_markdown(self, txt_file: Path, output_file: Path) -> Path:
        """Convert plain text to basic Markdown"""
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic Markdown formatting
        lines = content.split('\n')
        md_lines = []

        for line in lines:
            stripped = line.strip()

            # Detect headers (all caps, short lines)
            if stripped and stripped.isupper() and len(stripped) < 50:
                md_lines.append(f"## {stripped}\n")
            # Detect bullet points
            elif stripped.startswith('•') or stripped.startswith('-'):
                md_lines.append(f"- {stripped.lstrip('•- ')}")
            else:
                md_lines.append(line)

        md_content = '\n'.join(md_lines)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"  ✓ Created: {output_file} (text-based conversion)")
        return output_file

    def export_html(self) -> Path:
        """Export to styled HTML using pandoc"""
        print(f"Exporting to HTML...")

        # First ensure PDF exists
        if not self.pdf_file.exists():
            pdf = self.export_pdf()
            if not pdf:
                return None
            pdf_source = pdf
        else:
            pdf_source = self.pdf_file

        output_file = self.output_dir / f"{self.base_name}.html"

        # Convert PDF to HTML via pandoc with CSS styling
        result = subprocess.run(
            [
                'pandoc', str(pdf_source),
                '-f', 'pdf',
                '-t', 'html',
                '--standalone',
                '--self-contained',
                '-o', str(output_file)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error converting to HTML: {result.stderr}", file=sys.stderr)
            # Try markdown -> HTML
            md_file = self.export_markdown()
            if md_file:
                print("  Trying Markdown-based conversion...")
                return self._md_to_html(md_file, output_file)
            return None

        # Add custom CSS styling
        self._add_html_styling(output_file)

        print(f"  ✓ Created: {output_file}")
        return output_file

    def _md_to_html(self, md_file: Path, output_file: Path) -> Path:
        """Convert Markdown to HTML with styling"""
        result = subprocess.run(
            [
                'pandoc', str(md_file),
                '-f', 'markdown',
                '-t', 'html',
                '--standalone',
                '--self-contained',
                '-o', str(output_file)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error converting Markdown to HTML: {result.stderr}", file=sys.stderr)
            return None

        self._add_html_styling(output_file)
        print(f"  ✓ Created: {output_file} (Markdown-based conversion)")
        return output_file

    def _add_html_styling(self, html_file: Path):
        """Add custom CSS to HTML export"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add custom CSS
        css = """
<style>
body {
    font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
    max-width: 8.5in;
    margin: 0 auto;
    padding: 1in;
    line-height: 1.6;
    color: #333;
}
h1, h2, h3 {
    color: #1a1a1a;
    margin-top: 1.5em;
}
h1 {
    font-size: 2em;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
}
h2 {
    font-size: 1.5em;
    border-bottom: 1px solid #ccc;
    padding-bottom: 0.2em;
}
ul {
    margin: 0.5em 0;
}
li {
    margin: 0.3em 0;
}
a {
    color: #0066cc;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
@media print {
    body {
        padding: 0.5in;
    }
}
</style>
"""

        # Insert CSS before </head> if exists, otherwise before </html>
        if '</head>' in content:
            content = content.replace('</head>', f'{css}\n</head>')
        elif '</html>' in content:
            content = content.replace('</html>', f'{css}\n</html>')
        else:
            content = css + content

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

    def export_all(self, formats: List[str], ats_pdf: bool = False):
        """Export to all specified formats"""
        results = {}

        for fmt in formats:
            if not self.check_dependencies(fmt):
                results[fmt] = None
                continue

            if fmt == 'pdf':
                results[fmt] = self.export_pdf(ats_optimized=False)
                if ats_pdf:
                    results['pdf_ats'] = self.export_pdf(ats_optimized=True)
            elif fmt == 'txt':
                results[fmt] = self.export_txt()
            elif fmt == 'md' or fmt == 'markdown':
                results[fmt] = self.export_markdown()
            elif fmt == 'html':
                results[fmt] = self.export_html()

        return results


def main():
    parser = argparse.ArgumentParser(
        description='Multi-Format CV Export Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s cv_senior_pm                        # Export PDF only
  %(prog)s cv_senior_pm --formats all          # Export all formats
  %(prog)s cv_senior_pm --formats txt html     # Export specific formats
  %(prog)s cv --formats pdf --ats              # Export ATS-optimized PDF
  %(prog)s cv_senior_pm --output-dir build/   # Custom output directory

Available formats:
  pdf      - Standard PDF (via Typst)
  txt      - Plain text (for online forms)
  md       - Markdown (for GitHub/LinkedIn)
  html     - Styled HTML (for portfolio websites)
  all      - All of the above

Note: Requires typst, pdftotext, and pandoc to be installed.
        """
    )

    parser.add_argument('source', help='Source .typ file (e.g., cv_senior_pm)')
    parser.add_argument('--formats', nargs='+', default=['pdf'],
                       choices=['pdf', 'txt', 'md', 'markdown', 'html', 'all'],
                       help='Output formats (default: pdf)')
    parser.add_argument('--output-dir', '-o', default='exports',
                       help='Output directory (default: exports/)')
    parser.add_argument('--ats', action='store_true',
                       help='Also generate ATS-optimized PDF')

    args = parser.parse_args()

    # Add .typ extension if not provided
    source_file = args.source if args.source.endswith('.typ') else f"{args.source}.typ"

    # Expand 'all' formats
    formats = args.formats
    if 'all' in formats:
        formats = ['pdf', 'txt', 'md', 'html']

    # Normalize markdown
    formats = ['md' if f == 'markdown' else f for f in formats]

    try:
        exporter = CVExporter(source_file, args.output_dir)

        print(f"Exporting {source_file} to formats: {', '.join(formats)}")
        print(f"Output directory: {args.output_dir}\n")

        results = exporter.export_all(formats, ats_pdf=args.ats)

        # Summary
        print("\n" + "="*60)
        print("Export Summary:")
        print("="*60)

        success_count = 0
        for fmt, result in results.items():
            if result:
                print(f"  ✓ {fmt.upper()}: {result}")
                success_count += 1
            else:
                print(f"  ✗ {fmt.upper()}: Failed")

        print(f"\nSuccessfully exported {success_count}/{len(results)} formats")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
