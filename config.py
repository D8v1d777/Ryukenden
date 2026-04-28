import os
import yaml
from typing import Any, Dict

class ConfigManager:
    """Handles configuration loading and management."""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config_path = config_path
        self.settings: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            # Return defaults or empty if config is missing
            return {"version": "1.0.0", "debug": False}
            
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration value."""
        keys = key.split(".")
        value = self.settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value