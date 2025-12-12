#!/usr/bin/env python3
"""
Configuration Manager for Promotion Parser
Handles different parsing modes and settings
"""
import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class ParserConfig:
    """Configuration settings for the promotion parser"""
    # Basic settings
    target_url: str = "https://www.bigdabach.co.il/"
    store_name: str = "Dabach"
    
    # Retry settings
    max_attempts: int = 5
    initial_delay: float = 2.0
    max_delay: float = 60.0
    backoff_factor: float = 2.0
    
    # Request settings
    request_timeout: int = 30
    user_agent_rotation: bool = True
    respect_robots_txt: bool = True
    
    # Cloudflare bypass settings
    use_enhanced_headers: bool = True
    use_proxy_rotation: bool = False
    use_mock_data_fallback: bool = True
    
    # Database settings
    database_url: str = "sqlite:///promotions.db"
    duplicate_checking: bool = True
    
    # Logging settings
    log_level: str = "INFO"
    log_to_file: bool = True
    log_file: str = "promotion_parser.log"
    
    # Mock data settings
    mock_data_enabled: bool = True
    mock_items_count: int = 5
    
    def save_to_file(self, config_path: str = "parser_config.json"):
        """Save configuration to JSON file"""
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, config_path: str = "parser_config.json"):
        """Load configuration from JSON file"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return cls(**config_data)
        else:
            return cls()  # Return default config
    
    def update_from_args(self, args: Dict[str, Any]):
        """Update configuration from command line arguments"""
        for key, value in args.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
    
    def get_proxy_config(self) -> Optional[Dict[str, str]]:
        """Get proxy configuration if enabled"""
        if not self.use_proxy_rotation:
            return None
        
        proxies_file = "proxies.json"
        if os.path.exists(proxies_file):
            try:
                with open(proxies_file, 'r') as f:
                    proxy_data = json.load(f)
                    
                # Return first working proxy (in real implementation, would rotate)
                working_proxies = [p for p in proxy_data if p.get('is_working', True)]
                if working_proxies:
                    proxy = working_proxies[0]
                    
                    auth = ""
                    if proxy.get('username') and proxy.get('password'):
                        auth = f"{proxy['username']}:{proxy['password']}@"
                    
                    proxy_url = f"http://{auth}{proxy['host']}:{proxy['port']}"
                    return {
                        'http': proxy_url,
                        'https': proxy_url
                    }
            except Exception as e:
                print(f"Warning: Could not load proxy configuration: {e}")
        
        return None
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get configuration for monitoring system"""
        return {
            'monitoring_enabled': True,
            'log_bypass_attempts': True,
            'track_success_rates': True,
            'save_challenge_types': True,
            'monitoring_db': 'bypass_monitoring.db'
        }

class ParserMode:
    """Different parsing modes and their configurations"""
    
    @staticmethod
    def get_demo_mode() -> ParserConfig:
        """Configuration for demonstration mode"""
        config = ParserConfig()
        config.use_mock_data_fallback = True
        config.max_attempts = 3  # Quick attempts
        config.log_level = "INFO"
        return config
    
    @staticmethod
    def get_production_mode() -> ParserConfig:
        """Configuration for production parsing"""
        config = ParserConfig()
        config.use_mock_data_fallback = False  # Don't fall back in production
        config.max_attempts = 10  # More attempts
        config.use_proxy_rotation = True
        config.use_enhanced_headers = True
        config.log_level = "WARNING"  # Less verbose in production
        return config
    
    @staticmethod
    def get_debug_mode() -> ParserConfig:
        """Configuration for debugging"""
        config = ParserConfig()
        config.max_attempts = 2
        config.log_level = "DEBUG"
        config.log_to_file = True
        return config
    
    @staticmethod
    def get_testing_mode() -> ParserConfig:
        """Configuration for testing"""
        config = ParserConfig()
        config.use_mock_data_fallback = True
        config.max_attempts = 1
        config.log_level = "ERROR"  # Minimal logging for tests
        return config

def create_default_config():
    """Create and save default configuration"""
    config = ParserConfig()
    config.save_to_file()
    print("Default configuration saved to parser_config.json")
    return config

def interactive_config_setup():
    """Interactive configuration setup"""
    print("=== Promotion Parser Configuration Setup ===\n")
    
    config = ParserConfig()
    
    # Basic settings
    print("1. Basic Settings:")
    config.target_url = input(f"Target URL [{config.target_url}]: ").strip() or config.target_url
    config.store_name = input(f"Store Name [{config.store_name}]: ").strip() or config.store_name
    
    # Retry settings
    print("\n2. Retry Settings:")
    config.max_attempts = int(input(f"Max Attempts [{config.max_attempts}]: ").strip() or config.max_attempts)
    config.request_timeout = int(input(f"Request Timeout (seconds) [{config.request_timeout}]: ").strip() or config.request_timeout)
    
    # Cloudflare bypass settings
    print("\n3. Cloudflare Bypass Settings:")
    config.use_enhanced_headers = input(f"Use Enhanced Headers (y/n) [y]: ").strip().lower() == 'y'
    config.use_proxy_rotation = input(f"Use Proxy Rotation (y/n) [n]: ").strip().lower() == 'y'
    
    # Mock data settings
    print("\n4. Mock Data Settings:")
    config.use_mock_data_fallback = input(f"Use Mock Data Fallback (y/n) [y]: ").strip().lower() != 'n'
    
    # Logging settings
    print("\n5. Logging Settings:")
    log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
    print(f"Log Levels: {log_levels}")
    config.log_level = input(f"Log Level [INFO]: ").strip().upper() or "INFO"
    
    # Save configuration
    config.save_to_file()
    print(f"\nConfiguration saved to parser_config.json")
    
    return config

def show_current_config():
    """Display current configuration"""
    config = ParserConfig.load_from_file()
    
    print("=== Current Parser Configuration ===")
    print(f"Target URL: {config.target_url}")
    print(f"Store Name: {config.store_name}")
    print(f"Max Attempts: {config.max_attempts}")
    print(f"Request Timeout: {config.request_timeout}s")
    print(f"Enhanced Headers: {config.use_enhanced_headers}")
    print(f"Proxy Rotation: {config.use_proxy_rotation}")
    print(f"Mock Data Fallback: {config.use_mock_data_fallback}")
    print(f"Log Level: {config.log_level}")
    print(f"Database URL: {config.database_url}")
    
    # Check proxy configuration
    proxy_config = config.get_proxy_config()
    if proxy_config:
        print(f"Proxy Configuration: Available")
    else:
        print(f"Proxy Configuration: Not configured")

def validate_configuration(config: ParserConfig) -> bool:
    """Validate configuration settings"""
    errors = []
    
    # Validate URL
    if not config.target_url.startswith(('http://', 'https://')):
        errors.append("Target URL must start with http:// or https://")
    
    # Validate numeric settings
    if config.max_attempts <= 0:
        errors.append("Max attempts must be positive")
    
    if config.request_timeout <= 0:
        errors.append("Request timeout must be positive")
    
    if config.initial_delay < 0:
        errors.append("Initial delay cannot be negative")
    
    # Validate log level
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if config.log_level.upper() not in valid_log_levels:
        errors.append(f"Invalid log level. Must be one of: {valid_log_levels}")
    
    # Check proxy file if proxy rotation is enabled
    if config.use_proxy_rotation and not os.path.exists("proxies.json"):
        errors.append("Proxy rotation enabled but proxies.json not found")
    
    if errors:
        print("Configuration validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("Configuration validation: ✅ PASSED")
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create":
            create_default_config()
        elif command == "interactive":
            interactive_config_setup()
        elif command == "show":
            show_current_config()
        elif command == "validate":
            config = ParserConfig.load_from_file()
            validate_configuration(config)
        elif command == "demo":
            config = ParserMode.get_demo_mode()
            config.save_to_file("demo_config.json")
            print("Demo mode configuration saved to demo_config.json")
        elif command == "production":
            config = ParserMode.get_production_mode()
            config.save_to_file("production_config.json")
            print("Production mode configuration saved to production_config.json")
        else:
            print("Available commands:")
            print("  create - Create default configuration")
            print("  interactive - Interactive configuration setup")
            print("  show - Show current configuration")
            print("  validate - Validate current configuration")
            print("  demo - Create demo mode configuration")
            print("  production - Create production mode configuration")
    else:
        # Default action: show current config
        show_current_config()