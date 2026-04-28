import json
import sys
import os
from core.attribution.image.image_analyzer import ImageAnalyzer

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_image.py <path_to_image>")
        sys.exit(1)

    # Mock config for standalone test
    config = {"logging": {"level": "INFO"}}
    
    analyzer = ImageAnalyzer(config)
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        sys.exit(1)

    print(f"[*] Analyzing: {image_path}")
    report = analyzer.execute(image_path)
    
    print("\n[FORENSIC REPORT]")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()