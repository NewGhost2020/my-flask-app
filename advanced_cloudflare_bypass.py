#!/usr/bin/env python3
"""
Advanced Cloudflare Bypass Techniques Implementation
This module contains advanced methods for handling Cloudflare protection
"""
import time
import random
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ProxyConfig:
    """Proxy configuration for rotation"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    country: Optional[str] = None
    is_working: bool = True

class AdvancedCloudflareBypass:
    """Advanced methods for bypassing Cloudflare protection"""
    
    def __init__(self):
        self.proxy_list = []
        self.current_proxy_index = 0
        self.success_count = 0
        self.failure_count = 0
        
    def load_proxy_list(self, proxy_file: str = "proxies.json"):
        """Load proxy list from JSON file"""
        try:
            with open(proxy_file, 'r') as f:
                proxy_data = json.load(f)
                self.proxy_list = [
                    ProxyConfig(**proxy) for proxy in proxy_data
                ]
            logging.info(f"Loaded {len(self.proxy_list)} proxies")
        except FileNotFoundError:
            logging.warning(f"Proxy file {proxy_file} not found")
        except Exception as e:
            logging.error(f"Error loading proxies: {e}")
    
    def get_random_proxy(self) -> Optional[ProxyConfig]:
        """Get a random working proxy"""
        working_proxies = [p for p in self.proxy_list if p.is_working]
        if not working_proxies:
            logging.warning("No working proxies available")
            return None
        
        return random.choice(working_proxies)
    
    def rotate_proxy(self) -> Optional[Dict[str, str]]:
        """Get proxy configuration for requests"""
        proxy = self.get_random_proxy()
        if not proxy:
            return None
        
        auth = ""
        if proxy.username and proxy.password:
            auth = f"{proxy.username}:{proxy.password}@"
        
        proxy_url = f"http://{auth}{proxy.host}:{proxy.port}"
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def mark_proxy_result(self, proxy: ProxyConfig, success: bool):
        """Mark proxy as working or not based on result"""
        if success:
            proxy.is_working = True
            self.success_count += 1
        else:
            proxy.is_working = False
            self.failure_count += 1
            
        # Log proxy health
        total = self.success_count + self.failure_count
        if total > 0:
            success_rate = (self.success_count / total) * 100
            logging.debug(f"Proxy {proxy.host}:{proxy.port} - Success rate: {success_rate:.1f}%")
    
    def get_stealth_headers(self) -> Dict[str, str]:
        """Generate highly realistic browser headers"""
        
        # Multiple browser profiles for rotation
        browser_profiles = {
            'chrome_windows': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Ch-Ua-Platform-Version': '"10.0.0"',
                'Sec-Ch-Ua-Full-Version-List': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.216", "Google Chrome";v="120.0.6099.216"',
            },
            'chrome_mac': {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Sec-Ch-Ua-Platform': '"macOS"',
                'Sec-Ch-Ua-Platform-Version': '"13.0.0"',
                'Sec-Ch-Ua-Full-Version-List': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.216", "Google Chrome";v="120.0.6099.216"',
            },
            'firefox_windows': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
                'Sec-Ch-Ua': 'Not_A Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            },
            'safari_mac': {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
                'Sec-Ch-Ua': 'Not A(Brand";v="99", "Chromium";v="121", "Not)A;Brand";v="99"',
            }
        }
        
        profile_name = random.choice(list(browser_profiles.keys()))
        base_headers = browser_profiles[profile_name]
        
        # Add common headers
        common_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        
        # Merge headers
        headers = {**common_headers, **base_headers}
        
        return headers
    
    def generate_realistic_cookies(self, domain: str) -> Dict[str, str]:
        """Generate realistic browser cookies"""
        current_time = int(time.time())
        random.seed(current_time)
        
        cookies = {
            # Cloudflare related
            'cf_use_ob': '0',
            '__cf_bm': f'{random.randint(1000000000, 9999999999)}.{current_time}',
            
            # Common site cookies
            'cookie_consent': 'true',
            'gdpr_consent': 'true',
            'cookie_settings': 'true',
            
            # Language and region
            'language': 'he',
            'currency': 'ILS',
            'timezone': 'Asia/Jerusalem',
            'region': 'IL',
            
            # Session and preferences
            'session_id': f'sess_{random.randint(100000, 999999)}{current_time}',
            'user_preferences': json.dumps({
                'language': 'he',
                'currency': 'ILS',
                'notifications': True
            }),
            
            # Marketing and analytics
            'marketing_opt_in': 'true',
            'analytics_opt_in': 'true',
        }
        
        # Add Google Analytics cookies
        ga_id = f"GA1.2.{random.randint(1000000000, 9999999999)}.{current_time}"
        cookies.update({
            '_ga': ga_id,
            '_gid': f"GA1.2.{random.randint(1000000000, 9999999999)}.{current_time}",
            '_gat': '1',
            '_gac_UA-XXXX-Y': f'1.{current_time}.0.0',
            'AMP_TOKEN': '%',
        })
        
        # Add Facebook cookies
        cookies.update({
            '_fbp': f'fb.1.{current_time}.{random.randint(1000000000, 9999999999)}',
            '_fbc': f'fb.1.{current_time}.{random.randint(1000000000, 9999999999)}',
        })
        
        return cookies
    
    def simulate_human_behavior(self):
        """Simulate human-like delays and patterns"""
        # Random thinking time (2-8 seconds)
        thinking_time = random.uniform(2, 8)
        logging.debug(f"Human-like thinking time: {thinking_time:.2f} seconds")
        time.sleep(thinking_time)
        
        # Simulate reading time based on content length (if we had content)
        # reading_time = content_length / 200  # Average reading speed
        # time.sleep(random.uniform(reading_time * 0.8, reading_time * 1.2))
    
    def handle_different_cf_challenges(self, response_text: str, status_code: int) -> Dict[str, str]:
        """Handle different types of Cloudflare challenges"""
        challenge_info = {
            'type': 'unknown',
            'recommended_action': 'unknown',
            'bypass_possible': False
        }
        
        text_lower = response_text.lower()
        
        if 'javascript challenge' in text_lower or 'cf-chl' in text_lower:
            challenge_info.update({
                'type': 'javascript_challenge',
                'recommended_action': 'Use Selenium with undetected-chromedriver',
                'bypass_possible': True
            })
        elif 'captcha' in text_lower:
            challenge_info.update({
                'type': 'captcha',
                'recommended_action': 'Manual human verification or 2captcha service',
                'bypass_possible': False
            })
        elif 'rate limit' in text_lower or 'too many requests' in text_lower:
            challenge_info.update({
                'type': 'rate_limiting',
                'recommended_action': 'Increase delays and reduce request frequency',
                'bypass_possible': True
            })
        elif 'bot detection' in text_lower:
            challenge_info.update({
                'type': 'bot_detection',
                'recommended_action': 'Use residential proxies or browser automation',
                'bypass_possible': True
            })
        elif status_code == 403:
            challenge_info.update({
                'type': 'ip_blocking',
                'recommended_action': 'Use proxy rotation with residential IPs',
                'bypass_possible': True
            })
        
        return challenge_info
    
    def create_session_with_bypass(self, use_proxy: bool = True) -> Dict:
        """Create a requests session with advanced bypass techniques"""
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        session = requests.Session()
        
        # Set realistic headers
        headers = self.get_stealth_headers()
        session.headers.update(headers)
        
        # Set realistic cookies
        cookies = self.generate_realistic_cookies('bigdabach.co.il')
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.bigdabach.co.il')
        
        # Configure proxy if available
        proxy_config = None
        if use_proxy and self.proxy_list:
            proxy_config = self.rotate_proxy()
            if proxy_config:
                session.proxies.update(proxy_config)
                logging.info(f"Using proxy: {proxy_config['http']}")
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return {
            'session': session,
            'proxy_config': proxy_config,
            'headers': headers,
            'cookies': cookies
        }

# Example proxy configuration file (proxies.json)
EXAMPLE_PROXIES = [
    {
        "host": "proxy1.example.com",
        "port": 8080,
        "username": "user1",
        "password": "pass1",
        "country": "US",
        "is_working": True
    },
    {
        "host": "proxy2.example.com", 
        "port": 3128,
        "country": "UK",
        "is_working": True
    },
    {
        "host": "proxy3.example.com",
        "port": 1080,
        "username": "user2",
        "password": "pass2",
        "country": "DE",
        "is_working": False
    }
]

def save_example_proxies():
    """Save example proxy configuration"""
    with open('proxies.json', 'w') as f:
        json.dump(EXAMPLE_PROXIES, f, indent=2)
    print("Example proxies.json created. Please update with real proxy servers.")

if __name__ == "__main__":
    # Save example configuration
    save_example_proxies()
    
    # Demonstrate usage
    bypass = AdvancedCloudflareBypass()
    bypass.load_proxy_list()
    
    # Create session with bypass techniques
    session_info = bypass.create_session_with_bypass()
    print(f"Session created with headers: {len(session_info['headers'])}")
    print(f"Cookies set: {len(session_info['cookies'])}")
    print(f"Using proxy: {session_info['proxy_config'] is not None}")