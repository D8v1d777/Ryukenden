import sys
from utils.logging import setup_logging
from utils.config import ConfigManager
from core.base import BaseModule
import json # Added for pretty printing JSON output
from core.attribution.image.image_analyzer import ImageAnalyzer # New import

def initialize_framework():
    """Initializes the core services of Ryukenden."""
    # 1. Load Configuration
    config = ConfigManager()
    
    # 2. Setup Logging
    log_level = config.get("logging.level", "INFO")
    logger = setup_logging(level=log_level)
    
    logger.info("--- Ryukenden Digital Forensics Framework ---")
    logger.info("Initializing clean architecture components...")
    
    return config, logger

def main():
    """Main entry point for Ryukenden."""
    try:
        config, logger = initialize_framework()
        
        logger.info("Demonstrating ImageAnalyzer:")
        # NOTE: For demonstration, ensure you have a 'sample_image.jpg' in the root directory
        # with some EXIF data, or update the path below.
        # If no image exists, the test script will create a dummy one.
        sample_image_path = "sample_image.jpg"
        try:
            from core.attribution.image.image_analyzer import ImageAnalyzer
        except ImportError:
            logger.error("ImageAnalyzer not found. Skipping image analysis demonstration.")
            image_analyzer = None

        if image_analyzer:
        analysis_result = image_analyzer.execute(sample_image_path)
        
        logger.info(f"Image Analysis Result for '{sample_image_path}':")
        logger.info(analysis_result)
        
        logger.info("Framework successfully initialized and ready for operations.")
        
        logger.info("\nDemonstrating URLAnalyzer:")
        sample_url = "https://www.google.com" # Example URL
        from core.attribution.url.url_analyzer import URLAnalyzer
        url_analyzer = URLAnalyzer(config.settings)
        analysis_result_url = url_analyzer.execute(sample_url)
        logger.info(f"URL Analysis Result for '{sample_url}':")
        logger.info(json.dumps(analysis_result_url, indent=4))

    except KeyboardInterrupt:
        print("\n[!] User interrupted. Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Critical error during initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()