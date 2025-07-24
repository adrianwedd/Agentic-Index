"""Generate beautiful text-based trend visualizations without matplotlib dependency."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

class TextTrendsGenerator:
    """Generate beautiful text-based trend visualizations."""
    
    def __init__(self, history_dir: Path = Path("data/history"), output_dir: Path = Path("docs/trends")):
        self.history_dir = history_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_snapshots(self) -> Tuple[List[datetime], List[Any]]:
        """Load and parse all historical snapshots."""
        files = sorted(self.history_dir.glob("*.json"))
        dates = []
        snapshots = []
        
        for f in files:
            try:
                date = datetime.strptime(f.stem, "%Y-%m-%d")
            except ValueError:
                continue
                
            with f.open() as fh:
                try:
                    data = json.load(fh)
                    if isinstance(data, dict) and "repos" in data:
                        snap = data["repos"]
                    elif isinstance(data, list):
                        snap = data
                    else:
                        snap = []
                except json.JSONDecodeError:
                    snap = []
                    
            dates.append(date)
            snapshots.append(snap)
            
        return dates, snapshots
    
    def normalize_repo_data(self, repo: Dict) -> Dict:
        """Normalize repository data across different schema versions."""
        return {
            'name': repo.get('name', repo.get('full_name', 'unknown')),
            'full_name': repo.get('full_name', repo.get('name', 'unknown')),
            'stars': repo.get('stargazers_count', 0),
            'forks': repo.get('forks_count', 0),
            'issues': repo.get('open_issues_count', 0),
            'score': repo.get('AgenticIndexScore', repo.get('AgentOpsScore', 0)),
            'language': repo.get('language', 'Unknown'),
            'category': repo.get('category', 'Uncategorized'),
        }
    
    def create_ascii_bar_chart(self, data: Dict[str, int], title: str, max_width: int = 40) -> str:
        """Create a beautiful ASCII bar chart."""
        if not data:
            return f"\n{title}\n{'='*len(title)}\nNo data available.\n"
        
        max_val = max(data.values())
        if max_val == 0:
            return f"\n{title}\n{'='*len(title)}\nAll values are zero.\n"
        
        result = f"\n{title}\n{'='*len(title)}\n"
        
        for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
            bar_length = int((value / max_val) * max_width)
            bar = '█' * bar_length + '░' * (max_width - bar_length)
            percentage = (value / sum(data.values())) * 100 if sum(data.values()) > 0 else 0
            result += f"{label:20} │{bar}│ {value:,} ({percentage:.1f}%)\n"
        
        return result + "\n"
    
    def create_sparkline(self, values: List[float], width: int = 20) -> str:
        """Create a simple ASCII sparkline."""
        if not values or all(v is None for v in values):
            return "─" * width
        
        # Filter out None values
        clean_values = [v for v in values if v is not None]
        if not clean_values:
            return "─" * width
            
        if len(clean_values) == 1:
            return "●" + "─" * (width - 1)
        
        min_val = min(clean_values)
        max_val = max(clean_values)
        
        if max_val == min_val:
            return "─" * width
        
        # Create sparkline
        chars = "▁▂▃▄▅▆▇█"
        sparkline = ""
        
        # Sample the values to fit the width
        if len(clean_values) > width:
            step = len(clean_values) / width
            sampled_values = [clean_values[int(i * step)] for i in range(width)]
        else:
            sampled_values = clean_values + [clean_values[-1]] * (width - len(clean_values))
        
        for val in sampled_values:
            normalized = (val - min_val) / (max_val - min_val)
            char_index = int(normalized * (len(chars) - 1))
            sparkline += chars[char_index]
        
        return sparkline
    
    def generate_evolution_report(self, dates: List[datetime], snapshots: List[Any]):
        """Generate a comprehensive text-based evolution report."""
        if not snapshots:
            return
        
        # Get latest snapshot to identify top repos
        latest = snapshots[-1]
        latest_repos = {}
        
        for repo in latest:
            if isinstance(repo, dict):
                norm_repo = self.normalize_repo_data(repo)
                if norm_repo['score'] > 0:
                    latest_repos[norm_repo['name']] = norm_repo
        
        # Get top 10 repositories by score
        top_repos = sorted(latest_repos.items(), key=lambda x: x[1]['score'], reverse=True)[:10]
        
        # Build evolution data
        evolution_data = {}
        for repo_name, _ in top_repos:
            evolution_data[repo_name] = {
                'dates': [],
                'stars': [],
                'scores': [],
                'forks': []
            }
        
        for date, snap in zip(dates, snapshots):
            snapshot_lookup = {}
            for repo in snap:
                if isinstance(repo, dict):
                    norm_repo = self.normalize_repo_data(repo)
                    snapshot_lookup[norm_repo['name']] = norm_repo
            
            for repo_name in evolution_data.keys():
                evolution_data[repo_name]['dates'].append(date)
                if repo_name in snapshot_lookup:
                    repo_data = snapshot_lookup[repo_name]
                    evolution_data[repo_name]['stars'].append(repo_data['stars'])
                    evolution_data[repo_name]['scores'].append(repo_data['score'])
                    evolution_data[repo_name]['forks'].append(repo_data['forks'])
                else:
                    evolution_data[repo_name]['stars'].append(None)
                    evolution_data[repo_name]['scores'].append(None)
                    evolution_data[repo_name]['forks'].append(None)
        
        # Generate the report
        report_content = f"""
🚀 AGENTIC INDEX - BEAUTIFUL TRENDS ANALYSIS
{'='*60}

📊 OVERVIEW
{'-'*20}
Historical snapshots: {len(snapshots)}
Date range: {dates[0].date()} → {dates[-1].date()}
Total tracked repositories: {len(latest_repos)}

🏆 TOP REPOSITORY EVOLUTION
{'-'*40}
"""
        
        for i, (repo_name, repo_data) in enumerate(top_repos[:8], 1):
            evolution = evolution_data[repo_name]
            current_stars = repo_data['stars']
            current_score = repo_data['score']
            
            # Create sparklines
            star_sparkline = self.create_sparkline(evolution['stars'])
            score_sparkline = self.create_sparkline(evolution['scores'])
            
            # Calculate growth if we have multiple data points
            star_growth = ""
            if len([s for s in evolution['stars'] if s is not None]) >= 2:
                first_stars = next((s for s in evolution['stars'] if s is not None), 0)
                if first_stars > 0:
                    growth_pct = ((current_stars - first_stars) / first_stars) * 100
                    arrow = "📈" if growth_pct > 0 else "📉" if growth_pct < 0 else "➡️"
                    star_growth = f" {arrow} {growth_pct:+.1f}%"
            
            short_name = repo_name.split('/')[-1] if '/' in repo_name else repo_name
            
            report_content += f"""
#{i:2} {short_name:25}
    Stars:  {star_sparkline} {current_stars:,}{star_growth}
    Score:  {score_sparkline} {current_score:.2f}
    Lang:   {repo_data['language']:15} Category: {repo_data['category']}
"""
        
        # Current landscape analysis
        all_repos = list(latest_repos.values())
        
        # Category distribution
        categories = {}
        for repo in all_repos:
            cat = repo['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        # Language distribution
        languages = {}
        for repo in all_repos:
            lang = repo['language']
            if lang != 'Unknown':
                languages[lang] = languages.get(lang, 0) + 1
        
        # Score distribution
        scores = [repo['score'] for repo in all_repos]
        avg_score = sum(scores) / len(scores) if scores else 0
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0
        
        report_content += f"""

📊 CURRENT LANDSCAPE ANALYSIS
{'-'*40}

📈 Score Statistics:
    Average Score: {avg_score:.2f}
    Score Range:   {min_score:.2f} → {max_score:.2f}
    Total Repos:   {len(all_repos)}

{self.create_ascii_bar_chart(categories, "🏷️ REPOSITORY CATEGORIES")}

{self.create_ascii_bar_chart(dict(list(languages.items())[:10]), "💻 TOP PROGRAMMING LANGUAGES")}

🔍 INSIGHTS & OBSERVATIONS
{'-'*40}
• Data spans {(dates[-1] - dates[0]).days} days across {len(snapshots)} snapshots
• Average repository has {sum(r['stars'] for r in all_repos)/len(all_repos):,.0f} stars
• Most active category: {max(categories.items(), key=lambda x: x[1])[0]}
• Most popular language: {max(languages.items(), key=lambda x: x[1])[0] if languages else 'N/A'}

📋 DATA RETENTION RECOMMENDATION
{'-'*40}
⚠️  Currently only {len(snapshots)} snapshots available
✅ Increased retention to 365 days in config.yaml
🔄 Future data collection will provide richer trend analysis

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Save the report
        report_path = self.output_dir / 'beautiful_trends_report.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_content, report_path
    
    def generate_csv_export(self, dates: List[datetime], snapshots: List[Any]):
        """Generate CSV exports for external visualization tools."""
        if not snapshots:
            return
        
        csv_path = self.output_dir / 'repository_trends.csv'
        
        with open(csv_path, 'w') as f:
            f.write("date,repository,stars,forks,issues,score,language,category\n")
            
            for date, snap in zip(dates, snapshots):
                for repo in snap:
                    if isinstance(repo, dict):
                        norm_repo = self.normalize_repo_data(repo)
                        if norm_repo['score'] > 0:
                            f.write(f"{date.date()},{norm_repo['name']},{norm_repo['stars']},"
                                  f"{norm_repo['forks']},{norm_repo['issues']},{norm_repo['score']},"
                                  f"{norm_repo['language']},{norm_repo['category']}\n")
        
        print(f"📊 CSV export generated: {csv_path}")
    
    def generate_all_visualizations(self):
        """Generate all text-based trend visualizations."""
        print("🎨 Generating beautiful text-based trend visualizations...")
        
        dates, snapshots = self.load_snapshots()
        
        if not snapshots:
            print("❌ No historical data found. Please check data/history directory.")
            return
        
        print(f"📊 Found {len(snapshots)} historical snapshots from {dates[0].date()} to {dates[-1].date()}")
        
        # Generate comprehensive report
        report_content, report_path = self.generate_evolution_report(dates, snapshots)
        
        # Generate CSV export
        self.generate_csv_export(dates, snapshots)
        
        print(f"\n✅ Beautiful trend visualizations generated!")
        print(f"📊 Main report: {report_path}")
        print(f"📈 CSV export: {self.output_dir}/repository_trends.csv")
        print(f"\n{report_content}")


def main():
    """CLI entry point for generating text-based trend visualizations."""
    generator = TextTrendsGenerator()
    generator.generate_all_visualizations()


if __name__ == "__main__":
    main()