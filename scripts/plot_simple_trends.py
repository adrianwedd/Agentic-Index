"""Create beautiful trend visualizations using only matplotlib (no seaborn dependency)."""

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set up beautiful styling without seaborn
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.edgecolor': '#dee2e6',
    'axes.grid': True,
    'grid.color': '#e9ecef',
    'grid.alpha': 0.6,
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9
})

class TrendsGenerator:
    """Generate beautiful trend visualizations."""
    
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
    
    def get_top_repos_evolution(self, dates: List[datetime], snapshots: List[Any], top_n: int = 8):
        """Get evolution data for top repositories."""
        if not snapshots:
            return {}, []
            
        # Get latest snapshot to determine top repos
        latest = snapshots[-1]
        latest_scores = {}
        
        for repo in latest:
            if isinstance(repo, dict):
                norm_repo = self.normalize_repo_data(repo)
                if norm_repo['score'] > 0:
                    latest_scores[norm_repo['name']] = norm_repo['score']
        
        # Get top repositories
        top_repos = sorted(latest_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        repo_names = [name for name, _ in top_repos]
        
        # Build time series for each repo
        evolution_data = {name: {'dates': [], 'stars': [], 'scores': [], 'forks': []} 
                         for name in repo_names}
        
        for date, snap in zip(dates, snapshots):
            # Create lookup for this snapshot
            snapshot_lookup = {}
            for repo in snap:
                if isinstance(repo, dict):
                    norm_repo = self.normalize_repo_data(repo)
                    snapshot_lookup[norm_repo['name']] = norm_repo
            
            # Record data for each top repo
            for repo_name in repo_names:
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
        
        return evolution_data, repo_names
    
    def plot_multi_metric_evolution(self, evolution_data: Dict, repo_names: List[str]):
        """Create a comprehensive multi-metric evolution chart."""
        if not evolution_data:
            print("No evolution data to plot")
            return
            
        # Create color palette
        colors = plt.cm.tab10([i for i in range(len(repo_names))])
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('🚀 Repository Evolution - Multi-Metric Analysis', fontsize=16, fontweight='bold', y=0.98)
        
        # Plot 1: Stars Evolution
        ax1.set_title('⭐ GitHub Stars Growth', fontweight='bold', pad=15)
        for i, repo_name in enumerate(repo_names):
            data = evolution_data[repo_name]
            # Filter None values
            valid_data = [(d, s) for d, s in zip(data['dates'], data['stars']) if s is not None]
            if valid_data:
                dates, stars = zip(*valid_data)
                short_name = repo_name.split('/')[-1] if '/' in repo_name else repo_name
                ax1.plot(dates, stars, 'o-', label=short_name, linewidth=2.5, 
                        markersize=6, color=colors[i])
        
        ax1.set_ylabel('Stars')
        ax1.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot 2: Agentic Index Scores
        ax2.set_title('📊 Agentic Index Score Evolution', fontweight='bold', pad=15)
        for i, repo_name in enumerate(repo_names):
            data = evolution_data[repo_name]
            valid_data = [(d, s) for d, s in zip(data['dates'], data['scores']) if s is not None and s > 0]
            if valid_data:
                dates, scores = zip(*valid_data)
                short_name = repo_name.split('/')[-1] if '/' in repo_name else repo_name
                ax2.plot(dates, scores, 's-', label=short_name, linewidth=2.5, 
                        markersize=6, color=colors[i])
        
        ax2.set_ylabel('Agentic Index Score')
        ax2.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
        ax2.tick_params(axis='x', rotation=45)
        
        # Plot 3: Forks Growth
        ax3.set_title('🍴 Repository Forks', fontweight='bold', pad=15)
        for i, repo_name in enumerate(repo_names):
            data = evolution_data[repo_name]
            valid_data = [(d, f) for d, f in zip(data['dates'], data['forks']) if f is not None]
            if valid_data:
                dates, forks = zip(*valid_data)
                short_name = repo_name.split('/')[-1] if '/' in repo_name else repo_name
                ax3.plot(dates, forks, '^-', label=short_name, linewidth=2.5, 
                        markersize=6, color=colors[i])
        
        ax3.set_ylabel('Forks')
        ax3.set_xlabel('Date')
        ax3.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
        ax3.tick_params(axis='x', rotation=45)
        
        # Plot 4: Growth Velocity (Stars per time period)
        ax4.set_title('📈 Star Growth Velocity', fontweight='bold', pad=15)
        for i, repo_name in enumerate(repo_names):
            data = evolution_data[repo_name]
            valid_data = [(d, s) for d, s in zip(data['dates'], data['stars']) if s is not None]
            if len(valid_data) > 1:
                dates, stars = zip(*valid_data)
                velocities = []
                velocity_dates = []
                
                for j in range(1, len(stars)):
                    # Calculate stars gained per day
                    days_diff = (dates[j] - dates[j-1]).days
                    if days_diff > 0:
                        velocity = (stars[j] - stars[j-1]) / days_diff
                        velocities.append(max(0, velocity))  # No negative velocities
                        velocity_dates.append(dates[j])
                
                if velocities:
                    short_name = repo_name.split('/')[-1] if '/' in repo_name else repo_name
                    ax4.plot(velocity_dates, velocities, 'd-', label=short_name, 
                            linewidth=2.5, markersize=6, color=colors[i])
        
        ax4.set_ylabel('Stars per Day')
        ax4.set_xlabel('Date')
        ax4.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.93)
        plt.savefig(self.output_dir / 'repository_evolution_comprehensive.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def plot_current_snapshot_analysis(self, latest_snapshot: List[Dict]):
        """Create analysis charts for the current state."""
        if not latest_snapshot:
            return
            
        repos = [self.normalize_repo_data(repo) for repo in latest_snapshot if isinstance(repo, dict)]
        repos = [r for r in repos if r['score'] > 0]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('📊 Current Repository Landscape Analysis', fontsize=16, fontweight='bold', y=0.98)
        
        # Plot 1: Score vs Stars correlation
        ax1.set_title('⭐ Stars vs Agentic Score Correlation', fontweight='bold', pad=15)
        stars = [r['stars'] for r in repos]
        scores = [r['score'] for r in repos]
        scatter = ax1.scatter(stars, scores, c=scores, s=50, alpha=0.7, cmap='viridis')
        ax1.set_xlabel('GitHub Stars')
        ax1.set_ylabel('Agentic Index Score')
        ax1.set_xscale('log')
        plt.colorbar(scatter, ax=ax1, label='Score')
        
        # Plot 2: Category distribution
        ax2.set_title('🏷️ Repository Categories', fontweight='bold', pad=15)
        categories = [r['category'] for r in repos]
        category_counts = {}
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        if category_counts:
            wedges, texts, autotexts = ax2.pie(category_counts.values(), 
                                              labels=category_counts.keys(), 
                                              autopct='%1.1f%%', startangle=90)
            # Make text more readable
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        # Plot 3: Language distribution (top 8)
        ax3.set_title('💻 Programming Languages', fontweight='bold', pad=15)
        languages = [r['language'] for r in repos if r['language'] != 'Unknown']
        lang_counts = {}
        for lang in languages:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        top_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        if top_langs:
            lang_names, lang_vals = zip(*top_langs)
            bars = ax3.barh(range(len(lang_names)), lang_vals, 
                           color=plt.cm.tab10([i for i in range(len(lang_names))]))
            ax3.set_yticks(range(len(lang_names)))
            ax3.set_yticklabels(lang_names)
            ax3.set_xlabel('Number of Repositories')
            
            # Add value labels on bars
            for i, (bar, val) in enumerate(zip(bars, lang_vals)):
                ax3.text(val + 0.1, i, str(val), va='center', fontweight='bold')
        
        # Plot 4: Score distribution histogram
        ax4.set_title('📈 Score Distribution', fontweight='bold', pad=15)
        ax4.hist(scores, bins=20, alpha=0.7, color='skyblue', edgecolor='navy')
        ax4.set_xlabel('Agentic Index Score')
        ax4.set_ylabel('Number of Repositories')
        ax4.axvline(sum(scores)/len(scores), color='red', linestyle='--', 
                   label=f'Mean: {sum(scores)/len(scores):.2f}')
        ax4.legend()
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.93)
        plt.savefig(self.output_dir / 'current_landscape_analysis.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_summary_report(self, dates: List[datetime], snapshots: List[Any]):
        """Generate a text summary report."""
        if not snapshots:
            return
            
        latest = snapshots[-1]
        repos = [self.normalize_repo_data(repo) for repo in latest if isinstance(repo, dict)]
        repos = [r for r in repos if r['score'] > 0]
        
        report_path = self.output_dir / 'trends_summary.txt'
        
        with open(report_path, 'w') as f:
            f.write("🚀 AGENTIC INDEX - TRENDS ANALYSIS SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"📊 Data Overview:\n")
            f.write(f"   • Historical snapshots: {len(snapshots)}\n")
            f.write(f"   • Date range: {dates[0].date()} to {dates[-1].date()}\n")
            f.write(f"   • Total repositories tracked: {len(repos)}\n\n")
            
            if repos:
                top_repo = max(repos, key=lambda x: x['score'])
                f.write(f"🏆 Top Repository:\n")
                f.write(f"   • Name: {top_repo['name']}\n")
                f.write(f"   • Score: {top_repo['score']:.2f}\n")
                f.write(f"   • Stars: {top_repo['stars']:,}\n")
                f.write(f"   • Language: {top_repo['language']}\n")
                f.write(f"   • Category: {top_repo['category']}\n\n")
                
                avg_score = sum(r['score'] for r in repos) / len(repos)
                avg_stars = sum(r['stars'] for r in repos) / len(repos)
                
                f.write(f"📈 Repository Statistics:\n")
                f.write(f"   • Average score: {avg_score:.2f}\n")
                f.write(f"   • Average stars: {avg_stars:,.0f}\n")
                f.write(f"   • Score range: {min(r['score'] for r in repos):.2f} - {max(r['score'] for r in repos):.2f}\n\n")
                
                # Category breakdown
                categories = {}
                for repo in repos:
                    cat = repo['category']
                    categories[cat] = categories.get(cat, 0) + 1
                
                f.write(f"🏷️ Category Breakdown:\n")
                for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(repos)) * 100
                    f.write(f"   • {cat}: {count} repos ({percentage:.1f}%)\n")
                
        print(f"📝 Summary report generated: {report_path}")
    
    def generate_all_charts(self):
        """Generate all trend visualizations."""
        print("🎨 Generating beautiful trend visualizations...")
        
        dates, snapshots = self.load_snapshots()
        
        if not snapshots:
            print("❌ No historical data found. Please check data/history directory.")
            return
        
        print(f"📊 Found {len(snapshots)} historical snapshots from {dates[0].date()} to {dates[-1].date()}")
        
        # Get evolution data for top repositories
        evolution_data, repo_names = self.get_top_repos_evolution(dates, snapshots)
        
        if evolution_data:
            print("📈 Creating repository evolution charts...")
            self.plot_multi_metric_evolution(evolution_data, repo_names)
        
        print("📊 Creating current landscape analysis...")
        latest_snapshot = snapshots[-1] if snapshots else []
        self.plot_current_snapshot_analysis(latest_snapshot)
        
        print("📝 Generating summary report...")
        self.generate_summary_report(dates, snapshots)
        
        print(f"\n✅ Beautiful charts generated in {self.output_dir}/")
        print("   📈 repository_evolution_comprehensive.png")
        print("   📊 current_landscape_analysis.png") 
        print("   📝 trends_summary.txt")


def main():
    """CLI entry point for generating trend charts."""
    generator = TrendsGenerator()
    generator.generate_all_charts()


if __name__ == "__main__":
    main()