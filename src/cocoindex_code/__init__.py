"""CocoIndex Code - CLI tool for indexing and querying codebases."""

from .cli import main
from .config import Config

__version__ = "0.1.0"
__all__ = ["Config", "main"]
