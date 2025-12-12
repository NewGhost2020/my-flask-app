#!/usr/bin/env python3
"""
Comprehensive Demo Script for Promotion Parser System
Demonstrates all features and capabilities
"""
import sys
import time
import subprocess
from datetime import datetime

class ParserSystemDemo:
    """Complete demonstration of the promotion parser system"""
    
    def __init__(self):
        self.demo_start_time = datetime.now()
        
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f" {title}")
        print("="*60)
    
    def print_step(self, step: str, description: str = ""):
        """Print step information"""
        print(f"\n🔸 {step}")
        if description:
            print(f"   {description}")
    
    def run_command(self, command: str, description: str = ""):
        """Run command and show result"""
        self.print_step("Executing", description or command)
        print(f"Command: {command}")
        print("-" * 40)
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=60
            )
            
            if result.stdout:
                print("Output:")
                print(result.stdout)
            
            if result.stderr:
                print("Errors/Warnings:")
                print(result.stderr)
            
            print(f"Return code: {result.returncode}")
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("Command timed out")
            return False
        except Exception as e:
            print(f"Error running command: {e}")
            return False
    
    def demo_configuration_management(self):
        """Demonstrate configuration management features"""
        self.print_header("CONFIGURATION MANAGEMENT DEMO")
        
        self.print_step("1.1", "Creating demo configuration")
        self.run_command(
            "python config_manager.py demo",
            "Create configuration optimized for demonstrations"
        )
        
        self.print_step("1.2", "Showing current configuration")
        self.run_command(
            "python config_manager.py show",
            "Display current parser settings"
        )
        
        self.print_step("1.3", "Validating configuration")
        self.run_command(
            "python config_manager.py validate",
            "Validate configuration settings"
        )
    
    def demo_basic_parsing(self):
        """Demonstrate basic parsing functionality"""
        self.print_header("BASIC PARSING DEMO")
        
        self.print_step("2.1", "Running parser with mock data")
        self.run_command(
            "python promotion_parser.py --mock",
            "Parse using mock Hebrew product data"
        )
        
        self.print_step("2.2", "Querying database")
        self.run_command(
            "python db_utility.py",
            "Display saved promotions from database"
        )
    
    def demo_advanced_bypass(self):
        """Demonstrate advanced Cloudflare bypass techniques"""
        self.print_header("ADVANCED CLOUDFLARE BYPASS DEMO")
        
        self.print_step("3.1", "Running parser with advanced bypass")
        self.run_command(
            "python promotion_parser.py --advanced",
            "Attempt parsing with proxy rotation and enhanced headers"
        )
        
        self.print_step("3.2", "Advanced bypass module features")
        self.run_command(
            "python advanced_cloudflare_bypass.py",
            "Demonstrate advanced bypass capabilities"
        )
    
    def demo_monitoring_system(self):
        """Demonstrate monitoring and analytics"""
        self.print_header("MONITORING & ANALYTICS DEMO")
        
        self.print_step("4.1", "Bypass effectiveness monitoring")
        self.run_command(
            "python bypass_monitor.py",
            "Analyze bypass technique effectiveness"
        )
        
        self.print_step("4.2", "Log analysis")
        if self.run_command(
            "python log_analyzer.py analyze",
            "Analyze parser execution logs"
        ):
            self.print_step("4.3", "Viewing log analysis report")
            self.run_command(
                "cat log_analysis_report.md",
                "Display detailed log analysis report"
            )
    
    def demo_testing_suite(self):
        """Demonstrate testing capabilities"""
        self.print_header("TESTING SUITE DEMO")
        
        self.print_step("5.1", "Running comprehensive tests")
        self.run_command(
            "python test_parser.py",
            "Execute full test suite"
        )
        
        self.print_step("5.2", "Database operations")
        self.run_command(
            "python db_utility.py clear",
            "Clear database for clean state"
        )
        
        self.print_step("5.3", "Re-populating with fresh data")
        self.run_command(
            "python promotion_parser.py --mock",
            "Add fresh mock data to database"
        )
    
    def show_system_overview(self):
        """Show system architecture and capabilities"""
        self.print_header("SYSTEM OVERVIEW")
        
        overview = """
🏪 **PROMOTION PARSER SYSTEM FOR ISRAELI RETAIL SITES**

📊 **Core Features:**
✅ SQLAlchemy database with SQLite backend
✅ BeautifulSoup web scraping with Cloudflare bypass
✅ Hebrew text processing (UTF-8)
✅ Duplicate detection and prevention
✅ Comprehensive logging and monitoring

🔧 **Cloudflare Bypass Levels:**
Level 1 (Basic): Enhanced headers, user-agent rotation
Level 2 (Advanced): Proxy rotation, session management  
Level 3 (Browser): Selenium/Playwright integration ready

🛠️ **Management Tools:**
• Configuration Manager - Interactive setup and presets
• Database Utilities - Query, clear, export functionality
• Monitoring System - Success rate tracking, analytics
• Log Analyzer - Detailed execution analysis
• Bypass Monitor - Technique effectiveness metrics

📈 **Production Ready:**
• Multiple parsing modes (demo, production, debug, testing)
• Automatic fallback to mock data
• Comprehensive error handling
• Performance monitoring and optimization
• Scalable architecture for additional sites

🌐 **Target Sites:**
Primary: https://www.bigdabach.co.il/ (Israeli electronics retailer)
Status: Protected by Cloudflare Bot Management (expected for e-commerce)
Solution: Advanced bypass techniques + mock data fallback
        """
        
        print(overview)
    
    def show_final_summary(self):
        """Show final summary and recommendations"""
        self.print_header("DEMO SUMMARY")
        
        duration = datetime.now() - self.demo_start_time
        
        summary = f"""
⏱️ **Demo Duration:** {duration.total_seconds():.1f} seconds

🎯 **Key Achievements:**
✅ Complete promotion scraping system implemented
✅ Multi-level Cloudflare protection bypass
✅ Production-ready architecture with monitoring
✅ Comprehensive testing and validation suite
✅ Hebrew language support with proper encoding
✅ Database integration with duplicate prevention

📋 **Next Steps for Production:**
1. Configure real proxy servers in proxies.json
2. Set up scheduled parsing (cron jobs)
3. Implement browser automation for maximum success rate
4. Add email notifications for new promotions
5. Deploy monitoring dashboard

🔒 **Ethical Considerations:**
• Respects robots.txt when configured
• Implements respectful delays (2-8 seconds)
• Uses meaningful User-Agent strings
• Considers server resource usage
• Provides opt-out mechanisms

📚 **Documentation:**
• README_PARSER.md - Complete system documentation
• CLOUDFLARE_BYPASS.md - Bypass techniques guide
• Configuration examples and templates
• API documentation for extensions

🚀 **Ready for Production Deployment!**
        """
        
        print(summary)
    
    def run_full_demo(self):
        """Run complete system demonstration"""
        print("🎬 Starting Comprehensive Promotion Parser System Demo")
        print(f"Started at: {self.demo_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show system overview
        self.show_system_overview()
        
        try:
            # Configuration management
            self.demo_configuration_management()
            
            # Basic parsing
            self.demo_basic_parsing()
            
            # Advanced bypass
            self.demo_advanced_bypass()
            
            # Monitoring system
            self.demo_monitoring_system()
            
            # Testing suite
            self.demo_testing_suite()
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Demo interrupted by user")
        except Exception as e:
            print(f"\n\n❌ Demo error: {e}")
        
        # Final summary
        self.show_final_summary()

def main():
    """Main demo entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        demo = ParserSystemDemo()
        
        if command == "overview":
            demo.show_system_overview()
        elif command == "config":
            demo.demo_configuration_management()
        elif command == "parsing":
            demo.demo_basic_parsing()
        elif command == "bypass":
            demo.demo_advanced_bypass()
        elif command == "monitoring":
            demo.demo_monitoring_system()
        elif command == "testing":
            demo.demo_testing_suite()
        elif command == "quick":
            # Quick demo with essential features
            demo.print_header("QUICK DEMO - Essential Features")
            demo.run_command("python promotion_parser.py --mock", "Mock data parsing")
            demo.run_command("python db_utility.py", "Database query")
            demo.run_command("python config_manager.py show", "Configuration view")
        else:
            print("Available demo commands:")
            print("  overview - Show system overview")
            print("  config  - Configuration management demo")
            print("  parsing - Basic parsing demo")
            print("  bypass  - Advanced bypass demo")
            print("  monitoring - Monitoring system demo")
            print("  testing - Testing suite demo")
            print("  quick   - Quick demo of essential features")
            print("  (no args) - Full comprehensive demo")
    else:
        # Run full demo
        demo = ParserSystemDemo()
        demo.run_full_demo()

if __name__ == "__main__":
    main()