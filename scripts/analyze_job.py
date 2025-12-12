#!/usr/bin/env python3
"""
Job Description Keyword Analyzer
Analyzes job postings and optimizes CV keywords for ATS compatibility

Features:
- Extract keywords from job descriptions
- Compare with current CV keywords
- Calculate ATS match score
- Suggest keyword additions
- Generate keyword profiles for metadata.toml

Usage:
    ./scripts/analyze_job.py --file job_posting.txt
    ./scripts/analyze_job.py --text "Senior Project Manager with 10+ years..."
    ./scripts/analyze_job.py --file job.txt --variant senior-pm
    ./scripts/analyze_job.py --file job.txt --suggest --output keywords.toml
"""

import argparse
import sys
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import Counter
import toml


class JobAnalyzer:
    """Analyze job descriptions for keyword optimization"""

    # Common construction industry keywords to look for
    CONSTRUCTION_KEYWORDS = {
        'roles': [
            'project manager', 'senior pm', 'construction manager',
            'superintendent', 'senior superintendent', 'field manager',
            'estimator', 'senior estimator', 'preconstruction manager',
            'project executive', 'operations manager', 'site manager'
        ],
        'skills': [
            'lean construction', 'last planner system', 'pull planning',
            'schedule management', 'budget management', 'cost control',
            'safety management', 'osha', 'quality control', 'qc/qa',
            'subcontractor management', 'vendor management',
            'client relations', 'stakeholder management',
            'change order management', 'rfi management',
            'team leadership', 'staff management', 'mentoring'
        ],
        'project_types': [
            'multifamily', 'high-rise', 'mid-rise', 'low-rise',
            'podium construction', 'type iii', 'type v',
            'wood frame', 'concrete', 'steel',
            'ground-up', 'renovation', 'historic renovation',
            'tenant improvement', 'ti work', 'tis',
            'hospitality', 'hotel', 'mixed-use',
            'senior living', 'healthcare', 'assisted living',
            'luxury residential', 'custom homes', 'high-end'
        ],
        'tools': [
            'procore', 'primavera p6', 'p6', 'microsoft project',
            'bluebeam', 'autocad', 'revit', 'bim',
            'sage', 'viewpoint', 'cmis', 'e-builder'
        ],
        'certifications': [
            'pmp', 'leed', 'leed ap', 'certified professional',
            'ccm', 'osha 30', 'osha 10', 'cpr', 'first aid'
        ],
        'methods': [
            'design-build', 'design build', 'cm/gc', 'cmgc',
            'hard bid', 'competitive bid', 'negotiated',
            'integrated project delivery', 'ipd',
            'target value delivery', 'tvd'
        ],
        'values': [
            'million', 'mn', 'unit', 'units', 'sf', 'square feet',
            'story', 'stories', 'floor', 'floors'
        ]
    }

    # Common filler words to ignore
    STOP_WORDS = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'their', 'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all',
        'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'
    }

    def __init__(self, cv_keywords: List[str] = None):
        """Initialize analyzer with current CV keywords"""
        self.cv_keywords = set(k.lower() for k in (cv_keywords or []))

    def extract_keywords(self, text: str) -> Dict[str, List[Tuple[str, int]]]:
        """Extract keywords from job description"""
        text_lower = text.lower()

        results = {
            'roles': [],
            'skills': [],
            'project_types': [],
            'tools': [],
            'certifications': [],
            'methods': [],
            'values': [],
            'requirements': [],
            'numbers': []
        }

        # Extract known construction keywords
        for category, keywords in self.CONSTRUCTION_KEYWORDS.items():
            for keyword in keywords:
                count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text_lower))
                if count > 0:
                    results[category].append((keyword, count))

        # Sort by frequency
        for category in results:
            results[category].sort(key=lambda x: x[1], reverse=True)

        # Extract requirements (looking for "required", "must have", etc.)
        requirements_section = re.search(
            r'(requirements?|qualifications?|must have|required skills)[:\s]+(.*?)(?=\n\n|responsibilities|$)',
            text_lower,
            re.DOTALL | re.IGNORECASE
        )

        if requirements_section:
            req_text = requirements_section.group(2)
            results['requirements'] = self._extract_phrases(req_text)

        # Extract numeric values (years of experience, project sizes, etc.)
        numbers = re.findall(
            r'(\d+[\+]?)\s*(years?|million|mn|units?|sf|square feet|stories|floors)',
            text_lower
        )
        results['numbers'] = list(set(numbers))

        return results

    def _extract_phrases(self, text: str) -> List[Tuple[str, int]]:
        """Extract significant phrases from text"""
        # Split into sentences
        sentences = re.split(r'[.•\n-]', text)

        phrases = []
        for sentence in sentences:
            # Clean up
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue

            # Extract noun phrases (simple heuristic: 2-4 words not in stop words)
            words = re.findall(r'\b\w+\b', sentence.lower())
            for i in range(len(words) - 1):
                bigram = ' '.join(words[i:i+2])
                if words[i] not in self.STOP_WORDS and words[i+1] not in self.STOP_WORDS:
                    phrases.append(bigram)

                if i < len(words) - 2:
                    trigram = ' '.join(words[i:i+3])
                    if all(w not in self.STOP_WORDS for w in words[i:i+3]):
                        phrases.append(trigram)

        # Count frequency
        phrase_counts = Counter(phrases)
        return phrase_counts.most_common(20)

    def calculate_match_score(self, job_keywords: Dict[str, List[Tuple[str, int]]]) -> Dict:
        """Calculate ATS match score"""
        # Extract all job keywords
        all_job_keywords = set()
        for category, keywords in job_keywords.items():
            if category in ['requirements', 'numbers']:
                continue
            for keyword, _ in keywords:
                all_job_keywords.add(keyword.lower())

        # Calculate matches
        matches = all_job_keywords.intersection(self.cv_keywords)
        missing = all_job_keywords - self.cv_keywords

        total_keywords = len(all_job_keywords)
        match_count = len(matches)

        score = (match_count / total_keywords * 100) if total_keywords > 0 else 0

        return {
            'score': round(score, 1),
            'total_job_keywords': total_keywords,
            'matched_keywords': match_count,
            'matches': sorted(matches),
            'missing': sorted(missing)
        }

    def suggest_keywords(self, job_keywords: Dict[str, List[Tuple[str, int]]], top_n: int = 10) -> List[str]:
        """Suggest top keywords to add to CV"""
        # Prioritize by category importance and frequency
        category_weights = {
            'roles': 3.0,
            'skills': 2.5,
            'project_types': 2.0,
            'methods': 2.0,
            'tools': 1.5,
            'certifications': 2.0
        }

        suggestions = []

        for category, keywords in job_keywords.items():
            if category not in category_weights:
                continue

            weight = category_weights[category]

            for keyword, freq in keywords:
                if keyword.lower() not in self.cv_keywords:
                    score = freq * weight
                    suggestions.append((keyword, score, category, freq))

        # Sort by weighted score
        suggestions.sort(key=lambda x: x[1], reverse=True)

        return suggestions[:top_n]

    def generate_keyword_profile(self, job_keywords: Dict[str, List[Tuple[str, int]]], profile_name: str) -> str:
        """Generate a keyword profile for metadata.toml"""
        # Get top keywords from each category
        profile_keywords = []

        for category in ['roles', 'skills', 'project_types', 'tools', 'certifications', 'methods']:
            if category in job_keywords:
                for keyword, _ in job_keywords[category][:5]:  # Top 5 from each category
                    # Capitalize appropriately
                    if category == 'tools':
                        keyword = keyword.upper() if keyword in ['p6', 'bim'] else keyword.title()
                    else:
                        keyword = keyword.title()

                    if keyword not in profile_keywords:
                        profile_keywords.append(keyword)

        # Format as TOML
        toml_str = f"\n[keywords.{profile_name}]\n"
        toml_str += "    injected_keywords_list = [\n"

        for keyword in profile_keywords[:15]:  # Max 15 keywords
            toml_str += f'        "{keyword}",\n'

        toml_str += "    ]\n"

        return toml_str


def load_cv_keywords(metadata_path: str = "metadata.toml") -> List[str]:
    """Load current CV keywords from metadata.toml"""
    try:
        with open(metadata_path, 'r') as f:
            metadata = toml.load(f)

        keywords = metadata.get('inject', {}).get('injected_keywords_list', [])
        return keywords
    except FileNotFoundError:
        print(f"Warning: {metadata_path} not found. Using empty keyword list.", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error loading keywords: {e}", file=sys.stderr)
        return []


def format_analysis_report(job_keywords: Dict, match_score: Dict, suggestions: List, numbers: List) -> str:
    """Format analysis as a readable report"""
    lines = []
    lines.append("\n" + "="*80)
    lines.append("JOB DESCRIPTION KEYWORD ANALYSIS")
    lines.append("="*80 + "\n")

    # ATS Match Score
    lines.append(f"ATS MATCH SCORE: {match_score['score']}%")
    lines.append(f"  • Matched Keywords: {match_score['matched_keywords']}/{match_score['total_job_keywords']}")
    lines.append("")

    # Score interpretation
    score = match_score['score']
    if score >= 80:
        lines.append("  ✓ EXCELLENT - Strong keyword alignment")
    elif score >= 60:
        lines.append("  ○ GOOD - Decent alignment, room for improvement")
    elif score >= 40:
        lines.append("  ⚠ FAIR - Significant gaps in keyword coverage")
    else:
        lines.append("  ✗ POOR - Major keyword gaps, high risk of ATS rejection")

    lines.append("\n" + "-"*80)

    # Matched Keywords
    if match_score['matches']:
        lines.append("\nMATCHED KEYWORDS:")
        for keyword in match_score['matches'][:20]:
            lines.append(f"  ✓ {keyword}")

    lines.append("\n" + "-"*80)

    # Missing Keywords
    if match_score['missing']:
        lines.append("\nMISSING KEYWORDS:")
        for keyword in match_score['missing'][:20]:
            lines.append(f"  ✗ {keyword}")

    lines.append("\n" + "-"*80)

    # Top Suggestions
    if suggestions:
        lines.append("\nTOP KEYWORD SUGGESTIONS (ranked by importance):")
        for i, (keyword, score, category, freq) in enumerate(suggestions, 1):
            lines.append(f"  {i}. {keyword.title()}")
            lines.append(f"     Category: {category} | Frequency: {freq}x | Score: {score:.1f}")

    lines.append("\n" + "-"*80)

    # Requirements/Experience
    if numbers:
        lines.append("\nNUMERIC REQUIREMENTS:")
        for number, unit in sorted(set(numbers), reverse=True):
            lines.append(f"  • {number} {unit}")

    lines.append("\n" + "-"*80)

    # Category Breakdown
    lines.append("\nKEYWORD BREAKDOWN BY CATEGORY:")
    for category in ['roles', 'skills', 'project_types', 'tools', 'certifications', 'methods']:
        if category in job_keywords and job_keywords[category]:
            lines.append(f"\n{category.upper().replace('_', ' ')}:")
            for keyword, freq in job_keywords[category][:10]:
                lines.append(f"  • {keyword.title()} ({freq}x)")

    lines.append("\n" + "="*80 + "\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Job Description Keyword Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --file job_posting.txt
  %(prog)s --text "Senior Project Manager with..."
  %(prog)s --file job.txt --variant senior-pm
  %(prog)s --file job.txt --suggest --output new_keywords.toml

Use cases:
  - Analyze job postings before applying
  - Optimize CV keywords for specific roles
  - Generate custom keyword profiles
  - Identify gaps in ATS compatibility
        """
    )

    parser.add_argument('--file', help='Path to job description file')
    parser.add_argument('--text', help='Job description text directly')
    parser.add_argument('--variant', help='CV variant to analyze (default: uses metadata.toml keywords)')
    parser.add_argument('--suggest', action='store_true', help='Generate keyword profile suggestion')
    parser.add_argument('--output', '-o', help='Output file for keyword profile (TOML format)')
    parser.add_argument('--profile-name', default='custom_job', help='Name for keyword profile')

    args = parser.parse_args()

    # Get job description text
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                job_text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        job_text = args.text
    else:
        print("Error: Must provide either --file or --text", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Load current CV keywords
    cv_keywords = load_cv_keywords()

    # Analyze job description
    analyzer = JobAnalyzer(cv_keywords)
    job_keywords = analyzer.extract_keywords(job_text)
    match_score = analyzer.calculate_match_score(job_keywords)
    suggestions = analyzer.suggest_keywords(job_keywords, top_n=10)

    # Print report
    report = format_analysis_report(
        job_keywords,
        match_score,
        suggestions,
        job_keywords.get('numbers', [])
    )
    print(report)

    # Generate keyword profile if requested
    if args.suggest:
        profile = analyzer.generate_keyword_profile(job_keywords, args.profile_name)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(profile)
            print(f"\n✓ Keyword profile saved to: {args.output}")
            print("\nTo use this profile:")
            print(f"1. Copy the content to your metadata.toml")
            print(f"2. Update [inject] section to use these keywords")
            print(f"3. Recompile your CV")
        else:
            print("\nSUGGESTED KEYWORD PROFILE:")
            print(profile)
            print("\nTo save this profile, run with: --output keywords.toml")


if __name__ == '__main__':
    main()
