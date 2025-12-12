#!/usr/bin/env python3
"""
Cloudflare Bypass Effectiveness Monitor
Tracks success rates of different bypass techniques
"""
import json
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter

# Optional imports for visualization
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

@dataclass
class BypassAttempt:
    """Record of a bypass attempt"""
    timestamp: datetime
    technique: str  # 'basic', 'advanced', 'mock'
    status_code: int
    success: bool
    duration: float
    proxy_used: bool
    challenge_type: str  # 'none', 'javascript', 'captcha', 'ip_block', 'rate_limit'
    user_agent: str
    error_message: Optional[str] = None

class BypassEffectivenessMonitor:
    """Monitor and analyze bypass technique effectiveness"""
    
    def __init__(self, db_path: str = "bypass_monitoring.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize monitoring database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bypass_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    technique TEXT NOT NULL,
                    status_code INTEGER NOT NULL,
                    success BOOLEAN NOT NULL,
                    duration REAL NOT NULL,
                    proxy_used BOOLEAN NOT NULL,
                    challenge_type TEXT NOT NULL,
                    user_agent TEXT NOT NULL,
                    error_message TEXT
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON bypass_attempts(timestamp)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_technique ON bypass_attempts(technique)
            """)
            conn.commit()
    
    def log_attempt(self, attempt: BypassAttempt):
        """Log a bypass attempt"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bypass_attempts 
                (timestamp, technique, status_code, success, duration, proxy_used, challenge_type, user_agent, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                attempt.timestamp.isoformat(),
                attempt.technique,
                attempt.status_code,
                attempt.success,
                attempt.duration,
                attempt.proxy_used,
                attempt.challenge_type,
                attempt.user_agent,
                attempt.error_message
            ))
            conn.commit()
    
    def get_success_rates(self, days: int = 7) -> Dict[str, float]:
        """Get success rates by technique over the specified period"""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT technique, COUNT(*) as total, SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful
                FROM bypass_attempts 
                WHERE timestamp >= ?
                GROUP BY technique
            """, (since_date,))
            
            results = {}
            for technique, total, successful in cursor.fetchall():
                success_rate = (successful / total * 100) if total > 0 else 0
                results[technique] = {
                    'success_rate': round(success_rate, 2),
                    'total_attempts': total,
                    'successful_attempts': successful
                }
        
        return results
    
    def get_challenge_types(self, days: int = 7) -> Dict[str, int]:
        """Get distribution of challenge types encountered"""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT challenge_type, COUNT(*) as count
                FROM bypass_attempts 
                WHERE timestamp >= ? AND challenge_type != 'none'
                GROUP BY challenge_type
                ORDER BY count DESC
            """, (since_date,))
            
            return dict(cursor.fetchall())
    
    def get_performance_metrics(self, technique: str = None) -> Dict:
        """Get performance metrics for a technique or all techniques"""
        query = """
            SELECT 
                technique,
                AVG(duration) as avg_duration,
                MIN(duration) as min_duration,
                MAX(duration) as max_duration,
                COUNT(*) as total_attempts,
                SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful_attempts,
                SUM(CASE WHEN proxy_used THEN 1 ELSE 0 END) as proxy_attempts
            FROM bypass_attempts
            WHERE timestamp >= datetime('now', '-7 days')
        """
        params = []
        
        if technique:
            query += " AND technique = ?"
            params.append(technique)
        
        query += " GROUP BY technique"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            results = {}
            for row in cursor.fetchall():
                technique, avg_dur, min_dur, max_dur, total, successful, proxy_used = row
                success_rate = (successful / total * 100) if total > 0 else 0
                proxy_rate = (proxy_used / total * 100) if total > 0 else 0
                
                results[technique] = {
                    'avg_duration': round(avg_dur, 2),
                    'min_duration': round(min_dur, 2),
                    'max_duration': round(max_dur, 2),
                    'success_rate': round(success_rate, 2),
                    'total_attempts': total,
                    'proxy_usage_rate': round(proxy_rate, 2)
                }
        
        return results
    
    def get_trending_analysis(self, days: int = 7) -> List[Dict]:
        """Get daily success rate trends"""
        since_date = (datetime.now() - timedelta(days=days)).date().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    DATE(timestamp) as date,
                    technique,
                    COUNT(*) as total,
                    SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful
                FROM bypass_attempts 
                WHERE DATE(timestamp) >= ?
                GROUP BY DATE(timestamp), technique
                ORDER BY date DESC, technique
            """, (since_date,))
            
            trends = []
            for date, technique, total, successful in cursor.fetchall():
                success_rate = (successful / total * 100) if total > 0 else 0
                trends.append({
                    'date': date,
                    'technique': technique,
                    'success_rate': round(success_rate, 2),
                    'total_attempts': total,
                    'successful_attempts': successful
                })
        
        return trends
    
    def generate_report(self, days: int = 7) -> str:
        """Generate a comprehensive effectiveness report"""
        success_rates = self.get_success_rates(days)
        challenge_types = self.get_challenge_types(days)
        performance = self.get_performance_metrics()
        trends = self.get_trending_analysis(days)
        
        report = f"""
# Cloudflare Bypass Effectiveness Report ({days} days)

## Success Rates by Technique
"""
        for technique, data in success_rates.items():
            report += f"- **{technique.title()}**: {data['success_rate']:.1f}% ({data['successful_attempts']}/{data['total_attempts']})\n"
        
        report += f"""
## Challenge Types Encountered
"""
        for challenge, count in challenge_types.items():
            report += f"- **{challenge.replace('_', ' ').title()}**: {count} times\n"
        
        report += f"""
## Performance Metrics
"""
        for technique, data in performance.items():
            report += f"""
### {technique.title()}
- Average Duration: {data['avg_duration']:.2f}s
- Success Rate: {data['success_rate']:.1f}%
- Proxy Usage: {data['proxy_usage_rate']:.1f}%
- Total Attempts: {data['total_attempts']}
"""
        
        if trends:
            report += f"""
## Daily Trends (Last {days} days)
"""
            for trend in trends[-10:]:  # Last 10 entries
                report += f"- {trend['date']}: {trend['technique']} - {trend['success_rate']:.1f}% ({trend['successful_attempts']}/{trend['total_attempts']})\n"
        
        report += f"""
## Recommendations

### Most Effective Technique
{self._get_best_technique(success_rates)}

### Least Effective Technique  
{self._get_worst_technique(success_rates)}

### Most Common Challenge
{self._get_most_common_challenge(challenge_types)}
"""
        
        return report
    
    def _get_best_technique(self, success_rates: Dict) -> str:
        """Get the most successful technique"""
        if not success_rates:
            return "No data available"
        
        best = max(success_rates.items(), key=lambda x: x[1]['success_rate'])
        return f"{best[0].title()} with {best[1]['success_rate']:.1f}% success rate"
    
    def _get_worst_technique(self, success_rates: Dict) -> str:
        """Get the least successful technique"""
        if not success_rates:
            return "No data available"
        
        worst = min(success_rates.items(), key=lambda x: x[1]['success_rate'])
        return f"{worst[0].title()} with {worst[1]['success_rate']:.1f}% success rate"
    
    def _get_most_common_challenge(self, challenge_types: Dict) -> str:
        """Get the most commonly encountered challenge"""
        if not challenge_types:
            return "No challenges recorded"
        
        most_common = max(challenge_types.items(), key=lambda x: x[1])
        return f"{most_common[0].replace('_', ' ').title()} ({most_common[1]} times)"
    
    def plot_success_rates(self, days: int = 7, save_path: str = "success_rates.png"):
        """Create a bar chart of success rates"""
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib not available - skipping chart generation")
            return
        
        success_rates = self.get_success_rates(days)
        
        if not success_rates:
            print("No data to plot")
            return
        
        techniques = list(success_rates.keys())
        rates = [data['success_rate'] for data in success_rates.values()]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(techniques, rates, color=['#2E8B57', '#4169E1', '#FF6347'][:len(techniques)])
        
        plt.title(f'Cloudflare Bypass Success Rates (Last {days} days)')
        plt.ylabel('Success Rate (%)')
        plt.xlabel('Technique')
        plt.ylim(0, 100)
        
        # Add value labels on bars
        for bar, rate in zip(bars, rates):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{rate:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()  # Close instead of show to avoid display issues
        
        print(f"Chart saved to {save_path}")

def simulate_bypass_attempts(monitor: BypassEffectivenessMonitor, num_attempts: int = 50):
    """Simulate bypass attempts for testing"""
    import random
    
    techniques = ['basic', 'advanced', 'mock']
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    ]
    challenge_types = ['none', 'javascript', 'captcha', 'ip_block', 'rate_limit']
    
    for i in range(num_attempts):
        technique = random.choice(techniques)
        
        # Simulate different success rates for different techniques
        if technique == 'basic':
            success_prob = 0.05  # 5% success rate
        elif technique == 'advanced':
            success_prob = 0.15  # 15% success rate
        else:  # mock
            success_prob = 1.0   # 100% success rate
        
        success = random.random() < success_prob
        status_code = 200 if success else 403
        duration = random.uniform(1, 30)
        proxy_used = technique == 'advanced' and random.random() < 0.8
        
        # Determine challenge type based on technique
        if success:
            challenge_type = 'none'
        else:
            challenge_type = random.choice(challenge_types)
        
        attempt = BypassAttempt(
            timestamp=datetime.now(),
            technique=technique,
            status_code=status_code,
            success=success,
            duration=duration,
            proxy_used=proxy_used,
            challenge_type=challenge_type,
            user_agent=random.choice(user_agents),
            error_message=None if success else "Cloudflare protection"
        )
        
        monitor.log_attempt(attempt)
        
        # Small delay to simulate real usage
        time.sleep(0.01)
    
    print(f"Simulated {num_attempts} bypass attempts")

if __name__ == "__main__":
    # Initialize monitor
    monitor = BypassEffectivenessMonitor()
    
    # Generate sample data
    print("Generating sample bypass data...")
    simulate_bypass_attempts(monitor, 100)
    
    # Generate and display report
    print("\n" + "="*50)
    print("CLOUDFLARE BYPASS EFFECTIVENESS REPORT")
    print("="*50)
    
    report = monitor.generate_report(days=7)
    print(report)
    
    # Save report to file
    with open('bypass_effectiveness_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\nReport saved to bypass_effectiveness_report.md")
    
    # Create visualization
    monitor.plot_success_rates(days=7)
    
    print("\nMonitoring system ready for real bypass tracking!")