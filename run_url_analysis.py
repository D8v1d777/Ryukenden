import json
import sys
from utils.config import ConfigManager
from utils.logging import setup_logging
from core.attribution.url.url_analyzer import URLAnalyzer

def main():
    """
    Standalone script to run the Ryukenden URL Analyzer on a specific target.
    Usage: python run_url_analysis.py <url>
    """
    # Get target URL from command line or use a default example
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.google.com"

    # 1. Initialize Configuration and Logging
    # We use the framework's centralized config and logging for consistency
    config = ConfigManager()
    setup_logging(level=config.get("logging.level", "INFO"))
    
    # 2. Instantiate the URLAnalyzer
    # The analyzer inherits from BaseModule and requires the settings dictionary
    analyzer = URLAnalyzer(config.settings)
    
    # 3. Perform Analysis
    print(f"[*] Starting Ryukenden URL Intelligence for: {target_url}")
    result = analyzer.execute(target_url)
    
    # 4. Display Results
    print("\n" + "="*60)
    print(f"FORENSIC REPORT: {target_url}")
    print("="*60)
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()