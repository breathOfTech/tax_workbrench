"""
Configuration loader.

Loads settings from YAML config file with environment variable overrides.
Env vars override YAML values using double-underscore notation:
    MONGODB__URI=... overrides mongodb.uri
    SERVER__PORT=... overrides server.port
"""

from pathlib import Path
from typing import Any

import yaml


_settings: dict[str, Any] = {}


def load_settings(config_path: Path | str) -> dict[str, Any]:
    """Load settings from YAML file. Call once at app startup."""
    global _settings
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path) as f:
        _settings = yaml.safe_load(f) or {}

    _apply_env_overrides()
    return _settings


def _apply_env_overrides() -> None:
    """Override YAML values with environment variables.

    Uses double-underscore as separator:
        MONGODB__URI → settings["mongodb"]["uri"]
        SERVER__PORT → settings["server"]["port"]
    """
    import os

    for key, value in os.environ.items():
        parts = key.lower().split("__")
        if len(parts) >= 2 and parts[0] in _settings:
            target = _settings
            for part in parts[:-1]:
                if part not in target:
                    break
                target = target[part]
            else:
                target[parts[-1]] = value


def get_setting(path: str, default: Any = None) -> Any:
    """Get a setting by dot-separated path. e.g. 'mongodb.uri'"""
    keys = path.split(".")
    value = _settings
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value
