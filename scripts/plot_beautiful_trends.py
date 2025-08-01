"""Create beautiful, comprehensive trend visualizations for repository data."""

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import numpy as np
import seaborn as sns

# Set up beautiful styling
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    plt.style.use('seaborn-darkgrid')
try:
    sns.set_palette("husl")
except:
    pass  # fallback to default palette

class BeautifulTrendsGenerator:
    """Generate beautiful, comprehensive trend visualizations."""
    
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
                    # Handle different schema formats
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
        # Handle different field names and structures
        normalized = {
            'name': repo.get('name', repo.get('full_name', 'unknown')),
            'full_name': repo.get('full_name', repo.get('name', 'unknown')),
            'stars': repo.get('stargazers_count', 0),
            'forks': repo.get('forks_count', 0),
            'issues': repo.get('open_issues_count', 0),
            'score': repo.get('AgenticIndexScore', repo.get('AgentOpsScore', 0)),
            'language': repo.get('language', 'Unknown'),
            'category': repo.get('category', 'Uncategorized'),
            'license': repo.get('license', 'Unknown'),
            'pushed_at': repo.get('pushed_at', ''),
            'archived': repo.get('archived', False)
        }
        return normalized
    
    def build_comprehensive_timeseries(self, dates: List[datetime], snapshots: List[Any]) -> Dict:
        """Build comprehensive time series data for all metrics."""
        if not snapshots:
            return {}
            
        # Get all unique repositories across all snapshots
        all_repos = set()
        for snap in snapshots:
            for repo in snap:
                if isinstance(repo, dict):
                    norm_repo = self.normalize_repo_data(repo)
                    all_repos.add(norm_repo['name'])
        
        # Build time series for each repository
        series_data = {}
        for repo_name in all_repos:
            series_data[repo_name] = {
                'dates': [],
                'stars': [],
                'forks': [],
                'issues': [],
                'score': [],
                'language': None,
                'category': None,
                'latest_stars': 0
            }
        
        # Populate time series data
        for date, snap in zip(dates, snapshots):
            repo_lookup = {}
            for repo in snap:
                if isinstance(repo, dict):
                    norm_repo = self.normalize_repo_data(repo)
                    repo_lookup[norm_repo['name']] = norm_repo
            
            for repo_name in all_repos:
                if repo_name in repo_lookup:
                    repo = repo_lookup[repo_name]
                    series_data[repo_name]['dates'].append(date)
                    series_data[repo_name]['stars'].append(repo['stars'])
                    series_data[repo_name]['forks'].append(repo['forks'])
                    series_data[repo_name]['issues'].append(repo['issues'])
                    series_data[repo_name]['score'].append(repo['score'])
                    series_data[repo_name]['language'] = repo['language']
                    series_data[repo_name]['category'] = repo['category']
                    series_data[repo_name]['latest_stars'] = repo['stars']
                else:
                    # Repository not present in this snapshot
                    series_data[repo_name]['dates'].append(date)
                    series_data[repo_name]['stars'].append(None)
                    series_data[repo_name]['forks'].append(None)
                    series_data[repo_name]['issues'].append(None)
                    series_data[repo_name]['score'].append(None)
        
        return series_data
    
    def plot_repository_evolution_timeline(self, series_data: Dict, top_n: int = 10):
        """Create a beautiful timeline showing repository evolution."""
        # Get top repositories by latest stars
        top_repos = sorted(
            [(name, data['latest_stars']) for name, data in series_data.items() if data['latest_stars'] > 0],
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🚀 Repository Evolution Timeline - Top Performers', fontsize=20, fontweight='bold', y=0.98)
        
        colors = plt.cm.Set3(np.linspace(0, 1, top_n))
        
        # Plot 1: Stars Evolution
        ax1.set_title('⭐ Star Growth Over Time', fontsize=14, fontweight='bold', pad=20)
        for i, (repo_name, _) in enumerate(top_repos):
            data = series_data[repo_name]
            if data['dates'] and any(s for s in data['stars'] if s is not None):
                # Filter out None values
                filtered_dates = [d for d, s in zip(data['dates'], data['stars']) if s is not None]
                filtered_stars = [s for s in data['stars'] if s is not None]
                
                if filtered_dates:
                    ax1.plot(filtered_dates, filtered_stars, 'o-', 
                            label=repo_name.split('/')[-1] if '/' in repo_name else repo_name,
                            linewidth=2.5, markersize=6, color=colors[i])
        
        ax1.set_ylabel('Stars', fontweight='bold')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot 2: Score Evolution
        ax2.set_title('📊 Agentic Index Score Progression', fontsize=14, fontweight='bold', pad=20)
        for i, (repo_name, _) in enumerate(top_repos):
            data = series_data[repo_name]
            if data['dates'] and any(s for s in data['score'] if s is not None and s > 0):
                filtered_dates = [d for d, s in zip(data['dates'], data['score']) if s is not None and s > 0]
                filtered_scores = [s for s in data['score'] if s is not None and s > 0]
                
                if filtered_dates:
                    ax2.plot(filtered_dates, filtered_scores, 's-',
                            label=repo_name.split('/')[-1] if '/' in repo_name else repo_name,
                            linewidth=2.5, markersize=6, color=colors[i])
        
        ax2.set_ylabel('Agentic Index Score', fontweight='bold')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        # Plot 3: Forks Evolution
        ax3.set_title('🍴 Fork Growth Trends', fontsize=14, fontweight='bold', pad=20)
        for i, (repo_name, _) in enumerate(top_repos):
            data = series_data[repo_name]
            if data['dates'] and any(f for f in data['forks'] if f is not None):
                filtered_dates = [d for d, f in zip(data['dates'], data['forks']) if f is not None]
                filtered_forks = [f for f in data['forks'] if f is not None]
                
                if filtered_dates:
                    ax3.plot(filtered_dates, filtered_forks, '^-',
                            label=repo_name.split('/')[-1] if '/' in repo_name else repo_name,
                            linewidth=2.5, markersize=6, color=colors[i])
        
        ax3.set_ylabel('Forks', fontweight='bold')
        ax3.set_xlabel('Date', fontweight='bold')
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        # Plot 4: Issues Evolution
        ax4.set_title('🐛 Open Issues Tracking', fontsize=14, fontweight='bold', pad=20)
        for i, (repo_name, _) in enumerate(top_repos):
            data = series_data[repo_name]
            if data['dates'] and any(iss for iss in data['issues'] if iss is not None):
                filtered_dates = [d for d, iss in zip(data['dates'], data['issues']) if iss is not None]
                filtered_issues = [iss for iss in data['issues'] if iss is not None]
                
                if filtered_dates:
                    ax4.plot(filtered_dates, filtered_issues, 'd-',
                            label=repo_name.split('/')[-1] if '/' in repo_name else repo_name,
                            linewidth=2.5, markersize=6, color=colors[i])
        
        ax4.set_ylabel('Open Issues', fontweight='bold')
        ax4.set_xlabel('Date', fontweight='bold')
        ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax4.grid(True, alpha=0.3)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.93, right=0.85)
        plt.savefig(self.output_dir / 'repository_evolution_timeline.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_current_state_dashboard(self, latest_snapshot: List[Dict]):
        """Create a comprehensive dashboard of current repository state."""
        if not latest_snapshot:
            return
            
        # Normalize all repository data
        repos = [self.normalize_repo_data(repo) for repo in latest_snapshot if isinstance(repo, dict)]
        repos = [r for r in repos if r['score'] > 0]  # Filter out invalid entries
        
        fig = plt.figure(figsize=(20, 12))
        fig.suptitle('📈 Agentic Index - Current State Dashboard', fontsize=24, fontweight='bold', y=0.98)
        
        # Create a complex grid layout
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # Plot 1: Score vs Stars Correlation (Top Left)
        ax1 = fig.add_subplot(gs[0, :2])
        stars = [r['stars'] for r in repos]
        scores = [r['score'] for r in repos]
        
        scatter = ax1.scatter(stars, scores, c=scores, s=60, alpha=0.7, cmap='viridis')
        ax1.set_xlabel('GitHub Stars', fontweight='bold')
        ax1.set_ylabel('Agentic Index Score', fontweight='bold')
        ax1.set_title('⭐ Stars vs Agentic Score Correlation', fontsize=14, fontweight='bold')
        ax1.set_xscale('log')
        ax1.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax1, label='Score')
        
        # Plot 2: Category Distribution (Top Right)
        ax2 = fig.add_subplot(gs[0, 2:])
        categories = [r['category'] for r in repos]
        category_counts = {}
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        wedges, texts, autotexts = ax2.pie(category_counts.values(), labels=category_counts.keys(), 
                                          autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
        ax2.set_title('🏷️ Repository Categories', fontsize=14, fontweight='bold')
        
        # Plot 3: Language Distribution (Middle Left)
        ax3 = fig.add_subplot(gs[1, :2])
        languages = [r['language'] for r in repos if r['language'] != 'Unknown']
        lang_counts = {}
        for lang in languages:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        # Show top 10 languages
        top_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        lang_names, lang_vals = zip(*top_langs) if top_langs else ([], [])
        
        bars = ax3.barh(range(len(lang_names)), lang_vals, color=plt.cm.viridis(np.linspace(0, 1, len(lang_names))))
        ax3.set_yticks(range(len(lang_names)))
        ax3.set_yticklabels(lang_names)
        ax3.set_xlabel('Number of Repositories', fontweight='bold')
        ax3.set_title('💻 Programming Languages', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')
        
        # Plot 4: Score Components Heatmap (Middle Right)
        ax4 = fig.add_subplot(gs[1, 2:])
        
        # Create score component data (simulated based on the scoring algorithm)
        score_components = []
        repo_names = []
        
        for repo in repos[:15]:  # Top 15 repos
            # Calculate components based on scoring formula
            stars_component = 0.30 * math.log2(repo['stars'] + 1)
            issue_ratio = max(0, min(1, 1 - repo['issues'] / (repo['stars'] + 1)))
            issue_component = 0.20 * issue_ratio
            
            components = [
                stars_component,
                issue_component,
                repo['score'] * 0.25,  # Estimated recency
                repo['score'] * 0.15,  # Estimated docs
                repo['score'] * 0.10   # Other factors
            ]
            score_components.append(components)
            repo_names.append(repo['name'].split('/')[-1] if '/' in repo['name'] else repo['name'])
        
        if score_components:
            heatmap_data = np.array(score_components)
            im = ax4.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
            ax4.set_xticks(range(5))
            ax4.set_xticklabels(['Stars', 'Issues', 'Recency', 'Docs', 'Others'], rotation=45)
            ax4.set_yticks(range(len(repo_names)))
            ax4.set_yticklabels(repo_names, fontsize=8)
            ax4.set_title('🔥 Score Components Heatmap', fontsize=14, fontweight='bold')
            plt.colorbar(im, ax=ax4, label='Component Score')
        
        # Plot 5: Top Performers Table (Bottom)
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')
        
        # Create a beautiful table of top performers
        top_repos = sorted(repos, key=lambda x: x['score'], reverse=True)[:10]
        table_data = []
        for i, repo in enumerate(top_repos):
            table_data.append([
                f"#{i+1}",
                repo['name'].split('/')[-1] if '/' in repo['name'] else repo['name'],
                f"{repo['score']:.2f}",
                f"{repo['stars']:,}",
                f"{repo['forks']:,}",
                repo['language'],
                repo['category']
            ])
        
        table = ax5.table(cellText=table_data,
                         colLabels=['Rank', 'Repository', 'Score', 'Stars', 'Forks', 'Language', 'Category'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0, 1, 1])
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # Style the table
        for i in range(len(table_data) + 1):
            for j in range(7):
                cell = table[(i, j)]
                if i == 0:  # Header row
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
        
        ax5.set_title('🏆 Top 10 Repositories by Agentic Index Score', fontsize=16, fontweight='bold', pad=20)
        
        plt.savefig(self.output_dir / 'current_state_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_all_charts(self):
        """Generate all beautiful trend charts."""
        print("🎨 Generating beautiful trend visualizations...")
        
        # Load historical data
        dates, snapshots = self.load_snapshots()
        
        if not snapshots:
            print("❌ No historical data found. Please check data/history directory.")
            return
        
        print(f"📊 Found {len(snapshots)} historical snapshots from {dates[0].date()} to {dates[-1].date()}")
        
        # Build comprehensive time series
        series_data = self.build_comprehensive_timeseries(dates, snapshots)
        
        # Generate charts
        print("📈 Creating repository evolution timeline...")
        self.plot_repository_evolution_timeline(series_data)
        
        print("📊 Creating current state dashboard...")
        latest_snapshot = snapshots[-1] if snapshots else []
        self.plot_current_state_dashboard(latest_snapshot)
        
        print(f"✅ Beautiful charts generated in {self.output_dir}")
        print("   - repository_evolution_timeline.png")
        print("   - current_state_dashboard.png")


def main():
    """CLI entry point for generating beautiful trend charts."""
    generator = BeautifulTrendsGenerator()
    generator.generate_all_charts()


if __name__ == "__main__":
    main()