import os
import json
from utils.logging import setup_logging
from utils.config import ConfigManager
from core.attribution.image.image_analyzer import ImageAnalyzer

def run_image_analyzer_test():
    """
    Tests the ImageAnalyzer module with a sample image.
    """
    # Initialize framework components
    config = ConfigManager()
    logger = setup_logging(level=config.get("logging.level", "INFO"))

    logger.info("--- Running ImageAnalyzer Test ---")

    # Create a dummy image for testing if it doesn't exist
    # For a real test, you'd place a sample_image.jpg with EXIF data
    sample_image_path = "sample_image.jpg"
    if not os.path.exists(sample_image_path):
        logger.warning(f"'{sample_image_path}' not found. Please place an image with EXIF data in the root directory for a meaningful test.")
        # Create a very basic dummy image if none exists, just to avoid file not found error
        try:
            from PIL import Image
            img = Image.new('RGB', (60, 30), color = 'red')
            img.save(sample_image_path)
            logger.info(f"Created a dummy '{sample_image_path}' for testing. It will likely have no EXIF data.")
        except ImportError:
            logger.error("Pillow not installed. Cannot create dummy image. Please install Pillow and provide a sample_image.jpg.")
            return

    analyzer = ImageAnalyzer(config.settings)
    analysis_result = analyzer.execute(sample_image_path)

    logger.info("\n--- Image Analysis Result ---")
    logger.info(json.dumps(analysis_result, indent=4))

if __name__ == "__main__":
    run_image_analyzer_test()