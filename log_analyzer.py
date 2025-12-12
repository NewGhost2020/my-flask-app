#!/usr/bin/env python3
"""
Log Analyzer for Promotion Parser
Analyzes parser logs and generates detailed statistics
"""
import re
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
import statistics

class ParserLogAnalyzer:
    """Analyzer for promotion parser logs"""
    
    def __init__(self, log_file: str = "promotion_parser.log"):
        self.log_file = log_file
        self.log_entries = []
        
    def load_logs(self) -> bool:
        """Load and parse log file"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse log entries
            log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (.+)'
            
            for match in re.finditer(log_pattern, content):
                timestamp_str, level, message = match.groups()
                
                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                    
                    entry = {
                        'timestamp': timestamp,
                        'level': level,
                        'message': message,
                        'raw': match.group(0)
                    }
                    
                    self.log_entries.append(entry)
                    
                except ValueError:
                    continue
            
            print(f"Loaded {len(self.log_entries)} log entries")
            return True
            
        except FileNotFoundError:
            print(f"Log file {self.log_file} not found")
            return False
        except Exception as e:
            print(f"Error loading logs: {e}")
            return False
    
    def get_execution_sessions(self) -> List[Dict]:
        """Identify parser execution sessions"""
        sessions = []
        
        # Find session start markers
        start_markers = [
            "PROMOTION PARSER EXECUTION STARTED",
            "Starting to parse"
        ]
        
        end_markers = [
            "PROMOTION PARSER EXECUTION COMPLETED",
            "Parser Execution Result"
        ]
        
        current_session = None
        
        for entry in self.log_entries:
            message = entry['message']
            
            # Check for session start
            if any(marker in message for marker in start_markers):
                if current_session:
                    sessions.append(current_session)
                
                current_session = {
                    'start_time': entry['timestamp'],
                    'start_level': entry['level'],
                    'start_message': message,
                    'end_time': None,
                    'end_level': None,
                    'end_message': None,
                    'attempts': [],
                    'products_found': 0,
                    'products_saved': 0,
                    'products_skipped': 0,
                    'duration': 0,
                    'status': 'unknown',
                    'errors': []
                }
            
            # Check for session end
            elif current_session and any(marker in message for marker in end_markers):
                current_session['end_time'] = entry['timestamp']
                current_session['end_level'] = entry['level']
                current_session['end_message'] = message
                
                # Calculate duration
                if current_session['start_time'] and current_session['end_time']:
                    current_session['duration'] = (
                        current_session['end_time'] - current_session['start_time']
                    ).total_seconds()
            
            # Collect detailed information
            elif current_session:
                # Parse attempt information
                if "Attempt" in message and "/" in message:
                    current_session['attempts'].append({
                        'message': message,
                        'timestamp': entry['timestamp'],
                        'level': entry['level']
                    })
                
                # Parse result statistics
                elif "Items found:" in message:
                    try:
                        count = int(re.search(r'Items found: (\d+)', message).group(1))
                        current_session['products_found'] = count
                    except:
                        pass
                
                elif "Items saved:" in message:
                    try:
                        count = int(re.search(r'Items saved: (\d+)', message).group(1))
                        current_session['products_saved'] = count
                    except:
                        pass
                
                elif "Items skipped:" in message:
                    try:
                        count = int(re.search(r'Items skipped: (\d+)', message).group(1))
                        current_session['products_skipped'] = count
                    except:
                        pass
                
                # Parse status
                elif "Status:" in message:
                    try:
                        status = re.search(r'Status: (\w+)', message).group(1)
                        current_session['status'] = status
                    except:
                        pass
                
                # Collect errors
                elif entry['level'] == 'ERROR':
                    current_session['errors'].append({
                        'message': message,
                        'timestamp': entry['timestamp']
                    })
        
        # Add the last session if exists
        if current_session:
            sessions.append(current_session)
        
        return sessions
    
    def analyze_success_patterns(self, sessions: List[Dict]) -> Dict:
        """Analyze success/failure patterns"""
        analysis = {
            'total_sessions': len(sessions),
            'successful_sessions': 0,
            'failed_sessions': 0,
            'success_rate': 0.0,
            'avg_duration': 0.0,
            'common_errors': Counter(),
            'status_distribution': Counter(),
            'duration_by_status': defaultdict(list)
        }
        
        if not sessions:
            return analysis
        
        # Analyze each session
        for session in sessions:
            status = session.get('status', 'unknown')
            duration = session.get('duration', 0)
            
            analysis['status_distribution'][status] += 1
            
            if status in ['success', 'success_with_mock', 'success_with_advanced_bypass']:
                analysis['successful_sessions'] += 1
            else:
                analysis['failed_sessions'] += 1
            
            if duration > 0:
                analysis['duration_by_status'][status].append(duration)
            
            # Count common errors
            for error in session.get('errors', []):
                # Extract error type
                if 'Cloudflare protection' in error['message']:
                    analysis['common_errors']['Cloudflare Protection'] += 1
                elif 'Network error' in error['message']:
                    analysis['common_errors']['Network Error'] += 1
                elif 'timeout' in error['message'].lower():
                    analysis['common_errors']['Timeout'] += 1
                else:
                    analysis['common_errors']['Other'] += 1
        
        # Calculate averages
        if analysis['total_sessions'] > 0:
            analysis['success_rate'] = (analysis['successful_sessions'] / analysis['total_sessions']) * 100
        
        # Calculate average durations
        for status, durations in analysis['duration_by_status'].items():
            if durations:
                analysis['duration_by_status'][status] = statistics.mean(durations)
        
        return analysis
    
    def analyze_attempt_patterns(self, sessions: List[Dict]) -> Dict:
        """Analyze request attempt patterns"""
        attempt_analysis = {
            'total_attempts': 0,
            'successful_attempts': 0,
            'failed_attempts': 0,
            'avg_attempts_per_session': 0.0,
            'max_attempts_needed': 0,
            'attempt_outcomes': Counter()
        }
        
        for session in sessions:
            attempts = session.get('attempts', [])
            attempt_analysis['total_attempts'] += len(attempts)
            
            if len(attempts) > attempt_analysis['max_attempts_needed']:
                attempt_analysis['max_attempts_needed'] = len(attempts)
            
            # Analyze attempt outcomes
            for attempt in attempts:
                message = attempt['message']
                
                if "Successfully accessed" in message:
                    attempt_analysis['successful_attempts'] += 1
                    attempt_analysis['attempt_outcomes']['Success'] += 1
                elif "Access forbidden (403)" in message:
                    attempt_analysis['failed_attempts'] += 1
                    attempt_analysis['attempt_outcomes']['403 Forbidden'] += 1
                elif "timeout" in message.lower():
                    attempt_analysis['failed_attempts'] += 1
                    attempt_analysis['attempt_outcomes']['Timeout'] += 1
                elif "Service unavailable (503)" in message:
                    attempt_analysis['failed_attempts'] += 1
                    attempt_analysis['attempt_outcomes']['503 Unavailable'] += 1
                else:
                    attempt_analysis['failed_attempts'] += 1
                    attempt_analysis['attempt_outcomes']['Other Failure'] += 1
        
        if sessions:
            attempt_analysis['avg_attempts_per_session'] = attempt_analysis['total_attempts'] / len(sessions)
        
        return attempt_analysis
    
    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive log analysis report"""
        if not self.log_entries:
            if not self.load_logs():
                return "No log data available for analysis"
        
        sessions = self.get_execution_sessions()
        success_analysis = self.analyze_success_patterns(sessions)
        attempt_analysis = self.analyze_attempt_patterns(sessions)
        
        report = f"""
# Promotion Parser Log Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Total Parsing Sessions**: {success_analysis['total_sessions']}
- **Success Rate**: {success_analysis['success_rate']:.1f}%
- **Successful Sessions**: {success_analysis['successful_sessions']}
- **Failed Sessions**: {success_analysis['failed_sessions']}
- **Average Duration**: {success_analysis['avg_duration']:.1f} seconds

## Session Analysis

### Status Distribution
"""
        
        for status, count in success_analysis['status_distribution'].most_common():
            percentage = (count / success_analysis['total_sessions']) * 100 if success_analysis['total_sessions'] > 0 else 0
            report += f"- **{status.replace('_', ' ').title()}**: {count} sessions ({percentage:.1f}%)\n"
        
        report += f"""
### Duration Analysis (by status)
"""
        for status, duration in success_analysis['duration_by_status'].items():
            report += f"- **{status.replace('_', ' ').title()}**: {duration:.1f} seconds average\n"
        
        report += f"""
### Common Errors
"""
        for error_type, count in success_analysis['common_errors'].most_common(5):
            report += f"- **{error_type}**: {count} occurrences\n"
        
        report += f"""
## Request Attempt Analysis

### Attempt Statistics
- **Total Attempts**: {attempt_analysis['total_attempts']}
- **Successful Attempts**: {attempt_analysis['successful_attempts']}
- **Failed Attempts**: {attempt_analysis['failed_attempts']}
- **Average Attempts per Session**: {attempt_analysis['avg_attempts_per_session']:.1f}
- **Maximum Attempts Needed**: {attempt_analysis['max_attempts_needed']}

### Attempt Outcomes
"""
        for outcome, count in attempt_analysis['attempt_outcomes'].most_common():
            report += f"- **{outcome}**: {count} attempts\n"
        
        report += f"""
## Recent Sessions Detail

"""
        
        # Show details of recent sessions
        recent_sessions = sessions[-5:] if len(sessions) > 5 else sessions
        
        for i, session in enumerate(recent_sessions, 1):
            report += f"""
### Session {i}
- **Start**: {session['start_time'].strftime('%Y-%m-%d %H:%M:%S') if session['start_time'] else 'Unknown'}
- **End**: {session['end_time'].strftime('%Y-%m-%d %H:%M:%S') if session['end_time'] else 'Unknown'}
- **Duration**: {session['duration']:.1f} seconds
- **Status**: {session['status']}
- **Products Found**: {session['products_found']}
- **Products Saved**: {session['products_saved']}
- **Products Skipped**: {session['products_skipped']}
- **Attempts Made**: {len(session['attempts'])}
- **Errors**: {len(session['errors'])}
"""
        
        report += f"""
## Recommendations

### Performance Optimization
"""
        
        if success_analysis['success_rate'] < 50:
            report += "- ⚠️ **Low Success Rate**: Consider implementing proxy rotation or browser automation\n"
        
        if attempt_analysis['avg_attempts_per_session'] > 5:
            report += "- ⚠️ **High Retry Rate**: Site has strong protection, consider longer delays\n"
        
        if success_analysis['common_errors']['Cloudflare Protection'] > 0:
            report += "- 🔧 **Cloudflare Blocks**: Implement advanced bypass techniques\n"
        
        if success_analysis['common_errors']['Network Error'] > 0:
            report += "- 🌐 **Network Issues**: Check network stability and add more robust error handling\n"
        
        report += f"""
### Monitoring Suggestions
- Set up alerts for success rate drops below 20%
- Monitor average session duration for performance degradation
- Track specific error patterns for proactive issue resolution
- Implement automated fallback to mock data when real parsing fails

## Technical Details
- **Log File**: {self.log_file}
- **Total Log Entries**: {len(self.log_entries)}
- **Analysis Period**: {sessions[0]['start_time'].strftime('%Y-%m-%d') if sessions and sessions[0]['start_time'] else 'Unknown'} to {sessions[-1]['end_time'].strftime('%Y-%m-%d') if sessions and sessions[-1]['end_time'] else 'Unknown'}
"""
        
        return report
    
    def export_session_data(self, output_file: str = "parser_sessions.json"):
        """Export session data to JSON for external analysis"""
        sessions = self.get_execution_sessions()
        
        # Convert datetime objects to strings for JSON serialization
        for session in sessions:
            if session['start_time']:
                session['start_time'] = session['start_time'].isoformat()
            if session['end_time']:
                session['end_time'] = session['end_time'].isoformat()
            
            for attempt in session['attempts']:
                attempt['timestamp'] = attempt['timestamp'].isoformat()
            
            for error in session['errors']:
                error['timestamp'] = error['timestamp'].isoformat()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, indent=2, ensure_ascii=False)
        
        print(f"Session data exported to {output_file}")
        return output_file

def main():
    """Main function for log analysis"""
    import sys
    
    analyzer = ParserLogAnalyzer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "analyze":
            report = analyzer.generate_comprehensive_report()
            
            # Save report to file
            with open('log_analysis_report.md', 'w', encoding='utf-8') as f:
                f.write(report)
            
            print("Log analysis report generated:")
            print("=" * 50)
            print(report)
            print("=" * 50)
            print("Full report saved to log_analysis_report.md")
        
        elif command == "export":
            analyzer.export_session_data()
        
        elif command == "load":
            if analyzer.load_logs():
                print(f"Successfully loaded {len(analyzer.log_entries)} log entries")
            else:
                print("Failed to load log file")
    else:
        # Default: analyze and display report
        report = analyzer.generate_comprehensive_report()
        print(report)

if __name__ == "__main__":
    main()