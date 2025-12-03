#!/usr/bin/env python3
"""
Achievement Database Management Script
Manage and query the centralized achievement metrics database

Usage:
    ./scripts/achievements.py list                     # List all achievements
    ./scripts/achievements.py list --tags senior-pm    # Filter by tags
    ./scripts/achievements.py report --tags senior-pm  # Generate report
    ./scripts/achievements.py stats                    # Show statistics
    ./scripts/achievements.py export --format json     # Export to JSON
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict
import json


class AchievementDatabase:
    """Manage the achievement database"""

    def __init__(self, yaml_path: str = "data/achievements.yaml"):
        self.yaml_path = Path(yaml_path)
        if not self.yaml_path.exists():
            raise FileNotFoundError(f"Achievement database not found: {yaml_path}")

        with open(self.yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        self.achievements = data.get('achievements', [])
        self.metadata = data.get('metadata', {})
        self.categories = data.get('categories', [])
        self.tags_info = data.get('tags', {})

    def filter_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Filter achievements by tags"""
        if not tags:
            return self.achievements

        filtered = []
        for achievement in self.achievements:
            achievement_tags = achievement.get('tags', [])
            if any(tag in achievement_tags for tag in tags):
                filtered.append(achievement)
        return filtered

    def filter_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Filter achievements by category"""
        return [a for a in self.achievements if a.get('category') == category]

    def filter_by_metric(self, metric: str) -> List[Dict[str, Any]]:
        """Filter achievements by metric type"""
        return [a for a in self.achievements if a.get('metric') == metric]

    def get_by_id(self, achievement_id: str) -> Dict[str, Any]:
        """Get achievement by ID"""
        for achievement in self.achievements:
            if achievement.get('id') == achievement_id:
                return achievement
        return None

    def list_achievements(self, tags: List[str] = None, category: str = None,
                         metric: str = None, sort_by: str = None) -> List[Dict[str, Any]]:
        """List achievements with optional filtering and sorting"""
        results = self.achievements

        if tags:
            results = self.filter_by_tags(tags)

        if category:
            results = [a for a in results if a.get('category') == category]

        if metric:
            results = [a for a in results if a.get('metric') == metric]

        if sort_by == 'value' or sort_by == 'value_numeric':
            results = sorted(results,
                           key=lambda x: x.get('value_numeric', 0),
                           reverse=True)
        elif sort_by == 'year':
            results = sorted(results,
                           key=lambda x: x.get('year', 0),
                           reverse=True)

        return results

    def generate_stats(self) -> Dict[str, Any]:
        """Generate statistics about the achievement database"""
        stats = {
            'total_achievements': len(self.achievements),
            'categories': defaultdict(int),
            'metrics': defaultdict(int),
            'tags': defaultdict(int),
            'total_project_value': 0,
            'projects': set(),
            'companies': set(),
            'years': set(),
        }

        for achievement in self.achievements:
            # Count categories
            if 'category' in achievement:
                stats['categories'][achievement['category']] += 1

            # Count metrics
            if 'metric' in achievement:
                stats['metrics'][achievement['metric']] += 1

            # Count tags
            for tag in achievement.get('tags', []):
                stats['tags'][tag] += 1

            # Sum project values
            if achievement.get('metric') == 'project_value':
                stats['total_project_value'] += achievement.get('value_numeric', 0)

            # Collect projects
            if 'project' in achievement:
                stats['projects'].add(achievement['project'])

            # Collect companies
            if 'company' in achievement:
                stats['companies'].add(achievement['company'])

            # Collect years
            if 'year' in achievement:
                stats['years'].add(achievement['year'])

        # Convert sets to counts
        stats['unique_projects'] = len(stats['projects'])
        stats['unique_companies'] = len(stats['companies'])
        stats['year_range'] = f"{min(stats['years'])} - {max(stats['years'])}" if stats['years'] else "N/A"

        # Remove sets (not JSON serializable)
        del stats['projects']
        del stats['companies']
        del stats['years']

        # Convert defaultdicts to regular dicts
        stats['categories'] = dict(stats['categories'])
        stats['metrics'] = dict(stats['metrics'])
        stats['tags'] = dict(stats['tags'])

        return stats


def format_achievement_table(achievements: List[Dict[str, Any]]) -> str:
    """Format achievements as a table"""
    if not achievements:
        return "No achievements found."

    lines = []
    lines.append("\n" + "="*100)
    lines.append(f"{'ID':<30} {'Metric':<20} {'Value':<15} {'Project/Company':<35}")
    lines.append("="*100)

    for achievement in achievements:
        aid = achievement.get('id', 'N/A')[:29]
        metric = achievement.get('metric', 'N/A')[:19]
        value = achievement.get('value', 'N/A')[:14]
        project = achievement.get('project', achievement.get('company', 'N/A'))[:34]

        lines.append(f"{aid:<30} {metric:<20} {value:<15} {project:<35}")

    lines.append("="*100)
    lines.append(f"\nTotal: {len(achievements)} achievements\n")

    return "\n".join(lines)


def format_achievement_report(achievements: List[Dict[str, Any]]) -> str:
    """Format achievements as a detailed report"""
    if not achievements:
        return "No achievements found."

    lines = []
    lines.append("\n" + "="*80)
    lines.append("ACHIEVEMENT REPORT")
    lines.append("="*80 + "\n")

    for i, achievement in enumerate(achievements, 1):
        lines.append(f"{i}. {achievement.get('id', 'N/A')}")
        lines.append(f"   Metric: {achievement.get('metric', 'N/A')}")
        lines.append(f"   Value: {achievement.get('value', 'N/A')}")

        if 'value_numeric' in achievement:
            lines.append(f"   Numeric: {achievement.get('value_numeric'):,}")

        if 'project' in achievement:
            lines.append(f"   Project: {achievement.get('project')}")

        if 'company' in achievement:
            lines.append(f"   Company: {achievement.get('company')}")

        if 'year' in achievement:
            lines.append(f"   Year: {achievement.get('year')}")

        if 'location' in achievement:
            lines.append(f"   Location: {achievement.get('location')}")

        if 'description' in achievement:
            lines.append(f"   Description: {achievement.get('description')}")

        if 'tags' in achievement:
            lines.append(f"   Tags: {', '.join(achievement.get('tags', []))}")

        lines.append("")

    lines.append("="*80)
    lines.append(f"Total: {len(achievements)} achievements")
    lines.append("="*80 + "\n")

    return "\n".join(lines)


def format_stats_report(stats: Dict[str, Any]) -> str:
    """Format statistics as a report"""
    lines = []
    lines.append("\n" + "="*80)
    lines.append("ACHIEVEMENT DATABASE STATISTICS")
    lines.append("="*80 + "\n")

    lines.append(f"Total Achievements: {stats['total_achievements']}")
    lines.append(f"Unique Projects: {stats['unique_projects']}")
    lines.append(f"Unique Companies: {stats['unique_companies']}")
    lines.append(f"Year Range: {stats['year_range']}")
    lines.append(f"Total Project Value: ${stats['total_project_value']:,}\n")

    lines.append("Categories:")
    for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  - {category}: {count}")

    lines.append("\nMetric Types:")
    for metric, count in sorted(stats['metrics'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  - {metric}: {count}")

    lines.append("\nTop Tags:")
    for tag, count in sorted(stats['tags'].items(), key=lambda x: x[1], reverse=True)[:15]:
        lines.append(f"  - {tag}: {count}")

    lines.append("\n" + "="*80 + "\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Achievement Database Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                           List all achievements
  %(prog)s list --tags senior-pm          Filter by tags
  %(prog)s list --category multifamily    Filter by category
  %(prog)s list --metric project_value    Filter by metric type
  %(prog)s list --sort value              Sort by numeric value
  %(prog)s report --tags senior-pm        Generate detailed report
  %(prog)s stats                          Show database statistics
  %(prog)s export --format json           Export to JSON
  %(prog)s get eastlake-value             Get specific achievement by ID
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    list_parser = subparsers.add_parser('list', help='List achievements')
    list_parser.add_argument('--tags', nargs='+', help='Filter by tags')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--metric', help='Filter by metric type')
    list_parser.add_argument('--sort', choices=['value', 'year'], help='Sort results')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate detailed report')
    report_parser.add_argument('--tags', nargs='+', help='Filter by tags')
    report_parser.add_argument('--category', help='Filter by category')
    report_parser.add_argument('--metric', help='Filter by metric type')
    report_parser.add_argument('--sort', choices=['value', 'year'], help='Sort results')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export achievements')
    export_parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                               help='Export format')
    export_parser.add_argument('--tags', nargs='+', help='Filter by tags')
    export_parser.add_argument('--output', '-o', help='Output file (default: stdout)')

    # Get command
    get_parser = subparsers.add_parser('get', help='Get achievement by ID')
    get_parser.add_argument('id', help='Achievement ID')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        db = AchievementDatabase()

        if args.command == 'list':
            achievements = db.list_achievements(
                tags=args.tags,
                category=args.category,
                metric=args.metric,
                sort_by=args.sort
            )
            print(format_achievement_table(achievements))

        elif args.command == 'report':
            achievements = db.list_achievements(
                tags=args.tags,
                category=args.category,
                metric=args.metric,
                sort_by=args.sort
            )
            print(format_achievement_report(achievements))

        elif args.command == 'stats':
            stats = db.generate_stats()
            print(format_stats_report(stats))

        elif args.command == 'export':
            achievements = db.list_achievements(tags=args.tags)

            if args.format == 'json':
                output = json.dumps(achievements, indent=2)
            else:  # yaml
                output = yaml.dump(achievements, default_flow_style=False)

            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output)
                print(f"Exported {len(achievements)} achievements to {args.output}")
            else:
                print(output)

        elif args.command == 'get':
            achievement = db.get_by_id(args.id)
            if achievement:
                print(yaml.dump(achievement, default_flow_style=False))
            else:
                print(f"Achievement not found: {args.id}", file=sys.stderr)
                sys.exit(1)

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
