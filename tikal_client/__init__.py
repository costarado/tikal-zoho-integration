"""
Tikal Call Center API Client
"""

from .client import TikalClient
from .exceptions import (
    TikalAPIError,
    TikalAuthenticationError,
    TikalConnectionError,
    TikalNotFoundError,
    TikalRateLimitError
)

__version__ = '1.0.0'
__all__ = [
    'TikalClient',
    'TikalAPIError',
    'TikalAuthenticationError',
    'TikalConnectionError',
    'TikalNotFoundError',
    'TikalRateLimitError'
]

